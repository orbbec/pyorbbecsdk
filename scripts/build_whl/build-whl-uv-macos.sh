#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# uv-optimized pyorbbecsdk2 build script (macOS)
# ============================================================
# Features:
#   - Support command-line arguments for Python versions
#   - Offline mode support with --offline flag
#   - Configurable cleanup options
#   - Build single or multiple Python versions
#   - Uses clang/clang++ compilers
#   - Handles .dylib libraries
# ============================================================

# Ensure uv and its managed Python versions are in PATH
export PATH="$HOME/.local/bin:$PATH"
export UV_LINK_MODE=copy

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

# Cleanup tracking arrays
CLEANUP_FAILED=()
CLEANUP_SKIPPED=()

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

Build pyorbbecsdk wheel packages for specified Python versions (macOS).

Options:
  --offline       Offline mode, skip network downloads (requires local pybind11)
  --no-clean      Don't clean build directories before building
  --clean         Clean build directories before building (default)
  --clean-only    Only clean, don't build
  --yes, -y       Auto-confirm all cleanup prompts (non-interactive)
  -h, --help      Show this help message

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
# Get pybind11 directory
# ============================================================

get_pybind11_dir() {
    local PYVER="$1"

    if [ "$OFFLINE_MODE" = "true" ]; then
        # Offline mode: use local venv pybind11
        local VENV_PYBIND11="$ROOT_DIR/venv$(echo "$PYVER" | tr -d '.')/share/cmake/pybind11"
        if [ -d "$VENV_PYBIND11" ]; then
            echo "$VENV_PYBIND11"
        else
            echo "Error: Offline mode requires pybind11 in local venv" >&2
            echo "Expected path: $VENV_PYBIND11" >&2
            echo "" >&2
            echo "To set up offline environment, run:" >&2
            echo "  uv venv venv$(echo "$PYVER" | tr -d '.') --python $PYVER" >&2
            echo "  uv pip install pybind11 -e . --python venv$(echo "$PYVER" | tr -d '.')/bin/python" >&2
            echo "  (or use 'uv pip install pybind11' in the venv)" >&2
            exit 1
        fi
    else
        # Online mode: use uv run --with pybind11
        uv run --python "$PYVER" --with pybind11 python - <<'EOF'
import pybind11
print(pybind11.get_cmake_dir())
EOF
    fi
}

# ============================================================
# Main build logic
# ============================================================

build_version() {
    local PYVER="$1"

    echo
    echo "==========================================="
    echo " Building pyorbbecsdk for Python $PYVER (macOS)"
    echo "==========================================="

    local BUILD_DIR="$ROOT_DIR/build_$PYVER"

    # Per-version cleanup
    if [ "$CLEAN_BUILD" = "true" ]; then
        per_version_cleanup "$PYVER"
    else
        mkdir -p "$BUILD_DIR"
        mkdir -p "$SHARED_DST_DIR"
    fi

    # Resolve Python interpreter
    echo "Resolving Python interpreter..."
    # Ensure uv-managed Python is installed
    uv python install "$PYVER"
    local PYTHON_EXE
    # Use cd to avoid project .venv interfering with uv python find
    PYTHON_EXE="$(cd /tmp && uv python find "$PYVER")"
    echo "Using Python: $PYTHON_EXE"

    # Resolve pybind11 CMake directory
    echo "Resolving pybind11 CMake directory..."
    local PYBIND11_DIR
    PYBIND11_DIR="$(get_pybind11_dir "$PYVER")"
    echo "pybind11_DIR=$PYBIND11_DIR"

    # CMake configure & build (using clang for macOS)
    pushd "$BUILD_DIR" >/dev/null

    # Get Python paths for CMake (force specific Python version)
    local PYTHON_ROOT
    PYTHON_ROOT="$(dirname "$(dirname "$PYTHON_EXE")")"

    # Set minimum macOS deployment target for broader compatibility
    export MACOSX_DEPLOYMENT_TARGET=11.0

    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_PREFIX_PATH="$PYTHON_ROOT" \
        -DPython3_EXECUTABLE="$PYTHON_EXE" \
        -DPython3_ROOT_DIR="$PYTHON_ROOT" \
        -DPython3_FIND_STRATEGY=LOCATION \
        -DPython3_FIND_REGISTRY=NEVER \
        -Dpybind11_DIR="$PYBIND11_DIR" \
        -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
        -DCMAKE_C_COMPILER=clang \
        -DCMAKE_CXX_COMPILER=clang++

    cmake --build . --target install -j"$(sysctl -n hw.ncpu)"

    popd >/dev/null

    # Fix dylib permissions on macOS
    echo "Fixing dylib permissions..."
    find "$INSTALL_LIB_DIR" -name "*.dylib" -exec chmod 755 {} \; 2>/dev/null || true

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

    # Build wheel via uv
    echo "Building wheel..."
    uv build --wheel --python "$PYVER" --link-mode copy

    # macOS does not need auditwheel - copy wheel directly
    if [ -d "$ROOT_DIR/dist" ]; then
        cp "$ROOT_DIR"/dist/*.whl "$WHEEL_DIR/"
        rm -rf "$ROOT_DIR/dist"
    fi

    echo "Finished Python $PYVER"
}

# ============================================================
# Detect architecture & set DYLD_LIBRARY_PATH (macOS)
# ============================================================

setup_arch() {
    ARCH="$(uname -m)"
    case "$ARCH" in
        x86_64|arm64)
            export DYLD_LIBRARY_PATH="$ROOT_DIR/sdk/lib/macOS:${DYLD_LIBRARY_PATH:-}"
            ;;
        *)
            echo "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac
    echo "Architecture: $ARCH"
    echo "DYLD_LIBRARY_PATH: $DYLD_LIBRARY_PATH"
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
    remove_directory_safe "$ROOT_DIR/install" "install directory" || true
    remove_directory_safe "$ROOT_DIR/dist" "dist directory" || true

    # Remove egg-info directories
    find "$ROOT_DIR/src" -name "*.egg-info" -type d -print0 2>/dev/null | \
        while IFS= read -r -d '' dir; do
            remove_directory_safe "$dir" "$(basename "$dir")" || true
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