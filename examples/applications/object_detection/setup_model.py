#!/usr/bin/env python3
# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
"""
One-click setup for YOLOv5 + Orbbec Object Detection.

  1. Install runtime Python dependencies (onnxruntime, opencv-python, numpy)
  2. Download the YOLOv5s ONNX model to  models/yolov5s.onnx

Usage:
    python setup_model.py              # default: download model + install deps
    python setup_model.py --force      # re-download even if model exists
    python setup_model.py --skip-deps  # skip pip install step
    python setup_model.py --export     # force local export (requires PyTorch)
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from urllib.error import URLError
from urllib.request import Request, urlopen, urlretrieve

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(_SCRIPT_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "yolov5s.onnx")

# ---------------------------------------------------------------------------
# Runtime dependencies (lightweight — no PyTorch)
# ---------------------------------------------------------------------------
RUNTIME_DEPS = ["numpy", "opencv-python", "onnxruntime"]

# ---------------------------------------------------------------------------
# Download sources (tried in order)
# ---------------------------------------------------------------------------
# The official ultralytics/yolov5 v7.0 release only ships .pt weights.
# The ONNX file can sometimes be found on community mirrors.
ONNX_URLS = [
    # Official v7.0 release (may not have .onnx — kept as first try)
    "https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.onnx",
]

# For the export fallback we download the repo as a zip (no git required).
YOLOV5_ZIP_URL = "https://github.com/ultralytics/yolov5/archive/refs/tags/v7.0.zip"
YOLOV5_PT_URL = "https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt"


# ===========================================================================
# Utilities
# ===========================================================================


def _pip_install(packages, quiet=False):
    """Run pip install for a list of packages."""
    cmd = [sys.executable, "-m", "pip", "install"] + packages
    if quiet:
        cmd.append("-q")
    subprocess.check_call(cmd, stdout=sys.stdout, stderr=sys.stderr)


def _download(url, dest, desc="Downloading"):
    """Download *url* to *dest* with a simple progress indicator."""
    print(f"  {desc}: {url}")
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=120) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            buf = bytearray()
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                buf.extend(chunk)
                if total:
                    pct = len(buf) * 100 // total
                    mb = len(buf) / (1024 * 1024)
                    print(f"\r  Progress: {pct:3d}%  ({mb:.1f} MB)", end="", flush=True)
            print()  # newline after progress
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(buf)
        return True
    except (URLError, OSError, TimeoutError) as exc:
        print(f"  Download failed: {exc}")
        return False


def _is_valid_onnx(path):
    """Quick sanity check — reject HTML error pages masquerading as models."""
    if not os.path.isfile(path):
        return False
    size = os.path.getsize(path)
    if size < 1024:  # an ONNX model is at least a few MB
        return False
    with open(path, "rb") as f:
        head = f.read(8)
    # HTML 404 pages start with '<!DO' or '<htm'
    if head[:4] in (b"<!DO", b"<htm", b"<HTM", b"<html"):
        return False
    return True


# ===========================================================================
# Method 1 — Direct ONNX download
# ===========================================================================


def try_direct_download():
    """Attempt to download a pre-exported ONNX from known URLs."""
    for url in ONNX_URLS:
        if _download(url, MODEL_PATH, "Trying direct ONNX download"):
            if _is_valid_onnx(MODEL_PATH):
                return True
            # Got an HTML redirect / 404 — remove and try next
            os.remove(MODEL_PATH)
            print("  Received invalid file (HTML redirect?), trying next URL...")
    return False


# ===========================================================================
# Method 2 — Download yolov5 repo (zip) + export locally
# ===========================================================================


def try_export():
    """Download the yolov5 v7.0 source as a zip, install deps, and export."""
    tmpdir = tempfile.mkdtemp(prefix="yolov5_export_")
    zip_path = os.path.join(tmpdir, "yolov5.zip")
    try:
        # ---- 2a. Download repo zip ----
        print("  Downloading yolov5 v7.0 source (zip)...")
        if not _download(YOLOV5_ZIP_URL, zip_path, "YOLOv5 repo"):
            # Fallback: try git clone if user has git
            return _try_git_clone_export(tmpdir)

        # ---- 2b. Extract ----
        print("  Extracting...")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmpdir)
        # The zip contains a top-level directory like  yolov5-7.0/
        subdirs = [d for d in os.listdir(tmpdir) if os.path.isdir(os.path.join(tmpdir, d)) and d.startswith("yolov5")]
        if not subdirs:
            print("  Could not find yolov5 folder in extracted zip.")
            return False
        repo_dir = os.path.join(tmpdir, subdirs[0])

        return _run_export(repo_dir)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _try_git_clone_export(tmpdir):
    """Fallback: use git clone if available."""
    repo_dir = os.path.join(tmpdir, "yolov5")
    try:
        print("  Zip download failed. Trying git clone...")
        subprocess.check_call(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                "v7.0",
                "https://github.com/ultralytics/yolov5.git",
                repo_dir,
            ],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"  git clone failed: {exc}")
        return False
    return _run_export(repo_dir)


def _run_export(repo_dir):
    """Install yolov5 requirements and run export.py inside *repo_dir*."""
    # ---- Install export dependencies ----
    print("  Installing PyTorch & export tools (this may take several minutes)...")
    req_file = os.path.join(repo_dir, "requirements.txt")
    try:
        _pip_install(["-r", req_file])
        _pip_install(["onnx"])
    except subprocess.CalledProcessError as exc:
        print(f"  pip install failed: {exc}")
        return False

    # ---- Download yolov5s.pt if not already cached ----
    pt_path = os.path.join(repo_dir, "yolov5s.pt")
    if not os.path.isfile(pt_path):
        if not _download(YOLOV5_PT_URL, pt_path, "YOLOv5s weights (.pt)"):
            print("  Could not download yolov5s.pt")
            return False

    # ---- Export ----
    print("  Exporting yolov5s.pt -> yolov5s.onnx (opset 12, imgsz 640)...")
    try:
        subprocess.check_call(
            [
                sys.executable,
                os.path.join(repo_dir, "export.py"),
                "--weights",
                pt_path,
                "--include",
                "onnx",
                "--opset",
                "12",
                "--imgsz",
                "640",
            ],
            cwd=repo_dir,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except subprocess.CalledProcessError as exc:
        print(f"  export failed: {exc}")
        return False

    src = os.path.join(repo_dir, "yolov5s.onnx")
    if not os.path.isfile(src):
        # export.py may write the file next to the .pt
        src = pt_path.replace(".pt", ".onnx")
    if not os.path.isfile(src):
        print("  Export completed but yolov5s.onnx not found.")
        return False

    os.makedirs(MODEL_DIR, exist_ok=True)
    shutil.copy2(src, MODEL_PATH)
    return True


# ===========================================================================
# Main
# ===========================================================================


def main():
    parser = argparse.ArgumentParser(description="One-click setup: install deps + download YOLOv5s ONNX model")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download model even if it already exists",
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip installing Python runtime dependencies",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Force local export from .pt (requires PyTorch)",
    )
    args = parser.parse_args()

    banner = "=" * 60
    print(banner)
    print("  YOLOv5 + Orbbec Object Detection  -  One-Click Setup")
    print(banner)

    # ------------------------------------------------------------------
    # Step 1: Runtime dependencies
    # ------------------------------------------------------------------
    if args.skip_deps:
        print("\n[1/2] Skipping dependency installation (--skip-deps)")
    else:
        print("\n[1/2] Installing runtime dependencies...")
        try:
            _pip_install(RUNTIME_DEPS, quiet=True)
            print("  OK: " + ", ".join(RUNTIME_DEPS))
        except subprocess.CalledProcessError:
            print("  FAILED — please install manually:")
            print(f'    pip install {" ".join(RUNTIME_DEPS)}')
            return 1

    # ------------------------------------------------------------------
    # Step 2: Get model
    # ------------------------------------------------------------------
    if os.path.isfile(MODEL_PATH) and not args.force:
        size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
        print(f"\n[2/2] Model already exists: {MODEL_PATH}  ({size_mb:.1f} MB)")
        print("  Use --force to re-download.")
    else:
        if args.force and os.path.isfile(MODEL_PATH):
            os.remove(MODEL_PATH)

        success = False

        if not args.export:
            # Method 1: direct ONNX download
            print("\n[2/2] Downloading YOLOv5s ONNX model...")
            print("\n  --- Method 1: Direct ONNX download ---")
            success = try_direct_download()

        if not success:
            # Method 2: export from .pt
            print("\n  --- Method 2: Local export from PyTorch weights ---")
            print("  (Requires ~2 GB PyTorch download on first run)")
            success = try_export()

        if success and os.path.isfile(MODEL_PATH):
            size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
            print(f"\n  Model saved: {MODEL_PATH}  ({size_mb:.1f} MB)")
        else:
            print("\n  ALL methods failed. Please download manually:")
            print("    1. git clone https://github.com/ultralytics/yolov5.git")
            print("    2. cd yolov5 && pip install -r requirements.txt && pip install onnx")
            print("    3. python export.py --weights yolov5s.pt --include onnx --opset 12")
            print(f"    4. Copy yolov5s.onnx to: {MODEL_PATH}")
            return 1

    # ------------------------------------------------------------------
    # Done
    # ------------------------------------------------------------------
    print(f"\n{banner}")
    print("  Setup complete!  Run the detector:")
    print(f'    python {os.path.join(_SCRIPT_DIR, "object_detection.py")}')
    print(banner)
    return 0


if __name__ == "__main__":
    sys.exit(main())
