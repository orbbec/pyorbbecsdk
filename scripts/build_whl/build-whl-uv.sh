#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# uv-optimized pyorbbecsdk2 build script (Linux)
# ============================================================
# Features:
#   - Support command-line arguments for Python versions
#   - Offline mode support with --offline flag
#   - Configurable cleanup options
#   - Build single or multiple Python versions
# ============================================================

export UV_LINK_MODE=copy

# Ensure uv and its managed Python versions are in PATH
export PATH="$HOME/.local/bin:$PATH"

# Set UV offline mode if requested
UV_OFFLINE="${UV_OFFLINE:-}"

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# ============================================================
# Default configuration
# ============================================================

# Default Python versions to build
PYTHON_VERSIONS=()

# Build options
OFFLINE_MODE=false
CLEAN_BUILD=true
CLEAN_ONLY=false
AUTO_CONFIRM=false
NO_SYNC=false

# manylinux version to use for the wheel tag (default: 2_27)
MANYLINUX_VERSION="${MANYLINUX_VERSION:-2.27}"

# Cleanup tracking arrays
CLEANUP_FAILED=()
CLEANUP_SKIPPED=()

# Per-version venv directories created by THIS run (for final cleanup).
# Only these are removed at the end; pre-existing venv<ver> dirs are left alone.
CREATED_VENVS=()

# Directory paths
WHEEL_DIR="$ROOT_DIR/wheel"
INSTALL_DIR="$ROOT_DIR/install"
INSTALL_LIB_DIR="$INSTALL_DIR/lib/pyorbbecsdk"
SHARED_DST_DIR="$INSTALL_LIB_DIR/shared"
ENV_SETUP_SRC="$ROOT_DIR/scripts/env_setup"

# ============================================================
# Usage function
# ============================================================

show_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [VERSION...]

Build pyorbbecsdk wheel packages for specified Python versions.

Options:
  --offline       Offline mode, skip network downloads (requires local pybind11)
  --no-clean      Don't clean build directories before building
  --clean         Clean build directories before building (default)
  --clean-only    Only clean, don't build
  --yes, -y       Auto-confirm all cleanup prompts (non-interactive)
  --no-sync       Use the currently activated virtual environment instead of
                  recreating venv<ver> and running uv sync. Requires an active
                  venv (VIRTUAL_ENV must be set); pybind11 is used as-is.
  -h, --help      Show this help message

Environment:
  MANYLINUX_VERSION  manylinux version for wheel tag (default: 2.27, use "2.27" for manylinux_2_27)

Arguments:
  VERSION         Python version (e.g., 3.10, 3.11) or 'all' for 3.8-3.13

Examples:
  $(basename "$0") 3.10                    # Build Python 3.10
  $(basename "$0") 3.8 3.9 3.10            # Build multiple versions
  $(basename "$0") all                     # Build all versions (3.8-3.13)
  $(basename "$0") --offline 3.10          # Offline build
  $(basename "$0") --clean all             # Clean and build all versions
  $(basename "$0") --clean-only            # Clean only, don't build
  $(basename "$0") all --yes               # Build all versions, auto-confirm cleanups
EOF
}

# ============================================================
# Parse command-line arguments
# ============================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --offline)
                OFFLINE_MODE=true
                export UV_OFFLINE=1
                shift
                ;;
            --no-clean)
                CLEAN_BUILD=false
                shift
                ;;
            --clean)
                CLEAN_BUILD=true
                shift
                ;;
            --clean-only)
                CLEAN_ONLY=true
                shift
                ;;
            --yes|-y)
                AUTO_CONFIRM=true
                shift
                ;;
            --no-sync)
                NO_SYNC=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            all)
                # Build all supported Python versions (3.8-3.13)
                PYTHON_VERSIONS=("3.8" "3.9" "3.10" "3.11" "3.12" "3.13")
                shift
                ;;
            3.*)
                PYTHON_VERSIONS+=("$1")
                shift
                ;;
            *)
                echo "Error: Unknown option or version: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Default to 3.10 if no versions specified
    if [[ ${#PYTHON_VERSIONS[@]} -eq 0 ]]; then
        PYTHON_VERSIONS=("3.10")
    fi
}

# ============================================================
# Cleanup functions
# ============================================================

# Safe remove directory - tracks failures
remove_directory_safe() {
    local path="$1"
    local name="$2"

    if [ ! -e "$path" ]; then
        return 0
    fi

    if rm -rf "$path" 2>/dev/null; then
        echo "    Deleted: $name"
        return 0
    else
        echo "    Failed to delete: $name" >&2
        CLEANUP_FAILED+=("$name ($path)")
        return 1
    fi
}

# Check and confirm deletion of a single path
confirm_delete() {
    local path="$1"
    local name="$2"

    if [ ! -e "$path" ]; then
        return 0
    fi

    if [ "$AUTO_CONFIRM" = "true" ]; then
        return $(remove_directory_safe "$path" "$name"; echo $?)
    fi

    echo -n "  Found: $name - delete? (y=yes/n=no/a=all/s=skip-all): "
    read -r response

    case "$response" in
        y|Y)
            return $(remove_directory_safe "$path" "$name"; echo $?)
            ;;
        a|A)
            AUTO_CONFIRM=true
            return $(remove_directory_safe "$path" "$name"; echo $?)
            ;;
        s|S)
            echo "    Skipped: $name"
            CLEANUP_SKIPPED+=("$name ($path)")
            return 1
            ;;
        *)
            echo "    Skipped: $name"
            CLEANUP_SKIPPED+=("$name ($path)")
            return 1
            ;;
    esac
}

# Interactive cleanup confirmation
interactive_cleanup() {
    echo ">>> Checking for existing build artifacts to clean"
    echo ""

    # Define paths to check
    local paths_to_check=(
        "$ROOT_DIR/build:build directory"
        "$ROOT_DIR/dist:dist directory"
        "$ROOT_DIR/install:install directory"
        "$ROOT_DIR/wheel:wheel directory"
    )

    # Check for build_* directories
    for dir in "$ROOT_DIR"/build_*; do
        if [ -d "$dir" ]; then
            local dirname
            dirname="$(basename "$dir")"
            paths_to_check+=("$dir:$dirname directory")
        fi
    done

    # Check if anything exists
    local has_items=false
    for item in "${paths_to_check[@]}"; do
        local path="${item%%:*}"
        if [ -e "$path" ]; then
            has_items=true
            break
        fi
    done

    if [ "$has_items" = "false" ]; then
        echo "  No build artifacts found, nothing to clean."
        echo ""
        mkdir -p "$ROOT_DIR/wheel"
        return
    fi

    # Process each path
    local skip_all=false
    for item in "${paths_to_check[@]}"; do
        local path="${item%%:*}"
        local name="${item#*:}"

        if [ "$skip_all" = "true" ]; then
            echo "  Skipped: $name"
            CLEANUP_SKIPPED+=("$name ($path)")
            continue
        fi

        if [ "$AUTO_CONFIRM" = "true" ]; then
            remove_directory_safe "$path" "$name"
            continue
        fi

        if [ -e "$path" ]; then
            echo -n "  Found: $name - delete? (y=yes/n=no/d=this dir only/s=skip-all/a=allow-all): "
            read -r response

            case "$response" in
                y|Y)
                    remove_directory_safe "$path" "$name"
                    ;;
                d|D)
                    remove_directory_safe "$path" "$name"
                    skip_all=true
                    ;;
                a|A)
                    AUTO_CONFIRM=true
                    remove_directory_safe "$path" "$name"
                    ;;
                s|S)
                    echo "    Skipped: $name"
                    CLEANUP_SKIPPED+=("$name ($path)")
                    skip_all=true
                    ;;
                *)
                    echo "    Skipped: $name"
                    CLEANUP_SKIPPED+=("$name ($path)")
                    ;;
            esac
        fi
    done

    echo ""
    mkdir -p "$ROOT_DIR/wheel"
}

# Per-version cleanup
per_version_cleanup() {
    local PYVER="$1"
    local BUILD_DIR="$ROOT_DIR/build_$PYVER"

    echo "  Cleaning build artifacts for Python $PYVER..."

    remove_directory_safe "$BUILD_DIR" "build_$PYVER directory" || true
    remove_directory_safe "$INSTALL_DIR" "install directory" || true
    remove_directory_safe "$ROOT_DIR/dist" "dist directory" || true

    mkdir -p "$BUILD_DIR"
    mkdir -p "$SHARED_DST_DIR"
}

# ============================================================
# Install Python version via uv
# ============================================================

install_python_version() {
    local PYVER="$1"

    echo "Resolving Python interpreter..." >&2
    # Ensure uv-managed Python is installed
    uv python install "$PYVER" >&2
    local python_exe
    # Use cd to avoid project .venv interfering with uv python find
    python_exe=$(cd /tmp && uv python find "$PYVER")
    if [ -z "$python_exe" ] || [ ! -x "$python_exe" ]; then
        echo "Failed to find Python ${PYVER} after installation." >&2
        exit 1
    fi
    echo "Using Python: $python_exe" >&2
    echo "$python_exe"
}

# ============================================================
# Get pybind11 directory
# ============================================================

# Get the per-version venv path (e.g. "3.10" -> $ROOT_DIR/venv310)
get_venv_path() {
    echo "$ROOT_DIR/venv$(echo "$1" | tr -d '.')"
}

# Get the python executable inside the per-version venv
get_venv_python() {
    echo "$(get_venv_path "$1")/bin/python"
}

# Validate that a virtual environment is activated (for --no-sync mode).
# Returns the python executable path of the active venv, or exits on error.
active_venv_python() {
    if [ -z "${VIRTUAL_ENV:-}" ]; then
        echo "Error: --no-sync requires an activated virtual environment." >&2
        echo "  Please activate a venv first, e.g. 'source venv310/bin/activate' or" >&2
        echo "  'uv venv .venv && .venv/Scripts/activate' (Windows), then re-run." >&2
        exit 1
    fi

    local py
    if [ -x "$VIRTUAL_ENV/bin/python" ]; then
        py="$VIRTUAL_ENV/bin/python"
    elif [ -x "$VIRTUAL_ENV/Scripts/python.exe" ]; then
        py="$VIRTUAL_ENV/Scripts/python.exe"
    else
        echo "Error: No python executable found in activated venv '$VIRTUAL_ENV'." >&2
        exit 1
    fi

    echo "$py"
}

# Get pybind11 CMake dir from the currently activated venv (--no-sync mode).
# Uses the active venv's pybind11 as-is; does not install or pin a version.
active_pybind11_dir() {
    local py
    py="$(active_venv_python)"
    "$py" -c "import pybind11; print(pybind11.get_cmake_dir())"
}

# Recreate the per-version venv (delete + uv venv) for reproducible automated builds
create_version_venv() {
    local PYVER="$1"
    local VENV_DIR
    VENV_DIR="$(get_venv_path "$PYVER")"

    echo "  Recreating venv for Python $PYVER..." >&2
    rm -rf "$VENV_DIR"
    mkdir -p "$(dirname "$VENV_DIR")"

    uv venv "$VENV_DIR" --python "$PYVER" >&2
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create venv for Python $PYVER" >&2
        exit 1
    fi

    if [ ! -x "$(get_venv_python "$PYVER")" ]; then
        echo "Error: venv for Python $PYVER created but python not found" >&2
        exit 1
    fi

    echo "$VENV_DIR"
}

get_pybind11_dir() {
    local PYVER="$1"
    local VENV_PYTHON
    VENV_PYTHON="$(get_venv_python "$PYVER")"

    # Install pinned pybind11 into the per-version venv (matches pyproject.toml
    # [build-system].requires) so the CMake compile environment matches the
    # packaging environment.
    echo "  Installing pybind11==2.12.0 into venv for Python $PYVER..." >&2
    uv pip install pybind11==2.12.0 --python "$VENV_PYTHON" >&2
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install pybind11 into venv for Python $PYVER" >&2
        exit 1
    fi

    "$VENV_PYTHON" -c "import pybind11; print(pybind11.get_cmake_dir())"
}

# ============================================================
# Main build logic
# ============================================================

build_version() {
    local PYVER="$1"

    echo
    echo "==========================================="
    echo " Building pyorbbecsdk for Python $PYVER"
    echo "==========================================="

    local BUILD_DIR="$ROOT_DIR/build_$PYVER"

    # Per-version cleanup
    if [ "$CLEAN_BUILD" = "true" ]; then
        per_version_cleanup "$PYVER"
    else
        mkdir -p "$BUILD_DIR"
        mkdir -p "$SHARED_DST_DIR"
    fi

    # In --no-sync mode, use the currently activated venv as-is (no recreate,
    # no pinned pybind11, no uv sync). Otherwise recreate the per-version venv
    # for reproducible automated builds.
    local VENV_DIR VENV_PYTHON PYBIND11_DIR
    if [ "$NO_SYNC" = "true" ]; then
        echo "  --no-sync: using activated venv (no venv recreation, no uv sync)"
        VENV_PYTHON="$(active_venv_python)"
        VENV_DIR="$(dirname "$(dirname "$VENV_PYTHON")")"
        echo "  Using active venv Python: $VENV_PYTHON"

        # Resolve pybind11 from the active venv (use as-is, not pinned)
        echo "Resolving pybind11 CMake directory from active venv..."
        PYBIND11_DIR="$(active_pybind11_dir)"
        echo "pybind11_DIR=$PYBIND11_DIR"
    else
        # Recreate the per-version venv (delete + uv venv) for reproducible builds.
        # Ensures no stale packages from previous runs leak into the build.
        VENV_DIR="$(create_version_venv "$PYVER")"
        # Track this venv so final_cleanup removes only what this run created.
        # NOTE: must record here (parent shell), not inside create_version_venv,
        # because $() runs the function in a subshell and the append would be lost.
        CREATED_VENVS+=("$VENV_DIR")

        # Resolve Python interpreter (auto-install if needed)
        echo "Resolving Python interpreter..."
        local PYTHON_EXE
        PYTHON_EXE="$(install_python_version "$PYVER")"
        echo "Using Python: $PYTHON_EXE"

        # Use the per-version venv python for CMake, so pybind11 (installed into the
        # venv) and the Python headers/libs come from the same interpreter.
        VENV_PYTHON="$(get_venv_python "$PYVER")"
        echo "Using venv Python for build: $VENV_PYTHON"

        # Resolve pybind11 CMake directory (installs pinned pybind11 into the venv)
        echo "Resolving pybind11 CMake directory..."
        PYBIND11_DIR="$(get_pybind11_dir "$PYVER")"
        echo "pybind11_DIR=$PYBIND11_DIR"
    fi

    # CMake configure & build (using gcc for Linux)
    pushd "$BUILD_DIR" >/dev/null

    # Get Python paths for CMake (force specific Python version)
    local PYTHON_ROOT
    PYTHON_ROOT="$(dirname "$(dirname "$VENV_PYTHON")")"

    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_PREFIX_PATH="$PYTHON_ROOT" \
        -DPython3_EXECUTABLE="$VENV_PYTHON" \
        -DPython3_ROOT_DIR="$PYTHON_ROOT" \
        -DPython3_FIND_STRATEGY=LOCATION \
        -DPython3_FIND_REGISTRY=NEVER \
        -Dpybind11_DIR="$PYBIND11_DIR" \
        -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
        -DCMAKE_C_COMPILER=gcc \
        -DCMAKE_CXX_COMPILER=g++

    cmake --build . --target install -j"$(nproc)"

    popd >/dev/null

    # Copy extra runtime files
    echo "Copying extra runtime files..."

    if [ -d "$ROOT_DIR/examples" ]; then
        cp -r "$ROOT_DIR/examples" "$INSTALL_LIB_DIR/"
    fi

    if [ -d "$ROOT_DIR/config" ]; then
        cp -r "$ROOT_DIR/config" "$INSTALL_LIB_DIR/"
    fi

    if [ -f "$ROOT_DIR/requirements.txt" ]; then
        mkdir -p "$INSTALL_LIB_DIR/examples"
        cp "$ROOT_DIR/requirements.txt" "$INSTALL_LIB_DIR/examples/"
    fi

    if [ -d "$ENV_SETUP_SRC" ]; then
        cp "$ENV_SETUP_SRC"/*.rules "$SHARED_DST_DIR/" 2>/dev/null || true
        cp "$ENV_SETUP_SRC"/*.sh    "$SHARED_DST_DIR/" 2>/dev/null || true
        cp "$ENV_SETUP_SRC"/setup_env.py "$SHARED_DST_DIR/" 2>/dev/null || true
    fi

    # Copy pyi stub files
    echo "Copying pyi stub files..."
    STUBS_DIR="$ROOT_DIR/stubs"
    if [ -d "$STUBS_DIR" ]; then
        # Copy __init__.pyi and pyorbbecsdk.pyi
        for pyi_file in "__init__.pyi" "pyorbbecsdk.pyi"; do
            if [ -f "$STUBS_DIR/$pyi_file" ]; then
                cp "$STUBS_DIR/$pyi_file" "$INSTALL_LIB_DIR/"
                echo "  Copied $pyi_file"
            else
                echo "  Warning: $pyi_file not found in $STUBS_DIR"
            fi
        done
    else
        echo "  Warning: stubs directory not found at $STUBS_DIR"
    fi

    # Sync runtime dependencies + project into the per-version venv.
    # CMake has already produced install/lib, so the editable install of
    # pyorbbecsdk2 (which copies install/lib) will succeed.
    # In --no-sync mode this step is skipped; the active venv is used as-is.
    if [ "$NO_SYNC" = "true" ]; then
        echo "  --no-sync: skipping uv sync (using active venv as-is)"
    else
        echo "Syncing dependencies via uv sync into $VENV_DIR..."
        # --no-install-project: install dependencies only. Installing the
        # project editable would run setup.py build_ext, whose output dir
        # resolves to src/pyorbbecsdk/ and pollutes the source tree.
        UV_PROJECT_ENVIRONMENT="$VENV_DIR" uv sync --no-install-project --python "$PYVER" >&2
        if [ $? -ne 0 ]; then
            echo "Error: uv sync failed (Python $PYVER)" >&2
            exit 1
        fi
    fi

    # Build wheel via uv. Point --python at the venv's python executable so the
    # wheel is tagged for the correct CPython version. In normal mode $VENV_PYTHON
    # is venv<ver>/bin/python; in --no-sync mode it is the activated venv python.
    # A bare version number would re-resolve a system interpreter, and omitting
    # it lets the build backend pick the project .venv (wrong Python).
    echo "Building wheel..."
    UV_PROJECT_ENVIRONMENT="$VENV_DIR" uv build --wheel --python "$VENV_PYTHON" --link-mode copy
    if [ $? -ne 0 ]; then
        echo "Error: uv build failed (Python $PYVER)" >&2
        exit 1
    fi

    # auditwheel (skip py38 if needed)
    if [ -d "$ROOT_DIR/dist" ]; then
        if [[ "$PYVER" != "3.8" ]]; then
            echo "Repairing wheel with auditwheel..."
            # --no-project: run auditwheel in an isolated env without linking the
            # current project (which would editable-install it and pollute src/).
            uv run --no-project --python "$PYVER" --with auditwheel auditwheel repair "."/dist/*.whl \
                --exclude libEGL* \
                --exclude libGLES* \
                --exclude libGL* \
                --exclude libOrbbecSDK.so* \
                --exclude libdepthengine.so* \
                --exclude libFilterProcessor.so \
                --exclude libob_*.so \
                --exclude libfirmwareupdater.so \
                --exclude libob_frame_processor.so \
                --exclude libnvinfer.so.10 \
                --exclude libnvinfer_plugin.so.10 \
                --exclude libnvonnxparser.so.10 \
                --exclude libcudart.so.* \
                --exclude libcudart_* \
                -w "$ROOT_DIR/dist/"
        fi

        # Force-retag the manylinux platform tag after build.
        # auditwheel may produce tags like manylinux_2_31_x86_64 or manylinux_2_28_x86_64
        # depending on the system's glibc version. Force-rewrite it to the specified
        # manylinux version (default 2.27) to match the target compatibility.
        local plat_tag
        plat_tag="manylinux_${MANYLINUX_VERSION}_${ARCH}"
        plat_tag="${plat_tag//./_}"  # Replace dots with underscores for manylinux tag format
        echo "Force-retagging wheel platform tag to $plat_tag..."
        ( cd "$ROOT_DIR/dist" && \
          uv run --no-project --with wheel wheel tags --platform-tag "$plat_tag" --remove *.whl )

        cp "$ROOT_DIR"/dist/*.whl "$WHEEL_DIR/"
        rm -rf "$ROOT_DIR/dist"
    fi

    echo "Finished Python $PYVER"
}

# ============================================================
# Detect architecture & set LD_LIBRARY_PATH
# ============================================================

setup_arch() {
    ARCH="$(uname -m)"
    case "$ARCH" in
        x86_64)
            export LD_LIBRARY_PATH="$ROOT_DIR/sdk/lib/linux_x64:${LD_LIBRARY_PATH:-}"
            ;;
        aarch64)
            export LD_LIBRARY_PATH="$ROOT_DIR/sdk/lib/arm64:${LD_LIBRARY_PATH:-}"
            ;;
        *)
            echo "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac
}

# ============================================================
# Final cleanup
# ============================================================

final_cleanup() {
    echo
    echo ">>> Final cleanup..."

    # Remove build_* directories
    for dir in "$ROOT_DIR"/build_*; do
        if [ -d "$dir" ]; then
            local dirname
            dirname="$(basename "$dir")"
            remove_directory_safe "$dir" "$dirname directory" || true
        fi
    done

    remove_directory_safe "$ROOT_DIR/build" "build directory" || true
    remove_directory_safe "$ROOT_DIR/dist" "dist directory" || true

    # In --no-sync mode we use the user's activated venv, so keep install/
    # (the compiled C++ artifacts) for them to inspect/use. Otherwise remove it.
    if [ "$NO_SYNC" = "true" ]; then
        echo "  --no-sync: keeping install directory for the active venv build"
    else
        remove_directory_safe "$ROOT_DIR/install" "install directory" || true
    fi

    # Remove egg-info directories
    find "$ROOT_DIR/src" -name "*.egg-info" -type d -print0 2>/dev/null | \
        while IFS= read -r -d '' dir; do
            remove_directory_safe "$dir" "$(basename "$dir")" || true
        done

    # Remove __pycache__ dirs left under src/ by the build
    find "$ROOT_DIR/src" -name "__pycache__" -type d -print0 2>/dev/null | \
        while IFS= read -r -d '' dir; do
            rm -rf "$dir" 2>/dev/null || true
        done

    # Remove only the per-version venv dirs THIS run created. Pre-existing
    # venv<ver> dirs (e.g. from an earlier manual setup) are left untouched.
    for venv_dir in "${CREATED_VENVS[@]}"; do
        remove_directory_safe "$venv_dir" "$(basename "$venv_dir")" || true
    done
}

# Show cleanup report
show_cleanup_report() {
    echo ""
    echo "==========================================="

    if [ ${#CLEANUP_FAILED[@]} -eq 0 ] && [ ${#CLEANUP_SKIPPED[@]} -eq 0 ]; then
        echo " Cleanup completed successfully"
        echo " All temporary files were removed"
    else
        if [ ${#CLEANUP_FAILED[@]} -gt 0 ]; then
            echo " Cleanup completed with FAILURES:"
            echo ""
            echo "  Failed to delete the following items:"
            for item in "${CLEANUP_FAILED[@]}"; do
                echo "    - $item"
            done
        fi

        if [ ${#CLEANUP_SKIPPED[@]} -gt 0 ]; then
            echo ""
            echo "  Skipped the following items (user requested):"
            for item in "${CLEANUP_SKIPPED[@]}"; do
                echo "    - $item"
            done
        fi

        echo ""
        echo "  You may need to manually remove these files/directories"
        echo "  or run the script with --clean-only to try again."
    fi

    echo ""
    echo " Wheels are located in: $WHEEL_DIR"
    echo "==========================================="
}

# ============================================================
# Main entry point
# ============================================================

main() {
    parse_args "$@"

    # Setup architecture
    setup_arch

    # Global cleanup (always run first)
    if [ "$CLEAN_BUILD" = "true" ]; then
        interactive_cleanup
    else
        mkdir -p "$ROOT_DIR/wheel"
    fi

    # Clean only mode
    if [ "$CLEAN_ONLY" = "true" ]; then
        show_cleanup_report
        echo ""
        echo ">>> Clean completed (no build requested)"
        exit 0
    fi

    # Build each version
    for PYVER in "${PYTHON_VERSIONS[@]}"; do
        build_version "$PYVER"
    done

    # Final cleanup
    final_cleanup

    # Show final report
    show_cleanup_report
}

# Run main
main "$@"
