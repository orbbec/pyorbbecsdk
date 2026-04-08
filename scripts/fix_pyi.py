#!/usr/bin/env python3
"""
Fix return type issues in pyorbbecsdk pyi files

Usage:
    python fix_pyi.py <input_pyi_file> [output_pyi_file]

If output_pyi_file is not specified, the input file will be modified directly.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path


def check_black_installed() -> bool:
    """Check if black is installed and available in PATH"""
    return shutil.which("black") is not None


def format_with_black(file_path: Path) -> bool:
    """Format the file with black, return True if successful"""
    result = subprocess.run(
        ["black", str(file_path), "--target-version", "py38"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def print_black_install_hint():
    """Print instructions for installing black"""
    print("\n" + "=" * 60)
    print("⚠️  black is not installed")
    print("=" * 60)
    print("To install black, use one of the following methods:")
    print("")
    print("  # Using uv (recommended):")
    print("  uv tool install black")
    print("")
    print("  # Using pip:")
    print("  pip install black")
    print("  # or")
    print("  pip install --user black")
    print("")
    print("Note: The pyi file has been fixed but not formatted.")
    print("      Run 'black <file> --target-version py38' manually")
    print("      or install black and re-run this script.")
    print("=" * 60 + "\n")


def check_isort_installed() -> bool:
    """Check if isort is installed and available in PATH"""
    return shutil.which("isort") is not None


def format_with_isort(file_path: Path) -> bool:
    """Format the file with isort, return True if successful"""
    result = subprocess.run(
        ["isort", str(file_path)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def print_isort_install_hint():
    """Print instructions for installing isort"""
    print("\n" + "=" * 60)
    print("⚠️  isort is not installed")
    print("=" * 60)
    print("To install isort, use one of the following methods:")
    print("")
    print("  # Using uv (recommended):")
    print("  uv tool install isort")
    print("")
    print("  # Using pip:")
    print("  pip install isort")
    print("  # or")
    print("  pip install --user isort")
    print("")
    print("Note: The pyi file has been fixed but not sorted.")
    print("      Run 'isort <file>' manually or install isort and re-run this script.")
    print("=" * 60 + "\n")


def fix_pyi_content(content: str) -> str:
    """Fix return type issues in pyi file content"""

    # 1. Fix typing_extensions.Buffer import issue
    # pybind11_stubgen generates typing_extensions.Buffer but doesn't add the import
    if "typing_extensions.Buffer" in content and "import typing_extensions" not in content:
        # Add typing_extensions import at the beginning of the file
        # Find the position of the last import statement
        import_pattern = r"^(import .+|from .+ import .+)$"
        last_import_end = 0
        for match in re.finditer(import_pattern, content, re.MULTILINE):
            last_import_end = match.end()

        if last_import_end > 0:
            # Add typing_extensions import after the last import
            content = content[:last_import_end] + "\nimport typing_extensions" + content[last_import_end:]
        else:
            # If no import found, add at the beginning of the file (skip possible shebang and docstring)
            lines = content.split("\n")
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith("#") or line.strip() == "":
                    insert_pos = i + 1
                else:
                    break
            lines.insert(insert_pos, "import typing_extensions")
            content = "\n".join(lines)

    # 2. Fix enum type default parameter values
    # pybind11_stubgen cannot parse C++ enum default values, generates ... as placeholder
    # Use line-level replacement to match the entire function signature line
    ENUM_DEFAULTS = [
        # Config class methods - enable_accel_stream (two parameters need to be fixed)
        (
            r"(def enable_accel_stream\(self, full_scale_range: OBAccelFullScaleRange) = \.\.\., (sample_rate: OBGyroSampleRate) = \.\.\.",
            r"\1 = OBAccelFullScaleRange.ACCEL_FS_UNKNOWN, \2 = OBGyroSampleRate.SAMPLE_RATE_UNKNOWN",
        ),
        # Config class methods - enable_gyro_stream
        (
            r"(def enable_gyro_stream\(self, full_scale_range: OBGyroFullScaleRange) = \.\.\., (sample_rate: OBGyroSampleRate) = \.\.\.",
            r"\1 = OBGyroFullScaleRange.FS_UNKNOWN, \2 = OBGyroSampleRate.SAMPLE_RATE_UNKNOWN",
        ),
        # Config class methods - enable_lidar_stream
        (
            r"(def enable_lidar_stream\(self, scan_rate: OBLiDARScanRate) = \.\.\., (format: OBFormat) = \.\.\.",
            r"\1 = OBLiDARScanRate.LIDAR_SCAN_UNKNOWN, \2 = OBFormat.UNKNOWN_FORMAT",
        ),
        # Config class methods - enable_video_stream
        (
            r"(def enable_video_stream\(.*format: OBFormat) = \.\.\.",
            r"\1 = OBFormat.UNKNOWN_FORMAT",
        ),
        # Context class methods
        (
            r"(def create_net_device\(.*access_mode: OBDeviceAccessMode) = \.\.\.",
            r"\1 = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS",
        ),
        # DeviceList class methods
        (
            r"(def get_device_by_index\(.*access_mode: OBDeviceAccessMode) = \.\.\.",
            r"\1 = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS",
        ),
        (
            r"(def get_device_by_serial_number\(.*access_mode: OBDeviceAccessMode) = \.\.\.",
            r"\1 = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS",
        ),
        (
            r"(def get_device_by_uid\(.*access_mode: OBDeviceAccessMode) = \.\.\.",
            r"\1 = OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS",
        ),
        # StreamProfileList class methods
        (
            r"(def get_video_stream_profile\(.*format: OBFormat) = \.\.\.",
            r"\1 = OBFormat.UNKNOWN_FORMAT",
        ),
    ]

    for pattern, replacement in ENUM_DEFAULTS:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            print(f"  Fixed: {pattern[:50]}...")
        content = new_content

    # Define method mappings that need to be fixed: class name -> {method name: return type}
    FIXES = {
        # Frame class
        "Frame": {
            "as_video_frame": "VideoFrame",
            "as_color_frame": "ColorFrame",
            "as_depth_frame": "DepthFrame",
            "as_ir_frame": "IRFrame",
            "as_frame_set": "FrameSet",
            "as_accel_frame": "AccelFrame",
            "as_gyro_frame": "GyroFrame",
            "as_confidence_frame": "ConfidenceFrame",
            "as_points_frame": "PointsFrame",
            "as_lidar_points_frame": "LiDARPointsFrame",
        },
        # VideoFrame class
        "VideoFrame": {
            "as_color_frame": "ColorFrame",
            "as_depth_frame": "DepthFrame",
            "as_ir_frame": "IRFrame",
            "as_confidence_frame": "ConfidenceFrame",
            "as_points_frame": "PointsFrame",
        },
        # StreamProfile class
        "StreamProfile": {
            "as_video_stream_profile": "VideoStreamProfile",
            "as_accel_stream_profile": "AccelStreamProfile",
            "as_gyro_stream_profile": "GyroStreamProfile",
            "as_lidar_stream_profile": "LiDARStreamProfile",
        },
    }

    # Fix methods: find class definitions, then fix methods within them
    for class_name, methods in FIXES.items():
        for method_name, return_type in methods.items():
            # Match method definitions in the class
            # Format: def method_name(self) -> ...:
            pattern = rf"(class {class_name}[^{{]*?\n)(.*?)(def {method_name}\(self\) -> \.\.\.:)"
            replacement = rf"\1\2def {method_name}(self) -> {return_type}:"
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Fix special return types (generics with type parameters)
    # Sensor.get_recommended_filters() -> list[...] should be list[Filter]
    content = re.sub(
        r"(class Sensor[^{]*?\n)(.*?)(def get_recommended_filters\(self\) -> list\[\.\.\.\]:)",
        r"\1\2def get_recommended_filters(self) -> list[Filter]:",
        content,
        flags=re.DOTALL,
    )

    return content


def fix_pyi_file(input_path: Path, output_path: Path = None) -> None:
    """Fix pyi file"""
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path
    else:
        output_path = Path(output_path)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    print(f"Reading: {input_path}")
    content = input_path.read_text(encoding="utf-8")

    fixed_content = fix_pyi_content(content)

    if content == fixed_content:
        print("No changes needed.")
    else:
        output_path.write_text(fixed_content, encoding="utf-8")
        print(f"Fixed: {output_path}")

    # Format with black if available
    print("Checking black formatter...")
    if check_black_installed():
        print("Running black formatter...")
        if format_with_black(output_path):
            print(f"Formatted with black: {output_path}")
        else:
            print(f"⚠️  Black formatting failed for: {output_path}")
    else:
        print_black_install_hint()

    # Format with isort if available
    print("Checking isort...")
    if check_isort_installed():
        print("Running isort...")
        if format_with_isort(output_path):
            print(f"Sorted imports with isort: {output_path}")
        else:
            print(f"⚠️  isort failed for: {output_path}")
    else:
        print_isort_install_hint()


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_pyi.py <input_pyi_file> [output_pyi_file]")
        print("")
        print("Example:")
        print("  python fix_pyi.py pyorbbecsdk.pyi")
        print("  python fix_pyi.py pyorbbecsdk.pyi pyorbbecsdk_fixed.pyi")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    fix_pyi_file(input_path, output_path)


if __name__ == "__main__":
    main()
