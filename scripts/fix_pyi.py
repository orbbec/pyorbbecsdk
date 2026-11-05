#!/usr/bin/env python3
"""
Repair generated pyorbbecsdk type stubs (Python 3.8+).

Usage:
    python fix_pyi.py <input_pyi_file> [output_pyi_file]

If output_pyi_file is not specified, the input file will be modified directly.
"""

import ast
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


# These overrides describe binding semantics that stubgen cannot infer from
# pybind11 docstrings, especially null shared_ptr values and py::object returns.
RETURN_TYPES = {
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
        "create_frame_set": "FrameSet",
        "create_video_frame": "VideoFrame",
    },
    "VideoFrame": {
        "as_color_frame": "ColorFrame",
        "as_depth_frame": "DepthFrame",
        "as_ir_frame": "IRFrame",
        "as_confidence_frame": "ConfidenceFrame",
        "as_points_frame": "PointsFrame",
    },
    "StreamProfile": {
        "as_video_stream_profile": "VideoStreamProfile",
        "as_accel_stream_profile": "AccelStreamProfile",
        "as_gyro_stream_profile": "GyroStreamProfile",
        "as_lidar_stream_profile": "LiDARStreamProfile",
    },
    "Sensor": {"get_recommended_filters": "list[Filter]"},
    "Device": {"get_available_frame_interleave_list": "DeviceFrameInterleaveList"},
    "ApplicationConfig": {"get_by_preset": "typing.Optional[ApplicationConfig]"},
    "ApplicationSensorConfig": {"stream_profile": "typing.Optional[StreamProfile]"},
    "Pipeline": {"wait_for_frames": "typing.Optional[FrameSet]"},
    "Filter": {"process": "typing.Optional[Frame]"},
    "FrameSet": {
        "__getitem__": "typing.Optional[Frame]",
        "get_frame": "typing.Optional[Frame]",
        "get_frame_by_type": "typing.Optional[Frame]",
        "get_frame_by_index": "typing.Optional[Frame]",
        **{
            "get_" + name + "_frame": "typing.Optional[" + frame_type + "]"
            for name, frame_type in {
                "depth": "DepthFrame",
                "color": "ColorFrame",
                "left_color": "ColorFrame",
                "right_color": "ColorFrame",
                "ir": "IRFrame",
                "left_ir": "IRFrame",
                "right_ir": "IRFrame",
                "confidence": "ConfidenceFrame",
                "accel": "AccelFrame",
                "gyro": "GyroFrame",
                "points": "PointsFrame",
                "lidar_points": "LiDARPointsFrame",
            }.items()
        },
    },
}

ENUM_DEFAULTS = {
    ("full_scale_range", "OBAccelFullScaleRange"): "OBAccelFullScaleRange.ACCEL_FS_UNKNOWN",
    ("full_scale_range", "OBGyroFullScaleRange"): "OBGyroFullScaleRange.FS_UNKNOWN",
    ("sample_rate", "OBGyroSampleRate"): "OBGyroSampleRate.SAMPLE_RATE_UNKNOWN",
    ("format", "OBFormat"): "OBFormat.UNKNOWN_FORMAT",
    ("access_mode", "OBDeviceAccessMode"): "OBDeviceAccessMode.OB_DEVICE_DEFAULT_ACCESS",
    ("scan_rate", "OBLiDARScanRate"): "OBLiDARScanRate.LIDAR_SCAN_UNKNOWN",
    ("stream_type", "OBStreamType"): "OBStreamType.COLOR_STREAM",
}

NUMERIC_INPUTS = {
    "int": "typing.SupportsInt | typing.SupportsIndex",
    "float": "typing.SupportsFloat | typing.SupportsIndex",
}


class _SourceEdits:
    """Edit AST spans while preserving docstrings, comments and formatting.

    AST columns are UTF-8 byte offsets, including when running on Python 3.8.
    No ast.unparse dependency or execution/import of the input stub is needed.
    """

    def __init__(self, source):
        self.source = source
        self.lines = source.splitlines(keepends=True)
        self.offsets = [0]
        for line in self.lines:
            self.offsets.append(self.offsets[-1] + len(line))
        self.edits = {}

    def offset(self, line, column):
        prefix = self.lines[line - 1].encode("utf-8")[:column].decode("utf-8")
        return self.offsets[line - 1] + len(prefix)

    def text(self, node):
        start = self.offset(node.lineno, node.col_offset)
        end = self.offset(node.end_lineno, node.end_col_offset)
        return self.source[start:end]

    def replace(self, node, replacement):
        start = self.offset(node.lineno, node.col_offset)
        end = self.offset(node.end_lineno, node.end_col_offset)
        if self.source[start:end] != replacement:
            self.edits[start, end] = replacement

    def apply(self):
        result = self.source
        boundary = len(result)
        for (start, end), replacement in sorted(self.edits.items(), reverse=True):
            if end > boundary:
                raise ValueError("Overlapping stub repairs")
            result = result[:start] + replacement + result[end:]
            boundary = start
        return result


def _annotation(source, node, numeric_input=False):
    text = source.text(node)
    text = text.replace("typing.Annotated", "typing_extensions.Annotated")
    # ndarray takes shape and dtype arguments. Older generators put a scalar
    # dtype in its only argument; NDArray is the corresponding one-argument alias.
    text = re.sub(
        r"numpy\.ndarray\[\s*(numpy\.\w+|typing\.Any)\s*\]",
        r"numpy.typing.NDArray[\1]",
        text,
    )
    return NUMERIC_INPUTS.get(text, text) if numeric_input else text


def _array_input(annotation):
    match = re.fullmatch(r"numpy\.typing\.NDArray\[(numpy\.\w+|typing\.Any)\]", annotation)
    if match:
        return "typing_extensions.Annotated[numpy.typing.ArrayLike, " + match[1] + "]"
    return annotation


def _ensure_imports(content):
    tree = ast.parse(content)
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.asname is None or alias.asname == alias.name
    }
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    uses_numpy_typing = any(
        isinstance(node, ast.Attribute)
        and node.attr == "typing"
        and isinstance(node.value, ast.Name)
        and node.value.id == "numpy"
        for node in ast.walk(tree)
    )
    required = []
    for name in ("typing", "numpy.typing", "typing_extensions"):
        used = uses_numpy_typing if name == "numpy.typing" else name in names
        if used and name not in imports:
            required.append("import " + name)
    if not required:
        return content
    # Insert after complete import statements, including multiline imports and
    # __future__ imports; otherwise retain the module docstring and comments.
    anchors = [n.end_lineno for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    if anchors:
        line = max(anchors)
    elif (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        line = tree.body[0].end_lineno
    else:
        line = tree.body[0].lineno - 1 if tree.body else len(content.splitlines())
    lines = content.splitlines(keepends=True)
    prefix = "".join(lines[:line])
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    return prefix + "\n".join(required) + "\n" + "".join(lines[line:])


def fix_pyi_content(content: str) -> str:
    """Repair generated annotations without crossing class/function boundaries.

    Numeric input protocols reflect pybind11 conversion; return values keep
    their concrete Python types. Reapplying this function is a no-op.
    """
    tree = ast.parse(content)
    edits = _SourceEdits(content)

    def fix_function(node, class_name=None, is_enum=False):
        args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
        for arg in args + [a for a in (node.args.vararg, node.args.kwarg) if a is not None]:
            if arg.annotation is None:
                continue
            annotation = _annotation(edits, arg.annotation, numeric_input=not is_enum)
            if class_name in ("Device", "OBDepthWorkMode") and node.name == "__eq__" and arg.arg != "self":
                annotation = "object"
            elif class_name == "Device" and node.name == "update_firmware_from_data" and arg.arg == "callback":
                annotation = "typing.Callable[[OBUpgradeState, str, int], None]"
            elif class_name == "ApplicationConfig" and node.name == "set_sensors" and arg.arg == "sensors":
                annotation = "typing.Sequence[ApplicationSensorConfig]"
            elif class_name == "OBImuPresetList" and node.name == "values" and arg.arg != "self":
                annotation = "typing.Sequence[int]"
            # Array setters accept ArrayLike, while getters return NDArray.
            if any(isinstance(d, ast.Attribute) and d.attr == "setter" for d in node.decorator_list):
                annotation = _array_input(annotation)
            edits.replace(arg.annotation, annotation)

        positional = node.args.posonlyargs + node.args.args
        defaults = list(zip(positional[len(positional) - len(node.args.defaults) :], node.args.defaults))
        defaults += list(zip(node.args.kwonlyargs, node.args.kw_defaults))
        for arg, default in defaults:
            if arg.annotation is not None and isinstance(default, ast.Constant) and default.value is Ellipsis:
                key = (arg.arg, edits.text(arg.annotation))
                if key in ENUM_DEFAULTS:
                    edits.replace(default, ENUM_DEFAULTS[key])

        if node.returns is not None:
            annotation = RETURN_TYPES.get(class_name, {}).get(node.name, _annotation(edits, node.returns))
            if (
                class_name == "OBImuPresetList"
                and node.name == "values"
                and not any(isinstance(d, ast.Attribute) and d.attr == "setter" for d in node.decorator_list)
            ):
                annotation = "list[int]"
            edits.replace(node.returns, annotation)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            fix_function(node)
        elif isinstance(node, ast.ClassDef):
            is_enum = any(
                isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == "__members__"
                for n in node.body
            )
            for member in node.body:
                if isinstance(member, ast.FunctionDef):
                    fix_function(member, node.name, is_enum)
                elif isinstance(member, ast.AnnAssign):
                    annotation = _annotation(edits, member.annotation)
                    name = member.target.id if isinstance(member.target, ast.Name) else None
                    if name == "__hash__" and node.name in ("Device", "OBDepthWorkMode"):
                        # Keep these classes unhashable. typeshed uses the same
                        # targeted exception for object.__hash__ overrides.
                        line = edits.lines[member.lineno - 1]
                        if "type: ignore" not in line:
                            edits.replace(member, edits.text(member) + "  # type: ignore[assignment]")
                    elif (
                        not is_enum
                        and name
                        and (
                            annotation in NUMERIC_INPUTS
                            or _array_input(annotation) != annotation
                            or (node.name == "OBImuPresetList" and name == "values")
                        )
                    ):
                        getter = "list[int]" if node.name == "OBImuPresetList" and name == "values" else annotation
                        setter = (
                            "typing.Sequence[int]"
                            if node.name == "OBImuPresetList" and name == "values"
                            else _array_input(NUMERIC_INPUTS.get(annotation, annotation))
                        )
                        indent = " " * member.col_offset
                        replacement = f"@property\n{indent}def {name}(self) -> {getter}: ..."
                        if not (node.name == "OBImuPresetList" and name == "count"):
                            replacement += (
                                f"\n{indent}@{name}.setter\n{indent}def {name}(self, value: {setter}) -> None: ..."
                            )
                        edits.replace(member, replacement)
                    else:
                        edits.replace(member.annotation, annotation)
    fixed = _ensure_imports(edits.apply())
    ast.parse(fixed)  # Never write syntactically invalid output.
    return fixed


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

    if content == fixed_content and output_path == input_path:
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
