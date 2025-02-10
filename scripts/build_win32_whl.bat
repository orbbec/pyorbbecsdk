@REM #!/bin/bash

@REM # Enter python virtual env
@REM source venv/bin/activate

@REM # Remove ./build directory
@REM cd ..
rmdir /s /q build

@REM # Create build directory and navigate into it
mkdir build
cd build

@REM # Run CMake
cmake -Dpybind11_DIR=$(pybind11-config) ..

@REM # Build Release with cmake
cmake --build . --config Release

@REM # Move back to the parent directory
cd ..

@REM # Remove old /install directory and create new /install/lib directory
rmdir /s /q install
mkdir -p ./install/lib/pyorbbecsdk/examples

@REM # Copy shared objects (*.pyd) from /build to /install/lib
robocopy ./build/Release/ ./install/lib/ *.pyd /E

@REM # Copy all c++ librarys except *.cmake to /install/lib
robocopy ./sdk/lib/win_x64/ ./install/lib/ /E

robocopy ./examples/ ./install/lib/pyorbbecsdk/examples /E

@REM # Run Python setup.py to build a wheel package
python3 setup.py bdist_wheel

@REM # Exit python virtual env
@REM deactivate

