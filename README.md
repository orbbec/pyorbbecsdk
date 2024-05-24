# Python Bindings for Orbbec SDK

This project provides Python bindings for the Orbbec SDK, allowing developers to interface with Orbbec devices in Python.

## Getting Started

### Get the Source Code

Clone the repository to get the latest version of the Python bindings for Orbbec SDK.

```bash
git clone https://github.com/orbbec/pyorbbecsdk.git
```

### Install Dependencies

Install the necessary Python development packages on Ubuntu.

```bash
sudo apt-get install python3-dev python3-venv python3-pip python3-opencv
```

### Custom Python3 Path (Optional)

If you use Anaconda, set the Python3 path to the Anaconda path in `pyorbbecsdk/CMakeLists.txt` before the `find_package(Python3 REQUIRED COMPONENTS Interpreter Development)` line:

```cmake
set(Python3_ROOT_DIR "/home/anaconda3/envs/py3.6.8") # Replace with your Python3 path
set(pybind11_DIR "${Python3_ROOT_DIR}/lib/python3.6/site-packages/pybind11/share/cmake/pybind11") # Replace with your Pybind11 path
```

### Build the Project

Create a virtual environment and build the project.

```bash
cd pyorbbecsdk
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
mkdir build
cd build
cmake -Dpybind11_DIR=`pybind11-config --cmakedir` ..
make -j4
make install
```

### Try the Examples

Set up your environment to run examples and install necessary system rules.

```bash
cd pyorbbecsdk
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
sudo bash ./scripts/install_udev_rules.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
python3 examples/depth_viewer.py
python3 examples/net_device.py # Requires ffmpeg installation for network device
```

Additional examples are available in the `examples` directory. Please see [examples/README.md](examples/README.md) for further details.

### Generate Stubs

Generate Python stubs for better IntelliSense in your IDE.

```bash
source env.sh
pip3 install pybind11-stubgen
pybind11-stubgen pyorbbecsdk
```

### Building on Windows

For instructions on how to build and run the examples on Windows, please refer to [docs/README.md](docs/README_EN.md).

## Making a Python Wheel

Generate a wheel package for easy distribution and installation.

```bash
cd pyorbbecsdk
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
mkdir build
cd build
cmake -Dpybind11_DIR=`pybind11-config --cmakedir` ..
make -j4
make install
cd ..
pip3 install wheel
python3 setup.py bdist_wheel
pip3 install dist/*.whl
```

## Enabling Device Timestamps via UVC Protocol on Windows

To get device timestamps through the UVC protocol on a Windows system, you must modify the registry by completing a registration process. This is required due to default system limitations. Follow the steps below to configure your system:

### 1. Connect the Device
- Ensure your UVC-compatible device is connected to the computer and recognized by the system. Confirm that the device is online and functioning.

### 2. Open PowerShell with Administrator Privileges
- Open the Start menu, type `PowerShell`, right-click on the PowerShell app, and select 'Run as administrator'.

### 3. Navigate to the Scripts Directory
- Use the `cd` command to change the directory to the location of your scripts.
  ```powershell
  cd scripts
  ```

### 4. Modify Execution Policy
- Modify the PowerShell execution policy to allow script execution. Run the following command and press `Y` when prompted to confirm the change:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### 5. Execute the Registration Script
- Run the registration script to modify the registry settings. Use the following command:
  ```powershell
  .\obsensor_metadata_win10.ps1 -op install_all
  ```

This will complete the necessary registration and modification of settings to allow device timestamps via the UVC protocol on your Windows system.


## Documentation

For detailed documentation, please refer to [docs/README.md](docs/README_EN.md).

## License

This project is licensed under the Apache License 2.0.
