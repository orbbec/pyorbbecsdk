#!/usr/bin/env python3
# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
# ******************************************************************************
"""
One-click test runner for pyorbbecsdk.

Auto-detects the connected device (or accepts a device name via --device),
then runs the matching test suite.  Results are saved as an HTML report.

Usage
-----
  # Auto-detect connected camera and run all its tests
  python test/run_tests.py

  # Specify device family explicitly
  python test/run_tests.py --device g300
  python test/run_tests.py --device femto
  python test/run_tests.py --device astra_mini
  python test/run_tests.py --device astra2

  # Filter by test category
  python test/run_tests.py --category functional
  python test/run_tests.py --category performance
  python test/run_tests.py --category stability

  # Combine: G300 functional tests only
  python test/run_tests.py --device g300 --category functional

  # Run without a camera (non-hardware tests only)
  python test/run_tests.py --no-hardware

  # Skip long performance benchmarks
  python test/run_tests.py --quick

  # Save report to a custom directory
  python test/run_tests.py --output my_reports/

Device aliases accepted by --device
------------------------------------
  g300, gemini, gemini330, gemini335, gemini336, gemini305, gemini345
  femto, femto_bolt, femto_mega
  astra_mini, astra_mini_pro
  astra2, astra_2

Category markers
-----------------
  functional   — basic API correctness (device info, stream start, controls)
  performance  — timing-sensitive benchmarks (FPS, latency, throughput)
  stability    — multi-frame / long-running reliability (timestamps, sync, drop rate)
"""

import argparse
import datetime
import os
import platform
import subprocess
import sys

# ---------------------------------------------------------------------------
# Device family detection
# ---------------------------------------------------------------------------

#: Maps the canonical marker name to name substrings found in device_info.get_name()
_DEVICE_NAME_PATTERNS = {
    "g300_series": [
        "Gemini 330",
        "Gemini 335",
        "Gemini 336",
        "Gemini 305",
        "Gemini 345",
        "Gemini345",
        "Gemini305",
    ],
    "femto": ["Femto Bolt", "Femto Mega", "FemtoBolt", "FemtoMega"],
    "astra_mini": ["Astra Mini", "Astra mini"],
    "astra2": ["Astra 2", "Astra2"],
}

#: User-friendly aliases accepted by --device
_DEVICE_ALIASES = {
    # G300 series
    "g300": "g300_series",
    "gemini": "g300_series",
    "gemini330": "g300_series",
    "gemini335": "g300_series",
    "gemini336": "g300_series",
    "gemini305": "g300_series",
    "gemini345": "g300_series",
    "g300_series": "g300_series",
    # Femto
    "femto": "femto",
    "femto_bolt": "femto",
    "femto_mega": "femto",
    # Astra Mini
    "astra_mini": "astra_mini",
    "astra_mini_pro": "astra_mini",
    # Astra 2
    "astra2": "astra2",
    "astra_2": "astra2",
}

#: Human-readable device family names
_DEVICE_DISPLAY = {
    "g300_series": "G300 Series (Gemini 330/335/336/305/345)",
    "femto": "Femto Bolt / Femto Mega",
    "astra_mini": "Astra Mini Pro / S Pro",
    "astra2": "Astra 2",
}


def detect_connected_device():
    """
    Query the first connected Orbbec device and return
    (marker_name, device_display_name, serial, firmware).
    Returns (None, raw_name, serial, firmware) if no pattern matches.
    Returns (None, None, None, None) if no device is connected.
    """
    try:
        from pyorbbecsdk import Context, OBLogLevel

        ctx = Context()
        ctx.set_logger_level(OBLogLevel.NONE)
        device_list = ctx.query_devices()
        if device_list.get_count() == 0:
            return None, None, None, None
        dev = device_list.get_device_by_index(0)
        di = dev.get_device_info()
        raw_name = di.get_name() or ""
        serial = di.get_serial_number() or "N/A"
        firmware = di.get_firmware_version() or "N/A"

        for marker, patterns in _DEVICE_NAME_PATTERNS.items():
            if any(p in raw_name for p in patterns):
                return marker, raw_name, serial, firmware

        return None, raw_name, serial, firmware
    except Exception as exc:
        print(f"[warn] Could not query device: {exc}")
        return None, None, None, None


# ---------------------------------------------------------------------------
# pytest argument construction
# ---------------------------------------------------------------------------


def build_markers(device_marker, category, no_hardware, quick):
    """
    Return a list of marker expressions to combine with AND logic.

    Category → pytest markers mapping:
      functional  → functional
      performance → performance
      stability   → stability
      (none)      → (all tests for the device family)
    """
    parts = []

    if no_hardware:
        parts.append("not hardware")
    elif device_marker:
        parts.append(device_marker)

    if quick:
        parts.append("not performance")

    if category:
        parts.append(category)

    return parts


def build_pytest_cmd(
    test_dir,
    report_path,
    device_marker,
    category,
    no_hardware,
    quick,
    sdk_version,
    device_name,
    serial,
    firmware,
):
    """Return the full pytest command as a list of strings."""
    marker_parts = build_markers(device_marker, category, no_hardware, quick)

    args = [sys.executable, "-m", "pytest", test_dir, "-v", "--tb=short"]

    if marker_parts:
        combined = " and ".join(f"({p})" for p in marker_parts)
        args += ["-m", combined]

    # HTML report (requires pytest-html)
    args += [
        f"--html={report_path}",
        "--self-contained-html",
        "--metadata",
        "SDK Version",
        sdk_version,
        "--metadata",
        "Device",
        device_name,
        "--metadata",
        "Serial",
        serial,
        "--metadata",
        "Firmware",
        firmware,
        "--metadata",
        "OS",
        f"{platform.system()} {platform.release()}",
        "--metadata",
        "Python",
        sys.version.split()[0],
    ]

    # Add timeout only if pytest-timeout is installed
    if not quick and not no_hardware:
        try:
            import subprocess

            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
            )
            if "timeout" in result.stdout.lower() or "timeout" in result.stderr.lower():
                args += ["--timeout=120"]
        except Exception:
            pass

    return args


# ---------------------------------------------------------------------------
# SDK version detection
# ---------------------------------------------------------------------------


def get_sdk_version():
    try:
        import importlib.metadata

        return importlib.metadata.version("pyorbbecsdk2")
    except Exception:
        pass
    try:
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(here, "setup.py")) as f:
            for line in f:
                if "version=" in line and "'" in line:
                    return line.split("'")[1]
    except Exception:
        pass
    return "unknown"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="pyorbbecsdk one-click test runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test/run_tests.py                          # auto-detect + run all
  python test/run_tests.py --device g300            # G300 series only
  python test/run_tests.py --device femto --quick   # Femto, skip benchmarks
  python test/run_tests.py --category functional    # functional tests only
  python test/run_tests.py --no-hardware            # no camera needed
""",
    )
    parser.add_argument(
        "--device",
        metavar="NAME",
        help=(
            "Device family to test. Auto-detected if omitted. "
            "Accepted values: g300, gemini, gemini335, femto, femto_bolt, "
            "femto_mega, astra_mini, astra2 (and their variants)"
        ),
    )
    parser.add_argument(
        "--category",
        metavar="CAT",
        choices=["functional", "performance", "stability"],
        help="Run only tests in this category (functional / performance / stability)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip performance benchmark tests (marker: not performance)",
    )
    parser.add_argument(
        "--no-hardware",
        action="store_true",
        help="Skip all hardware-dependent tests (no camera required)",
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        default="reports",
        help="Directory for HTML report output (default: reports/)",
    )
    parser.add_argument(
        "--sdk-version",
        metavar="V",
        help="Override SDK version string shown in report",
    )
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(repo_root, args.output)
    os.makedirs(output_dir, exist_ok=True)

    sdk_version = args.sdk_version or get_sdk_version()

    # ---- Resolve device marker ----
    device_marker = None
    device_name = "N/A"
    serial = "N/A"
    firmware = "N/A"

    if args.no_hardware:
        device_name = "N/A (--no-hardware)"
    elif args.device:
        alias = args.device.lower().replace("-", "_")
        if alias not in _DEVICE_ALIASES:
            print(f"[error] Unknown device alias '{args.device}'.")
            print(f"  Accepted values: {', '.join(sorted(_DEVICE_ALIASES))}")
            return 2
        device_marker = _DEVICE_ALIASES[alias]
        device_name = _DEVICE_DISPLAY.get(device_marker, device_marker)
        # Still try to get serial/firmware from connected device
        _, raw_name, serial, firmware = detect_connected_device()
        if raw_name:
            device_name = raw_name
    else:
        # Auto-detect
        print("Auto-detecting connected device …")
        device_marker, device_name, serial, firmware = detect_connected_device()
        if device_name is None:
            print("[error] No Orbbec device detected and --device not specified.")
            print("  Connect a camera or use --no-hardware to run without one.")
            return 1
        if device_marker is None:
            print(f"[warn] Device '{device_name}' not recognised — running generic tests only.")

    # ---- Build report path ----
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_device = (device_marker or "generic").replace("/", "_")
    safe_cat = args.category or "all"
    report_name = f"test_report_{safe_device}_{safe_cat}_{timestamp}.html"
    report_path = os.path.join(output_dir, report_name)

    # ---- Print run summary ----
    print()
    print("=" * 60)
    print("  pyorbbecsdk Test Runner")
    print("=" * 60)
    print(f"  Device      : {device_name}")
    print(f"  Family      : {_DEVICE_DISPLAY.get(device_marker, device_marker or 'generic')}")
    print(f"  Serial      : {serial}")
    print(f"  Firmware    : {firmware}")
    print(f"  SDK version : {sdk_version}")
    print(f"  Category    : {args.category or 'all'}")
    print(f"  Quick mode  : {args.quick}")
    print(f"  No hardware : {args.no_hardware}")
    print(f"  Report      : {report_path}")
    print("=" * 60)
    print()

    # ---- Build and run pytest ----
    cmd = build_pytest_cmd(
        test_dir=test_dir,
        report_path=report_path,
        device_marker=device_marker,
        category=args.category,
        no_hardware=args.no_hardware,
        quick=args.quick,
        sdk_version=sdk_version,
        device_name=device_name,
        serial=serial,
        firmware=firmware,
    )

    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=repo_root)
    exit_code = result.returncode

    # ---- Copy to latest ----
    print()
    if os.path.exists(report_path):
        print(f"Report saved : {report_path}")
        latest = os.path.join(output_dir, "test_report_latest.html")
        try:
            import shutil

            shutil.copy2(report_path, latest)
            print(f"Latest copy  : {latest}")
        except Exception:
            pass
    else:
        print("WARNING: HTML report not created.")
        print("  Install pytest-html with: pip install pytest-html")

    # ---- Exit summary ----
    print()
    if exit_code == 0:
        print("Result: ALL PASSED")
    elif exit_code == 1:
        print("Result: SOME TESTS FAILED — see report for details")
    elif exit_code == 5:
        print("Result: NO TESTS COLLECTED — check --device / --category filters")
    else:
        print(f"Result: pytest exited with code {exit_code}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
