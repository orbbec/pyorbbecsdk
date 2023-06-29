# Python binding for Orbbec SDK

A python binding for Orbbec SDK.

## Getting Started

### Get source code

In the command prompt:

```bash
git clone https://github.com/OrbbecDeveloper/pyorbbecsdk.git
```

### Install dependencies

```bash
cd pyorbbecsdk
pip install -r requirements.txt
```

To install `python3-dev`  you can follow the instructions provided on their respective websites.

### Build

CMake is required to build the project. First, create a new directory called `build` and navigate into it:

```bash
mkdir build
cd build
```

Then, build the project using CMake:

```bash
cmake -G "Visual Studio 16 2019" -A x64 ..
```

Replace `"Visual Studio 16 2019"` with your specific version of Visual Studio.

To compile the code:

```bash
cmake --build . --config Release
```

Finally, to install the compiled binaries:

```bash
cmake --install .
```

### Try examples

To try the examples, navigate to the `pyorbbecsdk` directory and set the `PYTHONPATH` environment variable to include
the `lib` directory in the `install` directory:

```bash
cd pyorbbecsdk
set PYTHONPATH=%PYTHONPATH%;%cd%\install\lib\
python examples\depth_viewer.py
```

Please note that these commands are for the Command Prompt. If you're using PowerShell, you may need to adjust the
commands accordingly.

Also, please ensure that you have all the required software (like git, python, pip, cmake, and Visual Studio) installed
on your Windows machine.
