"""Hardware-free regression tests: python -m unittest discover -s scripts/tests."""

import ast
import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "fix_pyi.py"
SPEC = importlib.util.spec_from_file_location("fix_pyi", SCRIPT)
fix_pyi = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fix_pyi)


class FixPyiTests(unittest.TestCase):
    def repair(self, source):
        fixed = fix_pyi.fix_pyi_content(textwrap.dedent(source))
        ast.parse(fixed)
        self.assertEqual(fix_pyi.fix_pyi_content(fixed), fixed)
        return fixed

    def test_array_getter_and_setter_keep_different_types(self):
        fixed = self.repair('''\
            """数组类型：numpy.ndarray must stay in this docstring."""
            from __future__ import annotations
            import numpy
            class OBAccelIntrinsic:
                bias: numpy.ndarray[numpy.float64]
            class Frame:
                def get_data(self) -> numpy.ndarray[numpy.uint8]: ...
        ''')
        self.assertIn("import numpy.typing", fixed)
        self.assertIn("import typing_extensions", fixed)
        self.assertIn("def bias(self) -> numpy.typing.NDArray[numpy.float64]", fixed)
        self.assertIn("value: typing_extensions.Annotated[numpy.typing.ArrayLike, numpy.float64]", fixed)
        self.assertIn("def get_data(self) -> numpy.typing.NDArray[numpy.uint8]", fixed)
        self.assertIn("数组类型：numpy.ndarray must stay in this docstring.", fixed)
        self.assertLess(fixed.index("from __future__"), fixed.index("import numpy.typing"))

    def test_existing_array_properties_and_valid_ndarray_are_preserved(self):
        fixed = self.repair("""\
            import typing
            import numpy
            class OBExtrinsic:
                @property
                def rot(self) -> numpy.typing.NDArray[numpy.float32]: ...
                @rot.setter
                def rot(self, value: typing.Annotated[numpy.typing.ArrayLike, numpy.float32]) -> None: ...
            def explicit() -> numpy.ndarray[typing.Any, numpy.dtype[numpy.uint8]]: ...
        """)
        self.assertIn("typing_extensions.Annotated", fixed)
        self.assertIn("numpy.ndarray[typing.Any, numpy.dtype[numpy.uint8]]", fixed)
        self.assertEqual(fixed.count("@rot.setter"), 1)

    def test_numeric_inputs_but_not_outputs_or_readonly_properties(self):
        fixed = self.repair("""\
            class OBPoint3f:
                x: float
                @property
                def size(self) -> int: ...
            def convert(value: float, index: int = 0, enabled: bool = True) -> float: ...
        """)
        self.assertIn("value: typing.SupportsFloat | typing.SupportsIndex", fixed)
        self.assertIn("index: typing.SupportsInt | typing.SupportsIndex = 0", fixed)
        self.assertIn("enabled: bool = True) -> float", fixed)
        self.assertIn("def x(self) -> float", fixed)
        self.assertNotIn("@size.setter", fixed)

    def test_rules_do_not_cross_class_boundaries_and_handle_multiline_signatures(self):
        fixed = self.repair("""\
            class Frame:
                @staticmethod
                def create_video_frame(
                    callback: typing.Callable[[int, int], None],
                    size: int = 0,
                ) -> ...: ...
            class Unrelated:
                def as_video_frame(self) -> ...: ...
                def process(self) -> str: ...
            class FrameSet:
                def get_depth_frame(self) -> DepthFrame: ...
                def get_frame_count(self) -> int: ...
            class Filter:
                def process(self, frame: Frame) -> typing.Any: ...
        """)
        self.assertIn(") -> VideoFrame:", fixed)
        self.assertIn("def as_video_frame(self) -> ...", fixed)
        self.assertIn("def process(self) -> str", fixed)
        self.assertIn("def get_depth_frame(self) -> typing.Optional[DepthFrame]", fixed)
        self.assertIn("def get_frame_count(self) -> int", fixed)
        self.assertIn("-> typing.Optional[Frame]", fixed)

    def test_enum_defaults_and_enum_integer_parameters(self):
        fixed = self.repair("""\
            import typing
            class OBFormat:
                __members__: typing.ClassVar[dict[str, OBFormat]]
                def __init__(self, value: int) -> None: ...
            class Config:
                def enable_video_stream(self, format: OBFormat = ...) -> None: ...
                def unrelated(self, default: int = ...) -> None: ...
        """)
        self.assertIn("format: OBFormat = OBFormat.UNKNOWN_FORMAT", fixed)
        self.assertIn("def __init__(self, value: int)", fixed)
        self.assertIn("default: typing.SupportsInt | typing.SupportsIndex = ...", fixed)

    def test_callbacks_sequences_and_nullable_application_config(self):
        fixed = self.repair("""\
            class Device:
                def update_firmware_from_data(self, data: bytes, callback: typing.Callable, async_update: bool = True) -> None: ...
            class ApplicationConfig:
                @staticmethod
                def get_by_preset(device: Device, preset_name: str) -> ApplicationConfig: ...
                def set_sensors(self, sensors: list[ApplicationSensorConfig]) -> None: ...
            class ApplicationSensorConfig:
                def stream_profile(self) -> StreamProfile: ...
            class OBImuPresetList:
                @property
                def values(self) -> list: ...
                @values.setter
                def values(self, items: typing.Sequence) -> None: ...
        """)
        self.assertIn("callback: typing.Callable[[OBUpgradeState, str, int], None]", fixed)
        self.assertIn("sensors: typing.Sequence[ApplicationSensorConfig]", fixed)
        self.assertIn("-> typing.Optional[ApplicationConfig]", fixed)
        self.assertIn("-> typing.Optional[StreamProfile]", fixed)
        self.assertIn("def values(self) -> list[int]", fixed)
        self.assertIn("items: typing.Sequence[int]", fixed)

    def test_unhashable_and_equality_declarations(self):
        fixed = self.repair("""\
            class Device:
                __hash__: typing.ClassVar[None] = None
                def __eq__(self, other: Device) -> bool: ...
            class OBDepthWorkMode:
                __hash__: typing.ClassVar[None] = None
                def __eq__(self, other: OBDepthWorkMode) -> bool: ...
        """)
        self.assertEqual(fixed.count("# type: ignore[assignment]"), 2)
        self.assertEqual(fixed.count("def __eq__(self, other: object)"), 2)

    def test_missing_imports_follow_complete_multiline_imports(self):
        fixed = self.repair("""\
            from __future__ import annotations
            from somewhere import (
                Something,
            )
            import typing as t
            class Frame:
                def update_data(self, data: typing_extensions.Buffer) -> None: ...
            def convert(value: float) -> float: ...
        """)
        self.assertIn("import typing\n", fixed)
        self.assertIn("import typing_extensions\n", fixed)
        self.assertLess(fixed.index("    Something,"), fixed.index("import typing_extensions"))

    def test_separate_output_is_written_even_when_no_repairs_are_needed(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.pyi"
            output = Path(directory) / "output.pyi"
            source.write_text("def get_version() -> str: ...\n", encoding="utf-8")
            with patch.object(fix_pyi, "check_black_installed", return_value=False), patch.object(
                fix_pyi, "check_isort_installed", return_value=False
            ), patch("builtins.print"):
                fix_pyi.fix_pyi_file(source, output)
            self.assertEqual(source.read_text(), output.read_text())

    def test_repository_stub_is_valid_and_idempotent(self):
        source = (SCRIPT.parents[1] / "stubs" / "pyorbbecsdk.pyi").read_text(encoding="utf-8")
        fixed = self.repair(source)
        self.assertNotIn("numpy.ndarray[numpy.", fixed)
        self.assertIn("typing.Optional[FrameSet]", fixed)


if __name__ == "__main__":
    unittest.main()
