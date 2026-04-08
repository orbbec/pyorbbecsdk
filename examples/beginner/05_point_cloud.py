# ******************************************************************************
#  pyorbbecsdk Beginner Example 05 — 3D Point Cloud
#
#  What you will learn:
#    1. How to enable PointCloudFilter to generate a 3D point cloud
#    2. How to use AlignFilter to get a colored point cloud (RGB + XYZ)
#    3. How to save the point cloud to a .ply file for visualization
#    4. How to render the point cloud in real-time using Open3D
#
#  Keyboard shortcuts (in the Open3D window):
#    C         — toggle between RGB colour / depth-coloured rendering
#    S         — save current point cloud to .ply
#    Q / ESC   — quit
#    Mouse     — rotate / pan / zoom
#
#  Device requirement: All
#
#  Run:
#    python examples/beginner/05_point_cloud.py
# ******************************************************************************

import os

import numpy as np

from pyorbbecsdk import OBError  # type: ignore
from pyorbbecsdk import (
    AlignFilter,
    Config,
    Context,
    OBFormat,
    OBSensorType,
    OBStreamType,
    Pipeline,
    PointCloudFilter,
    save_point_cloud_to_ply,
)

# --- Optional Open3D import ---
try:
    import open3d as o3d

    HAS_OPEN3D = True
except ImportError:
    HAS_OPEN3D = False
    print("[WARN] open3d not installed. Install with:  pip install open3d")
    print("       Falling back to save-only mode (no live rendering).\n")

SAVE_DIR = os.path.join(os.getcwd(), "point_clouds")
os.makedirs(SAVE_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Point cloud data extraction helpers
# ---------------------------------------------------------------------------


def _extract_xyz(points_frame):
    """Extract Nx3 float32 positions from a POINT-format PointsFrame."""
    data = np.frombuffer(points_frame.get_data(), dtype=np.float32)
    n = data.size // 3
    return data.reshape(n, 3)


def _extract_xyz_rgb(points_frame):
    """Extract Nx3 positions and Nx3 colours from an RGB_POINT-format PointsFrame."""
    # OBColorPoint: float x, y, z, r, g, b  (6 × float32 = 24 bytes per point)
    data = np.frombuffer(points_frame.get_data(), dtype=np.float32)
    n = data.size // 6
    data = data.reshape(n, 6)
    xyz = data[:, 0:3]
    rgb = data[:, 3:6] / 255.0  # SDK stores 0-255 as float → normalise
    rgb = np.clip(rgb, 0.0, 1.0)
    return xyz, rgb


def _depth_colormap(z_values):
    """Map Z depth (mm) to a rainbow colour (red=near, blue=far)."""
    valid = z_values[z_values > 0]
    if valid.size == 0:
        return np.zeros((z_values.shape[0], 3))
    z_min, z_max = valid.min(), valid.max()
    span = z_max - z_min
    if span < 1e-3:
        span = 1.0
    # Normalise 0–1
    t = np.clip((z_values - z_min) / span, 0.0, 1.0)
    # HSV-style rainbow: hue goes 0 (red/near) → 0.66 (blue/far)
    hue = t * 0.66
    r = np.clip(np.abs(hue * 6.0 - 3.0) - 1.0, 0, 1)
    g = np.clip(2.0 - np.abs(hue * 6.0 - 2.0), 0, 1)
    b = np.clip(2.0 - np.abs(hue * 6.0 - 4.0), 0, 1)
    colors = np.stack([r, g, b], axis=1)
    # Mark z==0 (invalid) as dark grey
    colors[z_values <= 0] = [0.15, 0.15, 0.15]
    return colors


# ---------------------------------------------------------------------------
# Scene helper: grid floor + camera frustum + axis
# ---------------------------------------------------------------------------


def _create_3d_grid(x_range=(-1500, 1500), y_range=(-1000, 1000), z_range=(-500, 3000), step_mm=500):
    """
    Create a corner-style 3-plane grid (like a room corner):
      - Floor    (XZ plane at Y = y_max, i.e. below)
      - Back wall (XY plane at Z = z_max, i.e. far end)
      - Right wall (YZ plane at X = x_max, i.e. right side)

    The three planes meet at a right-angle corner ahead of the camera.
    The camera (at origin) sits roughly at the centre of the grid volume,
    looking towards the corner.
    All values in mm.
    """
    points, lines, colors = [], [], []
    idx = 0

    xs = np.arange(x_range[0], x_range[1] + step_mm * 0.5, step_mm)
    ys = np.arange(y_range[0], y_range[1] + step_mm * 0.5, step_mm)
    zs = np.arange(z_range[0], z_range[1] + step_mm * 0.5, step_mm)

    x0, x1 = x_range
    y0, y1 = y_range
    z0, z1 = z_range

    c_floor = [0.25, 0.25, 0.30]  # slightly blue-ish
    c_back = [0.25, 0.30, 0.25]  # slightly green-ish
    c_right = [0.30, 0.25, 0.25]  # slightly red-ish
    c_edge = [0.45, 0.45, 0.45]  # brighter for the 3 shared edges

    def _add(p0, p1, c):
        nonlocal idx
        points.append(p0)
        points.append(p1)
        lines.append([idx, idx + 1])
        idx += 2
        colors.append(c)

    # ── Floor (XZ plane, Y = y1) ──
    for x in xs:  # lines ∥ Z
        _add([x, y1, z0], [x, y1, z1], c_floor)
    for z in zs:  # lines ∥ X
        _add([x0, y1, z], [x1, y1, z], c_floor)

    # ── Back wall (XY plane, Z = z1) ──
    for x in xs:  # lines ∥ Y
        _add([x, y0, z1], [x, y1, z1], c_back)
    for y in ys:  # lines ∥ X
        _add([x0, y, z1], [x1, y, z1], c_back)

    # ── Right wall (YZ plane, X = x1) ──
    for y in ys:  # lines ∥ Z
        _add([x1, y, z0], [x1, y, z1], c_right)
    for z in zs:  # lines ∥ Y
        _add([x1, y0, z], [x1, y1, z], c_right)

    # ── Highlight the 3 shared corner edges ──
    _add([x1, y1, z0], [x1, y1, z1], c_edge)  # floor ∩ right (∥ Z)
    _add([x1, y0, z1], [x1, y1, z1], c_edge)  # right ∩ back  (∥ Y)
    _add([x0, y1, z1], [x1, y1, z1], c_edge)  # floor ∩ back  (∥ X)

    ls = o3d.geometry.LineSet()
    ls.points = o3d.utility.Vector3dVector(np.array(points))
    ls.lines = o3d.utility.Vector2iVector(np.array(lines))
    ls.colors = o3d.utility.Vector3dVector(np.array(colors))
    return ls


def _create_depth_ticks(z_range=(0, 3000), step_mm=500, x_offset=1050):
    """
    Create small '+' shaped tick marks along the Z axis with depth labels.
    Returns a LineSet for the tick geometry (text labels are not supported
    in the non-blocking Visualizer, but the ticks still convey spacing).
    """
    points, lines = [], []
    idx = 0
    tick_half = 30  # mm half-length of a tick mark
    for z in np.arange(z_range[0], z_range[1] + step_mm * 0.5, step_mm):
        # Horizontal tick on the right edge
        points.append([x_offset - tick_half, 0, z])
        points.append([x_offset + tick_half, 0, z])
        lines.append([idx, idx + 1])
        idx += 2
        # Vertical tick
        points.append([x_offset, -tick_half, z])
        points.append([x_offset, tick_half, z])
        lines.append([idx, idx + 1])
        idx += 2
    ls = o3d.geometry.LineSet()
    ls.points = o3d.utility.Vector3dVector(np.array(points))
    ls.lines = o3d.utility.Vector2iVector(np.array(lines))
    ls.paint_uniform_color([0.55, 0.55, 0.3])  # yellowish
    return ls


def _create_camera_marker():
    """
    Create a small camera frustum wireframe at the origin, indicating where the
    camera is located. The frustum opens along +Z (the camera looks at +Z).
    All units in mm.
    """
    # Camera body as a simple pyramid frustum
    fw, fh, fd = 60, 40, 80  # frustum half-width, half-height, depth (mm)
    pts = [
        [0, 0, 0],  # 0  camera centre (origin)
        [-fw, -fh, fd],  # 1  top-left  (far plane)
        [fw, -fh, fd],  # 2  top-right
        [fw, fh, fd],  # 3  bottom-right
        [-fw, fh, fd],  # 4  bottom-left
    ]
    edges = [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],  # rays from origin → corners
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 1],  # far-plane rectangle
    ]
    ls = o3d.geometry.LineSet()
    ls.points = o3d.utility.Vector3dVector(np.array(pts, dtype=np.float64))
    ls.lines = o3d.utility.Vector2iVector(np.array(edges))
    ls.paint_uniform_color([0.0, 1.0, 0.0])  # green
    return ls


def _create_origin_axes(length_mm=300):
    """Create XYZ axis lines at the camera origin (R=X, G=Y, B=Z) in mm."""
    pts = [
        [0, 0, 0],
        [length_mm, 0, 0],
        [0, 0, 0],
        [0, length_mm, 0],
        [0, 0, 0],
        [0, 0, length_mm],
    ]
    edges = [[0, 1], [2, 3], [4, 5]]
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ls = o3d.geometry.LineSet()
    ls.points = o3d.utility.Vector3dVector(np.array(pts, dtype=np.float64))
    ls.lines = o3d.utility.Vector2iVector(np.array(edges))
    ls.colors = o3d.utility.Vector3dVector(np.array(colors, dtype=np.float64))
    return ls


# ---------------------------------------------------------------------------
# Open3D real-time visualiser
# ---------------------------------------------------------------------------


class PointCloudVisualizer:
    """Non-blocking Open3D point cloud viewer refreshed every frame."""

    # Colour modes
    MODE_RGB = 0
    MODE_DEPTH = 1
    MODE_NAMES = {MODE_RGB: "RGB Colour", MODE_DEPTH: "Depth Colourmap"}

    def __init__(self, window_name="Orbbec Point Cloud", width=1280, height=720):
        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window(window_name=window_name, width=width, height=height)

        # Register key callbacks
        self.vis.register_key_callback(ord("C"), self._on_toggle_color)
        self.vis.register_key_callback(ord("S"), self._on_save)

        # Render options
        opt = self.vis.get_render_option()
        opt.background_color = np.array([0.1, 0.1, 0.1])
        opt.point_size = 2.0

        self.pcd = o3d.geometry.PointCloud()
        self._geometry_added = False
        self._frame_count = 0

        # Colour mode state
        self._color_mode = self.MODE_RGB
        self._last_xyz = None
        self._last_rgb = None
        self._save_requested = False

        # Create scene reference geometry (3D grid, depth ticks, camera marker, axes)
        self._grid = _create_3d_grid(
            x_range=(-1500, 1500),
            y_range=(-1000, 1000),
            z_range=(-500, 3000),
            step_mm=500,
        )
        self._ticks = _create_depth_ticks(z_range=(-500, 3000), step_mm=500, x_offset=1550)
        self._camera = _create_camera_marker()
        self._axes = _create_origin_axes(length_mm=300)

    # --- Key callbacks ---
    def _on_toggle_color(self, vis):
        if self._color_mode == self.MODE_RGB:
            self._color_mode = self.MODE_DEPTH
        else:
            self._color_mode = self.MODE_RGB
        print(f"[Viewer] Colour mode → {self.MODE_NAMES[self._color_mode]}")
        # Re-apply colour immediately
        if self._last_xyz is not None:
            self._apply_colors()
            self.vis.update_geometry(self.pcd)
        return False

    def _on_save(self, vis):
        self._save_requested = True
        return False

    @property
    def save_requested(self):
        """Check and reset the save flag (set by 'S' key)."""
        if self._save_requested:
            self._save_requested = False
            return True
        return False

    # --- Colour application ---
    def _apply_colors(self):
        xyz = self._last_xyz
        rgb = self._last_rgb
        if self._color_mode == self.MODE_RGB and rgb is not None:
            self.pcd.colors = o3d.utility.Vector3dVector(rgb.astype(np.float64))
        else:
            # Depth colourmap based on Z
            cmap = _depth_colormap(xyz[:, 2])
            self.pcd.colors = o3d.utility.Vector3dVector(cmap.astype(np.float64))

    def update(self, xyz, rgb=None):
        """Push a new set of points (and optional colours) to the viewer."""
        # Filter out invalid (0,0,0) points
        mask = ~np.all(xyz == 0, axis=1)
        xyz = xyz[mask]
        if rgb is not None:
            rgb = rgb[mask]

        if xyz.shape[0] == 0:
            return True

        # Keep coordinates in mm (no scaling)
        self._last_xyz = xyz
        self._last_rgb = rgb

        self.pcd.points = o3d.utility.Vector3dVector(xyz.astype(np.float64))
        self._apply_colors()

        if not self._geometry_added:
            self.vis.add_geometry(self.pcd)
            self.vis.add_geometry(self._grid)
            self.vis.add_geometry(self._ticks)
            self.vis.add_geometry(self._camera)
            self.vis.add_geometry(self._axes)
            self._geometry_added = True
            # Set a nice initial viewpoint — slightly above and to the side
            ctr = self.vis.get_view_control()
            # Camera at centre, looking towards the corner (right-below-far)
            ctr.set_front([-0.3, -0.3, -0.9])
            ctr.set_up([0, -1, 0])
            ctr.set_lookat([500, 300, 1250])  # centre of corner region
            ctr.set_zoom(0.25)
        else:
            self.vis.update_geometry(self.pcd)

        self._frame_count += 1
        alive = self.vis.poll_events()
        self.vis.update_renderer()
        return alive

    def destroy(self):
        self.vis.destroy_window()


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

    # ----- Configure depth stream -----
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is None:
        print("No proper depth profile, cannot generate point cloud")
        return
    depth_profile = depth_profile_list.get_default_video_stream_profile()
    config.enable_stream(depth_profile)

    # ----- Configure colour stream (optional) -----
    has_color_sensor = False
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
            has_color_sensor = True
    except OBError as e:
        print(f"[INFO] Color sensor unavailable: {e}")

    try:
        pipeline.enable_frame_sync()
        pipeline.start(config)
    except OBError as e:
        print(f"Error: {e}")
        print("Please connect an Orbbec camera and try again.")
        return

    # ----- Build filter pipeline -----
    align_filter = AlignFilter(align_to_stream=OBStreamType.COLOR_STREAM)
    point_cloud_filter = PointCloudFilter()

    point_format = OBFormat.RGB_POINT if has_color_sensor else OBFormat.POINT
    point_cloud_filter.set_create_point_format(point_format)

    # ----- Setup viewer -----
    viewer = None
    if HAS_OPEN3D:
        viewer = PointCloudVisualizer()
        mode_str = "RGB + Depth" if has_color_sensor else "Depth only"
        print("=== Open3D Point Cloud Viewer ===")
        print(f"  Colour sensor : {'YES' if has_color_sensor else 'NO'} ({mode_str})")
        print(f"  Depth unit    : mm")
        print()
        print("  C     — toggle RGB colour / depth colourmap")
        print("  S     — save point cloud to .ply")
        print("  Q/ESC — quit")
        print("  Mouse — rotate / pan / zoom")
        print()

    save_index = 0
    running = True

    try:
        while running:
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue

            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                continue

            color_frame = frames.get_color_frame()
            if has_color_sensor and color_frame is None:
                continue

            # Align colour → depth
            aligned = align_filter.process(frames)

            # Generate point cloud
            point_cloud_frame = point_cloud_filter.process(aligned)
            if point_cloud_frame is None:
                continue

            # Extract numpy arrays
            if has_color_sensor and color_frame is not None:
                xyz, rgb = _extract_xyz_rgb(point_cloud_frame.as_points_frame())
            else:
                xyz = _extract_xyz(point_cloud_frame.as_points_frame())
                rgb = None

            # ----- Render -----
            if viewer is not None:
                alive = viewer.update(xyz, rgb)
                if not alive:
                    break
                # Handle save request from 'S' key
                if viewer.save_requested:
                    ply_path = os.path.join(SAVE_DIR, f"point_cloud_{save_index:04d}.ply")
                    save_point_cloud_to_ply(ply_path, point_cloud_frame)
                    save_index += 1
                    print(f"[Saved] {ply_path}")
            else:
                # No Open3D — save one frame and exit
                ply_path = os.path.join(SAVE_DIR, "point_cloud.ply")
                save_point_cloud_to_ply(ply_path, point_cloud_frame)
                print(f"Saved point cloud to {ply_path}")
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    # Cleanup
    if viewer is not None:
        viewer.destroy()
    pipeline.stop()
    print("Done.")


if __name__ == "__main__":
    main()
