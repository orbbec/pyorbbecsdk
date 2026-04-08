#!/usr/bin/env python3
"""
Orbbec SDK — One-Click Environment Setup
=========================================

Automatically configures your OS for Orbbec RGB-D cameras:

  * **Windows** — Registers UVC metadata in the Windows registry
    (required for correct timestamps and frame synchronization).
  * **Linux**   — Installs udev rules for USB device access.

Usage:
    # Windows (run as Administrator)
    python scripts/env_setup/setup_env.py

    # Linux
    sudo python3 scripts/env_setup/setup_env.py

    # Check current status without making changes
    python scripts/env_setup/setup_env.py --check

    # Remove previously installed configuration
    python scripts/env_setup/setup_env.py --uninstall
"""

import argparse
import ctypes
import os
import platform
import shutil
import subprocess
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
#  Colour helpers (ANSI)
# ---------------------------------------------------------------------------
_USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _green(text: str) -> str:
    return f"\033[92m{text}\033[0m" if _USE_COLOR else text


def _yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m" if _USE_COLOR else text


def _red(text: str) -> str:
    return f"\033[91m{text}\033[0m" if _USE_COLOR else text


def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m" if _USE_COLOR else text


# ---------------------------------------------------------------------------
#  Windows helpers
# ---------------------------------------------------------------------------
_UDEV_RULES_SRC = os.path.join(_SCRIPT_DIR, "99-obsensor-libusb.rules")
_UDEV_RULES_DST = "/etc/udev/rules.d/99-obsensor-libusb.rules"
_PS_SCRIPT = os.path.join(_SCRIPT_DIR, "obsensor_metadata_win10.ps1")


def _is_admin_windows() -> bool:
    """Return True if running with Administrator privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore[attr-defined]
    except AttributeError:
        return False


def _run_ps_script(operation: str) -> int:
    """Run the PowerShell metadata registration script with the given -op."""
    ps = shutil.which("powershell")
    if ps is None:
        print(_red("[ERROR] PowerShell not found on PATH."))
        return 1

    cmd = [
        ps,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        _PS_SCRIPT,
        "-op",
        operation,
    ]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def _windows_check() -> bool:
    """Check if the metadata PowerShell script exists."""
    if not os.path.isfile(_PS_SCRIPT):
        print(_red(f"[ERROR] Script not found: {_PS_SCRIPT}"))
        return False
    print(_green("[OK]"), "Metadata registration script found.")
    print("     Run this tool without --check to apply.")
    return True


def _windows_install() -> int:
    if not os.path.isfile(_PS_SCRIPT):
        print(_red(f"[ERROR] Script not found: {_PS_SCRIPT}"))
        return 1

    if not _is_admin_windows():
        print(_yellow("[WARN] Not running as Administrator — requesting elevation …"))
        # Re-launch self as admin
        args = " ".join(f'"{a}"' for a in sys.argv)
        try:
            ctypes.windll.shell32.ShellExecuteW(  # type: ignore[attr-defined]
                None, "runas", sys.executable, args, None, 1
            )
            print("  Elevated process launched. Check the new window for progress.")
            return 0
        except Exception as exc:
            print(_red(f"[ERROR] Failed to elevate: {exc}"))
            print("  Please re-run this script from an Administrator terminal.")
            return 1

    print(_bold("=== Windows Metadata Registration ==="))
    print()
    print("Registering UVC metadata for all Orbbec devices …")
    rc = _run_ps_script("install_all")
    if rc == 0:
        print()
        print(_green("[OK] Metadata registration completed."))
        print("     Timestamps and frame synchronization are now enabled.")
    else:
        print()
        print(_red(f"[ERROR] PowerShell script exited with code {rc}."))
        print("     See output above for details.")
    return rc


def _windows_uninstall() -> int:
    if not os.path.isfile(_PS_SCRIPT):
        print(_red(f"[ERROR] Script not found: {_PS_SCRIPT}"))
        return 1
    if not _is_admin_windows():
        print(_red("[ERROR] Administrator privileges required. Re-run as Administrator."))
        return 1
    return _run_ps_script("remove_all")


# ---------------------------------------------------------------------------
#  Linux helpers
# ---------------------------------------------------------------------------
def _is_root() -> bool:
    return os.geteuid() == 0  # type: ignore[attr-defined]


def _linux_check() -> bool:
    if os.path.isfile(_UDEV_RULES_DST):
        print(_green("[OK]"), f"udev rules installed at {_UDEV_RULES_DST}")
        return True
    else:
        print(_yellow("[MISSING]"), f"udev rules not found at {_UDEV_RULES_DST}")
        print("       Run this tool without --check to install.")
        return False


def _linux_install() -> int:
    if not os.path.isfile(_UDEV_RULES_SRC):
        print(_red(f"[ERROR] Rules file not found: {_UDEV_RULES_SRC}"))
        return 1

    if not _is_root():
        print(_yellow("[WARN] Root privileges required — re-running with sudo …"))
        args = [sys.executable] + sys.argv
        os.execvp("sudo", ["sudo"] + args)
        # execvp replaces the process; code below is unreachable
        return 1

    print(_bold("=== Linux udev Rules Installation ==="))
    print()

    # Copy rules file
    shutil.copy2(_UDEV_RULES_SRC, _UDEV_RULES_DST)
    print(f"  Installed {_UDEV_RULES_DST}")

    # Reload udev
    print("  Reloading udev rules …")
    subprocess.run(["udevadm", "control", "--reload"], check=True)
    subprocess.run(["udevadm", "trigger"], check=True)

    print()
    print(_green("[OK] udev rules installed and activated."))
    print("     Your Orbbec camera can now be accessed without root.")
    return 0


def _linux_uninstall() -> int:
    if not _is_root():
        print(_red("[ERROR] Root privileges required. Re-run with sudo."))
        return 1
    if os.path.isfile(_UDEV_RULES_DST):
        os.remove(_UDEV_RULES_DST)
        subprocess.run(["udevadm", "control", "--reload"], check=True)
        subprocess.run(["udevadm", "trigger"], check=True)
        print(_green("[OK]"), "udev rules removed.")
    else:
        print(_yellow("[INFO]"), "Nothing to remove — rules file not found.")
    return 0


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-click environment setup for Orbbec RGB-D cameras.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_env.py             Install / register (default)
  python setup_env.py --check     Verify setup status
  python setup_env.py --uninstall Remove configuration
        """,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--check",
        action="store_true",
        help="Check current configuration status (no changes made).",
    )
    group.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove previously installed configuration.",
    )
    args = parser.parse_args()

    system = platform.system()
    print()
    print(_bold(f"Orbbec SDK Environment Setup  [{system}]"))
    print("=" * 44)
    print()

    if system == "Windows":
        if args.check:
            return 0 if _windows_check() else 1
        elif args.uninstall:
            return _windows_uninstall()
        else:
            return _windows_install()

    elif system == "Linux":
        if args.check:
            return 0 if _linux_check() else 1
        elif args.uninstall:
            return _linux_uninstall()
        else:
            return _linux_install()

    elif system == "Darwin":
        print(_yellow("[INFO] macOS does not require additional environment setup."))
        return 0

    else:
        print(_red(f"[ERROR] Unsupported platform: {system}"))
        return 1


if __name__ == "__main__":
    sys.exit(main())
