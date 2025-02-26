#!/bin/bash

# Enter python virtual env
# source venv/bin/activate

# for py_version in cp38-cp38 cp39-cp39 cp310-cp310 cp311-cp311 cp312-cp312 cp313-cp313; do
    # export current python3 path
    export PATH=/opt/python/3.10.16/bin:$PATH
    export LD_LIBRARY_PATH=/opt/python/3.10.16/lib:$LD_LIBRARY_PATH

    # Remove ./build directory
    rm -rf ./build

    # Create build directory and navigate into it
    mkdir -p build && cd build

    # Run CMake
    cmake -Dpybind11_DIR=$(pybind11-config --cmakedir) ..

    # Build with make using 4 threads
    make -j$(nproc)

    # Move back to the parent directory
    cd ..

    # Remove old /install directory and create new /install/lib directory
    rm -rf ./install
    mkdir -p ./install/lib/pyorbbecsdk

    # Copy shared objects (*.so) from /build to /install/lib
    cp ./build/*.so ./install/lib/

    # Copy all files from /sdk/lib/arm64/ except *.cmake to /install/lib
    ARCH=$(uname -m)
    # Define source directory based on architecture
    if [ "$ARCH" == "aarch64" ]; then
        SRC_DIR="./sdk/lib/arm64"
    elif [ "$ARCH" == "x86_64" ]; then
        SRC_DIR="./sdk/lib/linux_x64"
    else
        echo "Unsupported architecture: $ARCH"
        exit 1
    fi
    #rsync -av --exclude='*.cmake' "$SRC_DIR/" ./install/lib/

    # Copy examples to /install/lib
    #cp -r ./examples ./install/lib/pyorbbecsdk
    #cp -r ./config ./install/lib/pyorbbecsdk
    #cp ./requirements.txt ./install/lib/pyorbbecsdk/examples
    #cp ./build/*.so ./install/lib/pyorbbecsdk/examples
    #rsync -av --exclude='*.cmake' "$SRC_DIR/" ./install/lib/pyorbbecsdk/examples


    # Run Python setup.py to build a wheel package
    python3 setup.py sdist bdist_wheel

    # Exit python virtual env
    # deactivate

#    echo "$py_version whl done!"
# done

echo "All whl generated!"
