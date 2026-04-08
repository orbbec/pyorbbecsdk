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
Automated test report generator for pyorbbecsdk releases.

Usage:
    # Full test suite (requires Gemini 335 connected)
    python test/generate_report.py

    # Quick smoke test (skip performance benchmarks)
    python test/generate_report.py --quick

    # Specific test module
    python test/generate_report.py --module test_g300_series_streams

    # Skip hardware tests (dry run, no camera needed)
    python test/generate_report.py --no-hardware

Options:
    --quick         Skip performance tests (marker: -m "not performance")
    --no-hardware   Skip hardware tests (marker: -m "not hardware")
    --module NAME   Run only the named test module
    --sdk-version V Override SDK version in report metadata (default: auto-detect)
    --output DIR    Report output directory (default: reports/)
"""

import argparse
import datetime
import os
import platform
import subprocess
import sys


def get_sdk_version():
    """Try to detect pyorbbecsdk2 version from the installed package."""
    try:
        import importlib.metadata

        return importlib.metadata.version("pyorbbecsdk2")
    except Exception:
        pass
    try:
        # Fall back to reading setup.py
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        setup_py = os.path.join(here, "setup.py")
        with open(setup_py) as f:
            for line in f:
                if "version=" in line and "'" in line:
                    return line.split("'")[1]
    except Exception:
        pass
    return "unknown"


def get_device_info():
    """Return a dict with connected device metadata (best-effort)."""
    info = {"name": "N/A", "serial": "N/A", "firmware": "N/A"}
    try:
        from pyorbbecsdk import Context, OBLogLevel

        ctx = Context()
        ctx.set_logger_level(OBLogLevel.NONE)
        device_list = ctx.query_devices()
        if device_list.get_count() > 0:
            dev = device_list.get_device_by_index(0)
            di = dev.get_device_info()
            info["name"] = di.get_name() or "N/A"
            info["serial"] = di.get_serial_number() or "N/A"
            info["firmware"] = di.get_firmware_version() or "N/A"
    except Exception:
        pass
    return info


def build_pytest_args(args, report_path, device_info, sdk_version):
    """Construct the pytest argument list."""
    pytest_args = []

    # Test target
    if args.module:
        # Support both bare name and filename
        module = args.module
        if not module.startswith("test_"):
            module = f"test_{module}"
        if not module.endswith(".py"):
            module = f"{module}.py"
        pytest_args.append(os.path.join(os.path.dirname(__file__), module))
    else:
        pytest_args.append(os.path.dirname(__file__))

    # Markers
    markers = []
    if args.no_hardware:
        markers.append("not hardware")
    if args.quick:
        markers.append("not performance")
    if markers:
        pytest_args += ["-m", " and ".join(f"({m})" for m in markers)]

    # Reporting
    pytest_args += [
        f"--html={report_path}",
        "--self-contained-html",
        "-v",
        "--tb=short",
        "--metadata",
        "SDK Version",
        sdk_version,
        "--metadata",
        "Device",
        device_info["name"],
        "--metadata",
        "Serial",
        device_info["serial"],
        "--metadata",
        "Firmware",
        device_info["firmware"],
        "--metadata",
        "OS",
        f"{platform.system()} {platform.release()}",
        "--metadata",
        "Python",
        sys.version.split()[0],
        "--metadata",
        "Machine",
        platform.machine(),
    ]

    if args.quick or args.no_hardware:
        pass  # no extra timeout
    else:
        pytest_args += ["--timeout=120"]  # generous for performance tests

    return pytest_args


def main():
    parser = argparse.ArgumentParser(
        description="Generate pyorbbecsdk test report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:")[1] if "Usage:" in __doc__ else "",
    )
    parser.add_argument("--quick", action="store_true", help="Skip performance benchmark tests")
    parser.add_argument("--no-hardware", action="store_true", help="Skip all hardware-dependent tests")
    parser.add_argument("--module", metavar="NAME", help="Run only a specific test module")
    parser.add_argument("--sdk-version", metavar="V", help="Override SDK version string in report")
    parser.add_argument(
        "--output",
        metavar="DIR",
        default="reports",
        help="Output directory for HTML report (default: reports/)",
    )
    args = parser.parse_args()

    # Resolve paths relative to repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, args.output)
    os.makedirs(output_dir, exist_ok=True)

    # Collect metadata
    sdk_version = args.sdk_version or get_sdk_version()
    device_info = (
        get_device_info()
        if not args.no_hardware
        else {"name": "N/A (--no-hardware)", "serial": "N/A", "firmware": "N/A"}
    )

    # Build report filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_ver = sdk_version.replace(".", "_")
    report_filename = f"test_report_{safe_ver}_{timestamp}.html"
    report_path = os.path.join(output_dir, report_filename)

    print(f"pyorbbecsdk Test Report Generator")
    print(f"  SDK version : {sdk_version}")
    print(f"  Device      : {device_info['name']} (SN: {device_info['serial']})")
    print(f"  Firmware    : {device_info['firmware']}")
    print(f"  Report path : {report_path}")
    print(f"  Quick mode  : {args.quick}")
    print(f"  No hardware : {args.no_hardware}")
    print()

    pytest_args = build_pytest_args(args, report_path, device_info, sdk_version)

    # Run pytest as a subprocess so the current process is not affected by
    # pytest's exit-code-based sys.exit()
    cmd = [sys.executable, "-m", "pytest"] + pytest_args
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=repo_root)
    exit_code = result.returncode

    print()
    if os.path.exists(report_path):
        print(f"HTML report saved to: {report_path}")
        # Also write a "latest" symlink-style convenience file
        latest_path = os.path.join(output_dir, "test_report_latest.html")
        try:
            import shutil

            shutil.copy2(report_path, latest_path)
            print(f"Latest report copy : {latest_path}")
        except Exception:
            pass
    else:
        print("WARNING: HTML report was not created (pytest-html may not be installed)")
        print("Install with: pip install pytest-html")

    # Summary
    if exit_code == 0:
        print("\nAll tests PASSED.")
    elif exit_code == 1:
        print("\nSome tests FAILED. See report for details.")
    elif exit_code == 5:
        print("\nNo tests were collected. Check --module name or marker filters.")
    else:
        print(f"\npytest exited with code {exit_code}.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
