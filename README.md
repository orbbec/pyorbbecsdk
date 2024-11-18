# Python Bindings for Orbbec SDK

This branch provides Python bindings for the [Orbbec SDK v2.x](https://github.com/orbbec/OrbbecSDK_v2),  enabling developers to interface with Orbbec devices using Python. The Orbbec SDK v.2.x is an open-source cross-platform SDK library based on Orbbec RGB-D cameras. The differences between Orbbec SDK v2.x and [Orbbec SDK v1.x](https://github.com/orbbec/OrbbecSDK) can be found in the [README](https://github.com/orbbec/OrbbecSDK_v2).

## Hardware Products Supported by Python SDK

| **products list** | **firmware version**        |
| ----------------- | --------------------------- |
| Gemini 335        | 1.3.25                      |
| Gemini 335L       | 1.3.25                      |
| Gemini 336        | 1.3.25                      |
| Gemini 336L       | 1.3.25                      |
| Femto Bolt        | 1.0.6/1.0.9                 |
| Femto Mega        | 1.1.7/1.2.7                 |
| Astra 2           | 2.8.20                      |
| Gemini 2 L        | 1.4.32                      |
| Gemini 2          | 1.4.60 /1.4.76              |


## Getting Started

### Clone the Repository
Clone the repository to get the latest version:
```bash
git clone https://github.com/orbbec/pyorbbecsdk.git
git checkout OrbbecSDK_V2.x
```

### Install Dependencies (Ubuntu)
Install the necessary Python development packages:
```bash
sudo apt-get install python3-dev python3-venv python3-pip python3-opencv
```

### Custom Python Path (Optional)
If you use Anaconda, update the Python path in `pyorbbecsdk/CMakeLists.txt` before the `find_package(Python3 REQUIRED COMPONENTS Interpreter Development)` line:
```cmake
set(Python3_ROOT_DIR "/home/anaconda3/envs/py3.6.8") # Replace with your Python path
set(pybind11_DIR "${Python3_ROOT_DIR}/lib/python3.6/site-packages/pybind11/share/cmake/pybind11") # Replace with your Pybind11 path
```

### Build the Project
Create a virtual environment and build the project:
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

### Run the Examples
Set up the environment and run the examples:
```bash
cd pyorbbecsdk
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
sudo bash ./scripts/install_udev_rules.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
python3 examples/depth_viewer.py
python3 examples/net_device.py # Requires ffmpeg installation for network devices
```

Additional examples are available in the `examples` directory. Refer to [examples/README.md](examples/README.md) for further details.

### Generate Python Stubs
Generate stubs for better IntelliSense support in your IDE:
```bash
source env.sh
pip3 install pybind11-stubgen
pybind11-stubgen pyorbbecsdk
```

### Building on Windows
Refer to [docs/README.md](docs/README_EN.md) for instructions on building and running examples on Windows.

## Making a Python Wheel
To generate a wheel package for easy distribution:
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
To enable device timestamps via the UVC protocol on Windows, modify the system registry as follows:

### Steps to Modify the Registry
1. **Connect the Device**: Ensure the UVC-compatible device is connected and recognized.
2. **Open PowerShell with Administrator Privileges**: Open PowerShell as an administrator.
3. **Navigate to the Scripts Directory**:
   ```powershell
   cd scripts
   ```
4. **Modify the Execution Policy**: Allow script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
5. **Execute the Registration Script**: Modify the registry settings:
   ```powershell
   .\obsensor_metadata_win10.ps1 -op install_all
   ```

## Documentation
Refer to [docs/README.md](docs/README_EN.md) for detailed documentation.

## License
This project is licensed under the Apache License 2.0.

