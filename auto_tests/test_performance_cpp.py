"""Python translations of tests/performance with the original case IDs.

The drop-rate accounting mirrors ``PerfStreamTest::runStreamingTest``: frames are
recorded by SDK index and by metadata frame number, and a gap in either sequence
counts as a dropped frame.  Two rates are therefore checked, with the C++
thresholds (baseline 15 %, under CPU/IO stress 20 %).
"""

from __future__ import annotations

import hashlib
import os
import threading
import time

import pytest

from conftest import first_profile, ob

pytestmark = pytest.mark.performance


def _performance_config(test_config):
    config = test_config.get("performance", {})
    return {
        "duration": max(1, int(config.get("durationSeconds", 60))),
        "cpu_threads": max(1, int(config.get("cpuThreads", 2)) or os.cpu_count() or 2),
        "io_threads": max(1, int(config.get("ioThreads", 2))),
    }


def _thread_safety_config(test_config):
    config = test_config.get("threadSafety", {})
    return {
        "duration": max(1, int(config.get("durationSeconds", 10))),
        "threads": max(1, int(config.get("threadCount", 4))),
    }


def _burn_cpu(stop_event):
    blob = b"x" * 1048576
    while not stop_event.is_set():
        hashlib.sha256(blob).digest()


def _depth_config(pipeline):
    config = ob.Config()
    config.enable_stream(first_profile(pipeline, ob.OBSensorType.DEPTH_SENSOR))
    return config


def _stream_config(pipeline):
    config = ob.Config()
    for stream in (ob.OBStreamType.DEPTH_STREAM, ob.OBStreamType.COLOR_STREAM):
        try:
            config.enable_stream(stream)
        except Exception:  # noqa: BLE001
            pass
    try:
        config.set_frame_aggregate_output_mode(ob.OBFrameAggregateOutputMode.DISABLE)
    except Exception:  # noqa: BLE001
        pass
    return config


def _run_streaming_test(device, seconds):
    """Port PerfStreamTest::runStreamingTest and its FrameRecord accounting."""
    pipeline = ob.Pipeline(device)
    lock = threading.Lock()
    records = {name: {"count": 0, "indexes": [], "meta_indexes": []}
               for name in ("depth", "color", "ir")}

    frame_types = {
        ob.OBFrameType.DEPTH_FRAME: "depth",
        ob.OBFrameType.COLOR_FRAME: "color",
        ob.OBFrameType.IR_FRAME: "ir",
        ob.OBFrameType.LEFT_IR_FRAME: "ir",
        ob.OBFrameType.RIGHT_IR_FRAME: "ir",
    }

    def process(frame):
        kind = frame_types.get(frame.get_type())
        if kind is None:
            return
        with lock:
            record = records[kind]
            record["count"] += 1
            record["indexes"].append(frame.get_index())
            if frame.has_metadata(ob.OBFrameMetadataType.FRAME_NUMBER):
                record["meta_indexes"].append(
                    frame.get_metadata_value(ob.OBFrameMetadataType.FRAME_NUMBER)
                )

    def callback(frameset):
        for index in range(frameset.get_count()):
            process(frameset.get_frame_by_index(index))

    try:
        pipeline.start(_stream_config(pipeline), callback)
    except Exception:  # noqa: BLE001
        pytest.skip("Pipeline could not start the C++ performance stream configuration")

    try:
        time.sleep(seconds)
    finally:
        try:
            pipeline.stop()
        except Exception:  # noqa: BLE001
            pass

    return records


def _assert_drop_rates(records, max_rate):
    assert any(record["count"] for _, record in records.items()), (
        "No frames received during the performance test window"
    )

    for name, record in records.items():
        if not record["count"]:
            continue

        for key in ("indexes", "meta_indexes"):
            indexes = record[key]
            if len(indexes) < 2:
                continue
            span = indexes[-1] - indexes[0]
            if span <= 0:
                continue
            received = len(set(indexes))
            drops = max(0, span + 1 - received)
            rate = drops / (span + 1)
            label = "SDK index" if key == "indexes" else "metadata index"
            assert rate <= max_rate, (
                f"{name} {label} drop rate {rate:.2%} exceeds {max_rate:.0%}"
            )


def test_TC_PERF_01_frame_drop_detection(device, test_config):
    config = _performance_config(test_config)
    records = _run_streaming_test(device, config["duration"])
    _assert_drop_rates(records, 0.15)


def test_TC_PERF_02_frame_drop_under_cpu_stress(device, test_config):
    config = _performance_config(test_config)
    stop = threading.Event()
    workers = [
        threading.Thread(target=_burn_cpu, args=(stop,), daemon=True)
        for _ in range(config["cpu_threads"])
    ]
    for worker in workers:
        worker.start()
    try:
        records = _run_streaming_test(device, config["duration"])
    finally:
        stop.set()
        for worker in workers:
            worker.join(timeout=10)
    _assert_drop_rates(records, 0.20)


def test_TC_PERF_03_frame_drop_under_io_stress(device, test_config, tmp_path):
    config = _performance_config(test_config)
    stop = threading.Event()

    def stress_io(index):
        path = tmp_path / f"io_stress_{index}.bin"
        payload = b"y" * 1048576
        while not stop.is_set():
            path.write_bytes(payload)
            path.read_bytes()

    workers = [
        threading.Thread(target=stress_io, args=(index,), daemon=True)
        for index in range(config["io_threads"])
    ]
    for worker in workers:
        worker.start()
    try:
        records = _run_streaming_test(device, config["duration"])
    finally:
        stop.set()
        for worker in workers:
            worker.join(timeout=10)
    _assert_drop_rates(records, 0.20)


def test_TC_TS_01_concurrent_pipeline_start_stop(device, test_config):
    config = _thread_safety_config(test_config)
    pipeline = ob.Pipeline(device)
    errors = []
    stop = threading.Event()

    def worker():
        while not stop.is_set():
            try:
                pipeline.start(_depth_config(pipeline))
                time.sleep(0.5)
                pipeline.stop()
            except ob.OBError:
                # A concurrent start/stop is allowed to be refused.
                pass
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

    workers = [
        threading.Thread(target=worker, daemon=True) for _ in range(config["threads"])
    ]
    for item in workers:
        item.start()
    try:
        deadline = time.monotonic() + config["duration"]
        while time.monotonic() < deadline:
            pipeline.wait_for_frames(1000)
    finally:
        stop.set()
        for item in workers:
            item.join(timeout=15)
        try:
            pipeline.stop()
        except Exception:  # noqa: BLE001
            pass

    assert not errors, f"unexpected errors during concurrent start/stop: {errors[:3]}"


def test_TC_TS_02_stream_while_property_access(device, test_config):
    config = _thread_safety_config(test_config)
    properties = []
    for index in range(device.get_support_property_count()):
        item = device.get_supported_property(index)
        if item.permission == ob.OBPermissionType.PERMISSION_READ_WRITE and (
            item.type == ob.OBPropertyType.OB_INT_PROPERTY
        ):
            properties.append(item.id)
    if not properties:
        pytest.skip("device exposes no writable int properties")

    pipeline = ob.Pipeline(device)
    stop = threading.Event()
    stream_errors = []
    frames = []

    def stream_worker():
        while not stop.is_set():
            try:
                frameset = pipeline.wait_for_frames(1000)
                if frameset is not None:
                    frames.append(frameset)
            except ob.OBError:
                pass
            except Exception as exc:  # noqa: BLE001
                stream_errors.append(exc)

    def property_worker():
        while not stop.is_set():
            for prop in properties:
                try:
                    value = device.get_int_property(prop)
                    device.set_int_property(prop, value)
                except Exception:  # noqa: BLE001
                    pass
            time.sleep(0.05)

    pipeline.start(_depth_config(pipeline))
    workers = [
        threading.Thread(target=stream_worker, daemon=True),
        threading.Thread(target=property_worker, daemon=True),
    ]
    for item in workers:
        item.start()
    try:
        time.sleep(config["duration"])
    finally:
        stop.set()
        for item in workers:
            item.join(timeout=15)
        try:
            pipeline.stop()
        except Exception:  # noqa: BLE001
            pass

    assert not stream_errors, f"streaming failed while properties were touched: {stream_errors[:3]}"
    assert frames, "no frames were delivered while properties were touched"


def test_TC_TS_03_concurrent_pipeline_create_destroy(device, test_config):
    config = _thread_safety_config(test_config)
    stop = threading.Event()
    lock = threading.Lock()
    iterations = []
    errors = []

    def worker():
        local = 0
        while not stop.is_set():
            try:
                pipeline = ob.Pipeline(device)
                pipeline.start(_depth_config(pipeline))
                for _ in range(5):
                    pipeline.wait_for_frames(1000)
                pipeline.stop()
                local += 1
            except ob.OBError:
                pass
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)
            time.sleep(0.1)
        with lock:
            iterations.append(local)

    workers = [
        threading.Thread(target=worker, daemon=True) for _ in range(config["threads"])
    ]
    for item in workers:
        item.start()
    try:
        time.sleep(config["duration"])
    finally:
        stop.set()
        for item in workers:
            item.join(timeout=20)

    assert sum(iterations) > 0
    assert not errors, f"concurrent pipeline churn raised: {errors[:3]}"
