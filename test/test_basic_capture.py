#!/usr/bin/env python3
"""
test_capture.py - Frame capture test for pyorbbecsdk on macOS

This test verifies that pyorbbecsdk can capture frames from an Orbbec camera.

Usage:
    python tests/test_capture.py

Note: Requires an Orbbec camera to be connected for full testing.
"""

import sys
import time


def test_pipeline_creation():
    """Test creating a Pipeline object"""
    print("=" * 50)
    print("Pipeline Creation Test")
    print("=" * 50)

    try:
        import pyorbbecsdk
        from pyorbbecsdk import OBFormat, OBSensorType

        ctx = pyorbbecsdk.Context()
        pipeline = pyorbbecsdk.Pipeline()

        print(f"✓ Pipeline created successfully")
        print(f"  Pipeline object: {pipeline}")

        return ctx, pipeline
    except Exception as e:
        print(f"✗ Pipeline creation failed: {e}")
        return None, None


def test_config_creation(ctx, pipeline):
    """Test creating and configuring a Config object"""
    print()
    print("=" * 50)
    print("Configuration Test")
    print("=" * 50)

    if pipeline is None:
        print("✗ Skipped (no pipeline)")
        return None

    try:
        import pyorbbecsdk
        from pyorbbecsdk import OBFormat, OBSensorType

        config = pyorbbecsdk.Config()
        print(f"✓ Config created successfully")

        # Try to enable streams (may fail without device)
        try:
            profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(profile)
            print(f"✓ Color stream configured")
        except Exception as e:
            print(f"  Color stream config skipped: {type(e).__name__}")

        try:
            profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            profile = profile_list.get_default_video_stream_profile()
            config.enable_stream(profile)
            print(f"✓ Depth stream configured")
        except Exception as e:
            print(f"  Depth stream config skipped: {type(e).__name__}")

        return config
    except Exception as e:
        print(f"✗ Config creation failed: {e}")
        return None


def test_pipeline_start(ctx, pipeline, config):
    """Test starting the pipeline"""
    print()
    print("=" * 50)
    print("Pipeline Start Test")
    print("=" * 50)

    if pipeline is None:
        print("✗ Skipped (no pipeline)")
        return False

    try:
        if config:
            pipeline.start(config)
        else:
            pipeline.start()

        print(f"✓ Pipeline started successfully")
        return True
    except Exception as e:
        print(f"  Pipeline start skipped (no device): {type(e).__name__}")
        return False


def test_frame_capture(pipeline, duration=3):
    """Test capturing frames"""
    print()
    print("=" * 50)
    print("Frame Capture Test")
    print("=" * 50)

    if pipeline is None:
        print("✗ Skipped (no pipeline)")
        return False

    try:
        print(f"  Capturing frames for {duration} seconds...")

        frame_count = 0
        start_time = time.time()

        while time.time() - start_time < duration:
            try:
                frames = pipeline.wait_for_frames(1000)
                if frames:
                    frame_count += 1

                    # Try to get color frame
                    try:
                        color_frame = frames.get_color_frame()
                        if color_frame:
                            width = color_frame.get_width()
                            height = color_frame.get_height()
                            print(f"  Frame {frame_count}: Color {width}x{height}")
                    except:
                        pass

                    # Try to get depth frame
                    try:
                        depth_frame = frames.get_depth_frame()
                        if depth_frame:
                            width = depth_frame.get_width()
                            height = depth_frame.get_height()
                            print(f"  Frame {frame_count}: Depth {width}x{height}")
                    except:
                        pass
            except Exception as e:
                # Timeout is OK, just continue
                pass

        print(f"✓ Captured {frame_count} frames")
        return True
    except Exception as e:
        print(f"✗ Frame capture failed: {e}")
        return False


def test_pipeline_stop(pipeline):
    """Test stopping the pipeline"""
    print()
    print("=" * 50)
    print("Pipeline Stop Test")
    print("=" * 50)

    if pipeline is None:
        print("✗ Skipped (no pipeline)")
        return True

    try:
        pipeline.stop()
        print(f"✓ Pipeline stopped successfully")
        return True
    except Exception as e:
        print(f"✗ Pipeline stop failed: {e}")
        return False


def test_cleanup(ctx, pipeline):
    """Test proper cleanup"""
    print()
    print("=" * 50)
    print("Cleanup Test")
    print("=" * 50)

    try:
        if pipeline:
            del pipeline
        if ctx:
            del ctx
        print("✓ Cleanup completed")
        return True
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
        return False


def main():
    """Run all tests"""
    print()
    print("╔" + "=" * 48 + "╗")
    print("║  pyorbbecsdk macOS Capture Test Suite       ║")
    print("╚" + "=" * 48 + "╝")
    print()

    results = []

    # Test pipeline creation
    ctx, pipeline = test_pipeline_creation()
    results.append(("Pipeline Creation", pipeline is not None))

    # Test config creation
    config = test_config_creation(ctx, pipeline)
    results.append(("Configuration", config is not None))

    # Test pipeline start
    start_success = test_pipeline_start(ctx, pipeline, config)
    results.append(("Pipeline Start", start_success))

    # Test frame capture
    capture_success = False
    if start_success:
        capture_success = test_frame_capture(pipeline)
    results.append(("Frame Capture", capture_success))

    # Test pipeline stop
    stop_success = test_pipeline_stop(pipeline)
    results.append(("Pipeline Stop", stop_success))

    # Test cleanup
    cleanup_success = test_cleanup(ctx, pipeline)
    results.append(("Cleanup", cleanup_success))

    # Summary
    print()
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        print("\nNote: Some tests may fail if no camera is connected.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
