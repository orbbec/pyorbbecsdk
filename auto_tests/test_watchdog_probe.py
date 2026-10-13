"""Watchdog probe: deliberately hangs when it is run.

It carries its own ``watchdog_probe`` marker, so ``run_tests.py`` never selects
it (every suite filter starts from a marker such as ``unit`` or ``hardware``).
It exists to prove the runner can break out of a wedged run:

    $env:OB_TEST_STALL_TIMEOUT="20"
    python auto_tests/run_tests.py --suite unit --skip-health `
        --pytest-arg=auto_tests/test_watchdog_probe.py::test_zzz_intentionally_slow_watchdog_probe `
        --pytest-arg=-m --pytest-arg=watchdog_probe

Expected: a "[WARNING] pytest produced no output for 20s ... terminating it"
line, followed by the fallback-report notice, and the runner exiting within
~35s instead of hanging.
"""

import time

import pytest

pytestmark = pytest.mark.watchdog_probe


def test_zzz_intentionally_slow_watchdog_probe():
    time.sleep(600)
