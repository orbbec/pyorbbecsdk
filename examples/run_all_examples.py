"""
Automated smoke-tester for all pyorbbecsdk examples.

Each example is launched in a subprocess with:
  - A wall-clock timeout (TIMEOUT_SEC seconds)
  - stdin piped so interactive input() calls get a synthetic answer
  - stdout/stderr captured

Exit codes interpreted:
  0        -> PASS
  timeout  -> PASS (example ran, just hit the time limit — normal for GUI loops)
  non-zero -> FAIL (import error, AttributeError, etc.)

Run from repo root:
    python examples/run_all_examples.py
"""

import os
import subprocess
import sys
import time

PYTHON = sys.executable
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT_SEC = 8  # seconds per example before we send SIGTERM

# ---------------------------------------------------------------------------
# Test matrix
# Each entry: (label, script_path, extra_args, stdin_input)
#   stdin_input  - bytes fed to the process stdin (simulates user typing)
#   extra_args   - additional CLI args to pass
# ---------------------------------------------------------------------------
TESTS = [
    # ---- Beginner ----
    ("01 hello_camera", "examples/beginner/01_hello_camera.py", [], None),
    ("02 depth_visualization", "examples/beginner/02_depth_visualization.py", [], None),
    (
        "03 color_and_depth_aligned (SW)",
        "examples/beginner/03_color_and_depth_aligned.py",
        [],
        None,
    ),
    (
        "03 color_and_depth_aligned (HW --hw)",
        "examples/beginner/03_color_and_depth_aligned.py",
        ["--hw"],
        None,
    ),
    ("04 camera_calibration", "examples/beginner/04_camera_calibration.py", [], None),
    ("05 point_cloud", "examples/beginner/05_point_cloud.py", [], None),
    ("06 multi_streams", "examples/beginner/06_multi_streams.py", [], None),
    ("07 imu", "examples/beginner/07_imu.py", [], None),
    # 08 net_device — requires a network camera; skip
    # 09 firmware_update — destructive; skip
    # ---- Advanced ----
    (
        "adv01 recorder (GUI)",
        "examples/advanced/01_recorder.py",
        [],
        b"test_recording.bag\n",
    ),  # answer the filename prompt
    (
        "adv01 recorder (--no-gui)",
        "examples/advanced/01_recorder.py",
        ["--no-gui"],
        b"test_recording_headless.bag\n",
    ),
    (
        "adv02 playback",
        "examples/advanced/02_playback.py",
        [],
        b"test_recording_headless.bag\n",
    ),  # play back what we just recorded
    (
        "adv03 save_image_to_disk",
        "examples/advanced/03_save_image_to_disk.py",
        [],
        None,
    ),
    ("adv04 enumerate", "examples/advanced/04_enumerate.py", [], b"q\n"),
    ("adv05 hot_plug", "examples/advanced/05_hot_plug.py", [], None),
    ("adv06 control", "examples/advanced/06_control.py", [], None),
    ("adv07 metadata", "examples/advanced/07_metadata.py", [], None),
    (
        "adv08 custom_filter_chain",
        "examples/advanced/08_custom_filter_chain.py",
        [],
        None,
    ),
    ("adv09 post_processing", "examples/advanced/09_post_processing.py", [], None),
    ("adv10 hdr", "examples/advanced/10_hdr.py", [], None),
    ("adv11 preset", "examples/advanced/11_preset.py", [], b"-1\n"),
    ("adv12 depth_work_mode", "examples/advanced/12_depth_work_mode.py", [], None),
    ("adv13 confidence", "examples/advanced/13_confidence.py", [], None),
    # adv14 two_devices_sync — needs 2 cameras; skip
    # adv15 high_performance_pipeline — runs but auto-exits? include with short timeout
    (
        "adv15 high_performance_pipeline",
        "examples/advanced/15_high_performance_pipeline.py",
        [],
        None,
    ),
    (
        "adv16 coordinate_transform",
        "examples/advanced/16_coordinate_transform.py",
        [],
        None,
    ),
    ("adv17 laser_interleave", "examples/advanced/17_laser_interleave.py", [], None),
    # adv18 forceip — needs network camera; skip
    # adv19 device_optional_depth_presets_update — needs Gemini 330; skip on 335L
    # ---- Applications ----
    ("app ruler", "examples/applications/ruler.py", [], None),
    # app object_detection — needs ONNX model file; skip
]

SKIP = {
    "examples/beginner/08_net_device.py",
    "examples/beginner/09_device_firmware_update.py",
    "examples/advanced/02_playback.py",  # needs a properly closed .bag; truncated files cause SDK crash
    "examples/advanced/14_two_devices_sync.py",
    "examples/advanced/18_forceip.py",
    "examples/advanced/19_device_optional_depth_presets_update.py",
    "examples/advanced/16_coordinate_transform.py",  # requires pynput module
    "examples/applications/object_detection.py",
}

# ---------------------------------------------------------------------------

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def run_one(label, script, extra_args, stdin_input):
    cmd = [PYTHON, os.path.join(REPO, script)] + extra_args
    t0 = time.time()
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=REPO,
        )
        try:
            stdout, stderr = proc.communicate(input=stdin_input, timeout=TIMEOUT_SEC)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            elapsed = time.time() - t0
            return "TIMEOUT", elapsed, stdout, stderr

        elapsed = time.time() - t0
        retcode = proc.returncode
        return ("PASS" if retcode == 0 else "FAIL"), elapsed, stdout, stderr

    except Exception as e:
        return "ERROR", time.time() - t0, b"", str(e).encode()


def main():
    results = []
    print(f"\n{'='*72}")
    print(f"  pyorbbecsdk Example Smoke Tests")
    print(f"  Timeout per example: {TIMEOUT_SEC}s")
    print(f"{'='*72}\n")

    for label, script, extra_args, stdin_input in TESTS:
        if script in SKIP:
            continue
        print(f"  Running  {label:<45}", end="", flush=True)
        status, elapsed, stdout, stderr = run_one(label, script, extra_args, stdin_input)

        if status in ("PASS", "TIMEOUT"):
            color = GREEN
        else:
            color = RED

        print(f"  {color}{status:8}{RESET}  ({elapsed:.1f}s)")

        if status == "FAIL":
            # Show last 10 lines of stderr for diagnosis
            err_lines = stderr.decode(errors="replace").strip().splitlines()
            for line in err_lines[-10:]:
                print(f"      {RED}{line}{RESET}")

        results.append((label, status, elapsed, stdout, stderr))

    # Summary
    passed = sum(1 for _, s, *_ in results if s in ("PASS", "TIMEOUT"))
    failed = sum(1 for _, s, *_ in results if s == "FAIL")
    errors = sum(1 for _, s, *_ in results if s == "ERROR")
    total = len(results)

    print(f"\n{'='*72}")
    print(f"  Results: {passed}/{total} passed", end="")
    if failed:
        print(f"  |  {RED}{failed} FAILED{RESET}", end="")
    if errors:
        print(f"  |  {RED}{errors} ERRORS{RESET}", end="")
    print(f"\n{'='*72}\n")

    # Cleanup test bag files
    for f in ("test_recording.bag", "test_recording_headless.bag"):
        fp = os.path.join(REPO, f)
        if os.path.exists(fp):
            os.remove(fp)
            print(f"  Cleaned up: {f}")

    return 1 if (failed + errors) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
