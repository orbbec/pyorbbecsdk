#!/bin/bash

# List of Python versions to build wheels for
PYTHON_VERSIONS=("3.6.8" "3.7.9" "3.8.5" "3.9.1")
CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SOURCE_DIR="$CURR_DIR/.."

# Ensure pyenv is initialized
if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
else
    echo "pyenv not found. Please install pyenv and pyenv-virtualenv."
    exit 1
fi

# Directory to store wheels
WHEELHOUSE="${SOURCE_DIR}/wheelhouse"
mkdir -p "$WHEELHOUSE"

# Base pyorbbecsdk directory
BASE_PYORBECSDK_DIR="${SOURCE_DIR}"

# Create a build directory
BUILD_DIR="${SOURCE_DIR}/build"
mkdir -p "$BUILD_DIR"

for version in "${PYTHON_VERSIONS[@]}"; do
    echo "Setting up Python $version"
    pyenv install -s "$version"
    WORK_DIR="${BUILD_DIR}/pyorbbecsdk_${version}"
    mkdir -p "$WORK_DIR"
    
    # Define the list of directories and files to copy
    ITEMS_TO_COPY=("src" "cmake"  "setup.py" "CMakeLists.txt")

    # Copy each item in the list
    for item in "${ITEMS_TO_COPY[@]}"; do
        cp -r "${BASE_PYORBECSDK_DIR}/${item}" "${WORK_DIR}/"
    done

    pyenv virtualenv -f "$version" "pyorbbecsdk_$version"
    pyenv activate "pyorbbecsdk_$version"

    # Navigate to specific version directory
    cd "$WORK_DIR"

    # Install requirements
    pip install -U pip setuptools wheel
    pip install pybind11==2.11.0 pybind11-global==2.11.0

    # Configure and build with CMake
    mkdir -p build
    cd build
    cmake -Dpybind11_DIR=`pybind11-config --cmakedir` ..
    make -j4
    make install

    # Navigate back to Python version directory to build wheel
    cd ..

    # Build wheel
    python setup.py bdist_wheel

    # Check if wheel was created successfully
    if [ $? -eq 0 ]; then
        # Move wheel to a central directory
        mv dist/*.whl "$WHEELHOUSE/"
    else
        echo "Building wheel failed for Python $version."
        break
    fi

    # Clean up and deactivate virtual environment
    pyenv deactivate
    rm -rf "$WORK_DIR"  # Remove the specific version directory
done

# Remove the build directory after completion
rm -rf "$BUILD_DIR"

# Reset pyenv local settings
pyenv local --unset
