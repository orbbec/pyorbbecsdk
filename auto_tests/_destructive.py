"""Single source of truth for the destructive hardware case list.

In the C++ tree the same list is duplicated in two places that must be kept in
sync by hand (``tests/hardware/CMakeLists.txt`` OB_HW_DESTRUCTIVE_TESTS and
``tests/hardware/hw_test_main_common.hpp`` kDestructiveTestFilter).  Here the
list lives once, the cases carry ``@pytest.mark.destructive``, and
``test_runner_selftest.py`` asserts that the two agree - so a drift fails a test
instead of silently changing which cases run in the default hardware suite.
"""

from __future__ import annotations

#: C++ case ids excluded from the default ``hw`` suite and run by the
#: ``destructive`` suite instead.  Keep the ordering identical to the C++ list
#: for easy diffing against the upstream test filter.
DESTRUCTIVE_TEST_IDS: tuple[str, ...] = (
    "TC_CPP_02_04_force_ip",
    "TC_CPP_02_05_hotplug_reboot",
    "TC_CPP_06_09_sensor_after_reboot",
    "TC_CPP_21_07_firmware_update",
    "TC_CPP_21_08_update_depth_presets",
)

#: Case ids that reboot the device but stay in the default hardware suite,
#: matching the C++ selection.  They are tagged ``reboot`` so the autouse
#: identity guard skips them (the old handle is invalid after a reboot).
#:
#: They are also run in their own process by ``run_tests.py``: rebooting inside
#: the shared pytest process corrupts the SDK heap for any later case (observed
#: as STATUS_HEAP_CORRUPTION on the next ``Pipeline()``), which CTest avoids by
#: giving every case its own process.
REBOOT_TEST_IDS: tuple[str, ...] = ("TC_CPP_21_06_reboot",)

DESTRUCTIVE_SET = frozenset(DESTRUCTIVE_TEST_IDS)
REBOOT_SET = frozenset(REBOOT_TEST_IDS)


def case_id_of(nodeid: str) -> str:
    """Best-effort extraction of the C++ case id from a pytest node id.

    Handles the parameterised form emitted for ported C++ ``TEST_P`` cases,
    e.g. ``test_playback_cpp.py::test_TC_CPP_18_playback_parameterized[
    None-TC_CPP_18_10_playback_device_info]`` -> ``TC_CPP_18_10_playback_device_info``.
    """
    tail = nodeid.rsplit("::", 1)[-1]
    if "[" in tail and tail.endswith("]"):
        tail = tail[tail.index("[") + 1 : -1]
        # Drop the leading parameter group (bag path placeholder) if present.
        if "-" in tail:
            tail = tail.split("-")[-1]
    if tail.startswith("test_"):
        tail = tail[len("test_") :]
    return tail
