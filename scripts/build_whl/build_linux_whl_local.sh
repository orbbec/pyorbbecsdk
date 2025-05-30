#!/bin/bash
echo $PYTHON3_EXECUTABLE
echo $PYTHON3_INCLUDE_DIR
echo $PYTHON3_LIBRARY
python3 --version
pip3 --version
which python3
which python3.10
which pybind11

# Enter python virtual env
# source venv/bin/activate

# Remove ./build directory
rm -rf ./build
# Remove old /install directory
rm -rf ./install

# Create build directory and navigate into it
mkdir -p build && cd build

# Run CMake
cmake -Dpybind11_DIR=$(pybind11-config --cmakedir) ..

# Build with make using 4 threads
make -j$(nproc)

make install

# Move back to the parent directory
cd ..

# Create new /install/lib directory
mkdir -p ./install/lib/pyorbbecsdk

# Copy examples to /install/lib
cp -r ./examples ./install/lib/pyorbbecsdk
cp -r ./config ./install/lib/pyorbbecsdk
cp ./requirements.txt ./install/lib/pyorbbecsdk/examples

# Run Python setup.py to build a wheel package
python3 setup.py sdist bdist_wheel

# Exit python virtual env
# deactivate
