#!/usr/bin/env python3
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.request
from urllib.error import URLError

# Add the parent directory to sys.path to allow importing pyorbbecsdk if running from scripts/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from pyorbbecsdk import *
except ImportError:
    print("Error: 'pyorbbecsdk' module not found.")
    print("Please install it via pip: pip install pyorbbecsdk2")
    sys.exit(1)

CONFIG_FILE_PATH = os.path.join(project_root, "config", "firmware_compatibility_pid.json")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("========================================================")
    print("   Orbbec Device Firmware Update Assistant")
    print("========================================================")


def load_config():
    """Load the firmware compatibility configuration."""
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"[!] Config file not found: {CONFIG_FILE_PATH}")
        return None
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Error loading config file: {e}")
        return None


def get_device_config(pid, device_name, config):
    """Find the configuration entry for a given device pid or name."""
    if not config or "devices" not in config:
        return None

    # Primary match: PID
    for entry in config["devices"]:
        if "pids" in entry and pid in entry["pids"]:
            return entry

    # Fallback match: Name
    for entry in config["devices"]:
        if "products" in entry:
            for product in entry["products"]:
                if product.lower() in device_name.lower():
                    return entry
    return None


def parse_version(version_str):
    """Parse version string into a tuple of integers."""
    # Remove 'v' prefix if present and split by '.'
    clean_ver = version_str.strip().lstrip("v")
    # Handle potential non-numeric suffixes (e.g. -beta, -rc) by splitting on '-'
    clean_ver = clean_ver.split("-")[0]
    try:
        return tuple(map(int, clean_ver.split(".")))
    except ValueError:
        return (0, 0, 0)


def compare_versions(current_ver, recommended_ver):
    """
    Compare two version strings.
    Returns:
         1 if current > recommended
         0 if current == recommended
        -1 if current < recommended
    """
    v1 = parse_version(current_ver)
    v2 = parse_version(recommended_ver)

    if v1 > v2:
        return 1
    elif v1 == v2:
        return 0
    else:
        return -1


def download_progress_hook(block_num, block_size, total_size):
    """Callback for urllib.urlretrieve to show download progress."""
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, int(downloaded * 100 / total_size))
        bar_length = 40
        filled_length = int(bar_length * percent // 100)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        sys.stdout.write(
            f"\rDownloading: |{bar}| {percent}% ({downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB)"
        )
        sys.stdout.flush()


def download_firmware(url):
    """Download firmware from the given URL to a temporary file."""
    print(f"\nDownloading firmware from: {url}")
    try:
        # Create a temporary file
        fd, temp_path = tempfile.mkstemp(suffix=".bin")
        os.close(fd)

        urllib.request.urlretrieve(url, temp_path, reporthook=download_progress_hook)
        print("\nDownload complete.")
        return temp_path
    except URLError as e:
        print(f"\n[!] Download failed: {e}")
        return None
    except Exception as e:
        print(f"\n[!] Error during download: {e}")
        return None


def progress_callback(state, message, percent):
    """Callback function to report firmware update progress."""
    bar_length = 40
    filled_length = int(bar_length * percent // 100)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    # Overwrite the current line
    sys.stdout.write(f"\rUpdate Progress: |{bar}| {percent}% - {message}")
    sys.stdout.flush()


def main():
    print_header()

    # Load configuration
    config = load_config()
    if not config:
        print("Cannot proceed without configuration.")
        sys.exit(1)

    # 1. Initialize Context and Query Devices
    try:
        ctx = Context()
        device_list = ctx.query_devices()

        if device_list.get_count() == 0:
            print("\n[!] No Orbbec devices found.")
            print("    Please connect your camera and try again.")
            sys.exit(1)

        print(f"\n[Step 1] Checking Connected Devices (Found {device_list.get_count()} devices)")

        devices_to_update = []

        for i in range(device_list.get_count()):
            device = device_list.get_device_by_index(i)
            info = device.get_device_info()
            name = info.get_name()
            pid = info.get_pid()
            # Normalize name by removing 'Orbbec' (case-insensitive) if present
            if "orbbec" in name.lower():
                name = re.sub(r"(?i)orbbec", "", name).strip()

            serial = info.get_serial_number()
            current_fw = info.get_firmware_version()

            print(f"\n  Device [{i}]: {name} (PID: {pid}, SN: {serial})")
            print(f"    Current Firmware: {current_fw}")

            # Check against config
            dev_config = get_device_config(pid, name, config)
            if dev_config:
                rec_fw = dev_config["recommended_version"]
                print(f"    Recommended Firmware: {rec_fw}")

                # Compare versions semantically
                comparison = compare_versions(current_fw, rec_fw)

                if comparison >= 0:
                    print("    Status: Already compatible with your firmware, no need to update.")
                else:
                    print(f"    Status: Update available ({current_fw} -> {rec_fw})")
                    devices_to_update.append((device, dev_config, name))
            else:
                print("    Status: No matching configuration found for this device.")

        if not devices_to_update:
            print("\nAll devices are up to date or no configuration found.")
            sys.exit(0)

        # 2. Process Updates
        print(f"\n[Step 2] Processing Updates for {len(devices_to_update)} device(s)")

        for device, dev_config, name in devices_to_update:
            print(f"\nPreparing to update {name}...")
            url = dev_config["download_url"]

            confirm = input(f"  > Do you want to download and update firmware for {name}? (y/n) [y]: ").strip().lower()
            if confirm not in ("", "y", "yes"):
                print("  Skipping update.")
                continue

            # Download
            bin_path = download_firmware(url)
            if not bin_path:
                print("  Skipping update due to download failure.")
                continue

            # Update
            print(f"\n  Starting firmware update for {name}...")
            print("  WARNING: DO NOT DISCONNECT THE CAMERA DURING UPDATE!")

            try:
                # device.update_firmware takes (path, callback, async_bool)
                device.update_firmware(bin_path, progress_callback, False)
                print("\n\n  [SUCCESS] Firmware update completed.")
                print("  Please disconnect and reconnect your device to apply changes.")
            except Exception as e:
                print(f"\n\n  [FAILED] Update error: {e}")
            finally:
                # Clean up temp file
                if os.path.exists(bin_path):
                    try:
                        os.remove(bin_path)
                    except:
                        pass

    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")


if __name__ == "__main__":
    main()
