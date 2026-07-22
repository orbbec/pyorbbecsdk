# ******************************************************************************
#  pyorbbecsdk Advanced Example 15 — High-Performance Async Pipeline
#
#  What you will learn:
#    1. Callback-based pipeline (async, no blocking wait_for_frames)
#    2. Thread-safe frame queue with bounded size (drops oldest if full)
#    3. Measuring actual frame rate and processing latency
#    4. Keeping the UI thread responsive while camera runs on a background thread
#    5. Proper shutdown sequence for multi-threaded pipelines
#
#  vs. the simple approach (wait_for_frames):
#    - Simple approach: main thread blocks for up to 1 second per frame
#    - Async approach: camera fills a queue; main thread drains it independently
#    - Result: UI stays responsive even when frames arrive faster than rendering
#
#  Press 'q' or ESC to quit.
#
#  Run:
#    python examples/advanced/15_high_performance_pipeline.py
# ******************************************************************************
import collections
import threading
import time

import cv2
import numpy as np

from pyorbbecsdk import (
    Config,
    Context,
    FrameSet,
    OBError,
    OBSensorType,
    Pipeline,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MAX_QUEUE_SIZE = 5  # Drop oldest frame if queue exceeds this depth
FPS_WINDOW = 60  # Measure FPS over last N frames
MIN_DEPTH_MM = 100
MAX_DEPTH_MM = 5000
ESC_KEY = 27


# ---------------------------------------------------------------------------
# Thread-safe frame queue
# ---------------------------------------------------------------------------


class FrameQueue:
    """A bounded queue that drops the oldest item when full."""

    def __init__(self, maxsize=MAX_QUEUE_SIZE):
        self._queue = collections.deque(maxlen=maxsize)
        self._lock = threading.Lock()
        self._dropped = 0

    def put(self, item):
        with self._lock:
            if len(self._queue) == self._queue.maxlen:
                self._queue.popleft()  # discard oldest
                self._dropped += 1
            self._queue.append(item)

    def get(self):
        with self._lock:
            return self._queue.popleft() if self._queue else None

    @property
    def dropped(self):
        with self._lock:
            return self._dropped


# ---------------------------------------------------------------------------
# FPS counter
# ---------------------------------------------------------------------------


class FPSCounter:
    """Computes FPS from a sliding window of frame timestamps."""

    def __init__(self, window=FPS_WINDOW):
        self._times = collections.deque(maxlen=window)

    def tick(self):
        self._times.append(time.perf_counter())

    @property
    def fps(self):
        if len(self._times) < 2:
            return 0.0
        elapsed = self._times[-1] - self._times[0]
        return (len(self._times) - 1) / elapsed if elapsed > 0 else 0.0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    pipeline = Pipeline()
    config = Config()
    depth_q = FrameQueue()
    color_q = FrameQueue()
    camera_fps = FPSCounter()
    render_fps = FPSCounter()
    stop_event = threading.Event()

    # --- Configure streams ---
    for sensor_type in [OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR]:
        try:
            profiles = pipeline.get_stream_profile_list(sensor_type)
            config.enable_stream(profiles.get_default_video_stream_profile())
        except OBError as e:
            print(f"WARNING: {sensor_type} unavailable: {e}")

    # --- Async callback ---
    # This function is called by the SDK's internal thread each time a
    # new frame set arrives. It must return quickly — any heavy processing
    # should happen in a separate consumer thread (here: the main thread).
    def on_new_frame(frame_set: FrameSet):
        if frame_set is None or stop_event.is_set():
            return
        camera_fps.tick()

        depth = frame_set.get_depth_frame()
        color = frame_set.get_color_frame()

        if depth is not None:
            depth_q.put(depth)
        if color is not None:
            color_q.put(color)

    # --- Start pipeline with callback ---
    pipeline.start(config, on_new_frame)
    print("Pipeline started (async callback mode).")
    print("Press 'q' or ESC to quit.\n")

    try:
        # Create a resizable window for the pipeline visualization
        cv2.namedWindow("High-Performance Pipeline  |  Press 'q' to quit", cv2.WINDOW_NORMAL)

        while True:
            t0 = time.perf_counter()

            depth_frame = depth_q.get()
            color_frame = color_q.get()

            panels = []

            # Process color
            if color_frame is not None:
                w = color_frame.get_width()
                h = color_frame.get_height()
                data = np.frombuffer(color_frame.get_data(), dtype=np.uint8)
                try:
                    img = data.reshape(h, w, 3)
                    panels.append(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                except Exception:
                    pass

            # Process depth
            if depth_frame is not None:
                # Depth frames are normally raw 16-bit pixel data, but a
                # malformed frame (e.g. after a sensor timestamp anomaly) can
                # deliver a buffer whose size is not a multiple of 2 bytes, or
                # that does not match the profile. Skip such frames instead of
                # crashing the viewer.
                try:
                    w = depth_frame.get_width()
                    h = depth_frame.get_height()
                    scale = depth_frame.get_depth_scale()
                    raw = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
                    depth_mm = raw.reshape(h, w).astype(np.float32) * scale
                    clipped = np.where((depth_mm >= MIN_DEPTH_MM) & (depth_mm <= MAX_DEPTH_MM), depth_mm, 0).astype(
                        np.uint16
                    )
                    norm = cv2.normalize(clipped, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                    panels.append(cv2.applyColorMap(norm, cv2.COLORMAP_JET))
                except ValueError:
                    # Buffer size / reshape mismatch -> skip this depth frame
                    pass

            if not panels:
                time.sleep(0.005)
                continue

            render_fps.tick()
            process_ms = (time.perf_counter() - t0) * 1000

            # Stack panels and add stats overlay with white text and black outline for readability
            # Color and depth default profiles usually differ in resolution
            # (e.g. 1280x720 color vs 640x400 depth), so np.hstack would fail.
            # Normalize all panels to the tallest one, preserving aspect ratio.
            if len(panels) > 1:
                target_h = max(p.shape[0] for p in panels)
                panels = [
                    p if p.shape[0] == target_h else cv2.resize(p, (int(p.shape[1] * target_h / p.shape[0]), target_h))
                    for p in panels
                ]
            display = np.hstack(panels)
            stats = (
                f"Camera: {camera_fps.fps:.1f} fps  "
                f"Render: {render_fps.fps:.1f} fps  "
                f"Process: {process_ms:.1f}ms  "
                f"Dropped: {depth_q.dropped}d/{color_q.dropped}c"
            )
            # Black outline (draw text slightly offset in black)
            cv2.putText(display, stats, (11, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)
            cv2.putText(display, stats, (9, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)
            cv2.putText(
                display,
                stats,
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
            )

            cv2.imshow("High-Performance Pipeline  |  Press 'q' to quit", display)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ESC_KEY):
                break

    finally:
        stop_event.set()
        pipeline.stop()
        cv2.destroyAllWindows()
        print(f"\nStopped. Total frames dropped: depth={depth_q.dropped}, color={color_q.dropped}")


if __name__ == "__main__":
    main()
