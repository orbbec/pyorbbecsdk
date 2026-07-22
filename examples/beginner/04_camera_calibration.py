# ******************************************************************************
#  pyorbbecsdk Beginner Example 04 — Camera Calibration Parameters
#
#  What you will learn:
#    1. How to start a depth + color stream and wait for the first frame
#    2. How to read intrinsic parameters (fx, fy, cx, cy) for depth and color
#    3. How to read distortion coefficients (k1, k2, k3, p1, p2)
#    4. How to read the extrinsic (rotation + translation) from depth to color
#    5. How to reshape the 9-element rotation vector into a 3×3 matrix
#
#  Calibration parameters explained:
#    Intrinsic  — relates 3D camera-space points to 2D image pixels.
#                 K = [[fx,  0, cx],
#                      [ 0, fy, cy],
#                      [ 0,  0,  1]]
#    Distortion — lens radial/tangential coefficients: (k1 k2 p1 p2 k3).
#    Extrinsic  — rigid transform (R | t) from the depth camera frame to the
#                 color camera frame.  R is a 3×3 rotation; t is in millimeters.
#
#  Typical use cases:
#    - Feed into OpenCV stereoRectify / projectPoints
#    - Build a custom depth-to-color projection without AlignFilter
#    - Export camera model for ROS, Open3D, or COLMAP
#
#  Run:
#    python examples/beginner/04_camera_calibration.py
# ******************************************************************************

import sys

import numpy as np

from pyorbbecsdk import Config, Context, OBError, OBSensorType, Pipeline


def _print_intrinsic(label: str, intr) -> None:
    """Print an OBCameraIntrinsic in a readable block."""
    print(f"  {label}:")
    print(f"    Resolution : {intr.width} × {intr.height}")
    print(f"    fx, fy     : {intr.fx:.4f}, {intr.fy:.4f}")
    print(f"    cx, cy     : {intr.cx:.4f}, {intr.cy:.4f}")


def _print_distortion(label: str, dist) -> None:
    """Print an OBCameraDistortion in a readable block."""
    print(f"  {label}:")
    print(f"    Radial  k1, k2, k3 : {dist.k1:.6f}, {dist.k2:.6f}, {dist.k3:.6f}")
    print(f"    Tangential p1, p2  : {dist.p1:.6f}, {dist.p2:.6f}")


def _print_extrinsic(label: str, ext) -> None:
    """Print an OBExtrinsic (rotation + translation) in a readable block.

    OBExtrinsic.rot       — shape (9,) float32, row-major 3×3 rotation matrix.
    OBExtrinsic.transform — shape (3,) float32, translation in millimeters.
    """
    R = np.array(ext.rot, dtype=np.float64).reshape(3, 3)
    t = np.array(ext.transform, dtype=np.float64)  # mm
    print(f"  {label}:")
    print(f"    Rotation (row-major 3×3):")
    for row in R:
        print(f"      [{row[0]:10.6f}  {row[1]:10.6f}  {row[2]:10.6f}]")
    print(f"    Translation (mm): tx={t[0]:.4f}  ty={t[1]:.4f}  tz={t[2]:.4f}")


def main():
    # Check if device is connected
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        print("Device Not Found! Please connect an Orbbec camera and try again.")
        return

    # --- Step 1: Create pipeline and enable both depth and color streams ---
    #   Calibration parameters are retrieved from OBCameraParam, which
    #   requires both sensors to be active so the SDK can return a matched
    #   depth/color camera pair.
    pipeline = Pipeline()
    config = Config()

    for sensor_type in (OBSensorType.DEPTH_SENSOR, OBSensorType.COLOR_SENSOR):
        try:
            profile_list = pipeline.get_stream_profile_list(sensor_type)
            profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(profile)
            print(f"Enabled {sensor_type.name}: {profile}")
        except OBError as e:
            print(f"WARNING: Could not enable {sensor_type.name}: {e}")

    pipeline.start(config)
    print("\nStreaming — waiting for the first valid frame set …\n")

    # --- Step 2: Wait for the first valid frame set ---
    #   We only need one frame set to obtain calibration data; the pipeline
    #   is stopped immediately afterwards.
    frame_set = None
    for _ in range(30):  # up to ~30 s
        frame_set = pipeline.wait_for_frames(1000)
        if frame_set is not None:
            break

    if frame_set is None:
        print("ERROR: No frames received within 30 seconds.")
        pipeline.stop()
        sys.exit(1)

    # --- Step 3: Retrieve OBCameraParam ---
    #   get_camera_param() returns the matched intrinsic and extrinsic
    #   parameters for the currently active depth/color profile pair.
    #   Call this AFTER the pipeline has started and delivered at least one
    #   frame so the SDK has resolved the active stream profiles.
    cam_param = pipeline.get_camera_param()

    pipeline.stop()

    # --- Step 4: Print depth camera intrinsics ---
    print("=" * 60)
    print("Depth Camera")
    print("=" * 60)
    _print_intrinsic("Intrinsic", cam_param.depth_intrinsic)
    print()
    _print_distortion("Distortion", cam_param.depth_distortion)

    # --- Step 5: Print color camera intrinsics ---
    print()
    print("=" * 60)
    print("Color Camera")
    print("=" * 60)
    _print_intrinsic("Intrinsic", cam_param.rgb_intrinsic)
    print()
    _print_distortion("Distortion", cam_param.rgb_distortion)

    # --- Step 6: Print depth-to-color extrinsic ---
    #   cam_param.transform describes the rigid body transform that maps a
    #   3D point expressed in the depth camera frame into the color camera
    #   frame:  P_color = R · P_depth + t
    print()
    print("=" * 60)
    print("Extrinsic: Depth → Color")
    print("=" * 60)
    _print_extrinsic("R | t", cam_param.transform)

    # --- Step 7: Example — build a numpy camera matrix K ---
    #   This is the standard format expected by OpenCV functions such as
    #   cv2.projectPoints(), cv2.undistort(), and cv2.stereoRectify().
    d = cam_param.depth_intrinsic
    K_depth = np.array(
        [
            [d.fx, 0, d.cx],
            [0, d.fy, d.cy],
            [0, 0, 1],
        ],
        dtype=np.float64,
    )

    c = cam_param.rgb_intrinsic
    K_color = np.array(
        [
            [c.fx, 0, c.cx],
            [0, c.fy, c.cy],
            [0, 0, 1],
        ],
        dtype=np.float64,
    )

    print()
    print("=" * 60)
    print("OpenCV-style Camera Matrices (numpy)")
    print("=" * 60)
    print("  K_depth =")
    for row in K_depth:
        print(f"    {row}")
    print("  K_color =")
    for row in K_color:
        print(f"    {row}")

    print("\nDone.")


if __name__ == "__main__":
    main()
