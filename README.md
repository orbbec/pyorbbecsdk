# Python binding for Orbbec SDK

A python binding for Orbbec SDK.

## Getting Started

### Get source code

```bash
git clone https://github.com/orbbec/pyorbbecsdk.git
```

### Install dependencies

```bash
sudo apt-get install python3-dev python3-venv python3-pip python3-opencv
```
### Custom Python3 path (optional)
If you use Anaconda, you can set the python3 path to the Anaconda path. Put below code in `pyorbbecsdk/CMakeLists.txt`
before `find_package(Python3 REQUIRED COMPONENTS Interpreter Development)`.

```cmake
set(Python3_ROOT_DIR "/home/anaconda3/envs/py3.6.8") # replace by your python3 path
set(pybind11_DIR "${Python3_ROOT_DIR}/lib/python3.6/site-packages/pybind11/share/cmake/pybind11") # replace by your pybind11 path
```

### Build

```bash
cd pyorbbecsdk
# Strongly recommended create virtual environment.
python3 -m venv  ./venv
source venv/bin/activate # activate virtual environment
pip3 install -r requirements.txt
mkdir build
cd build
cmake -Dpybind11_DIR=`pybind11-config --cmakedir` ..
make -j4
make install
```

### Try examples

```bash
cd pyorbbecsdk
# set PYTHONPATH environment variable to include the lib directory in the install directory
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/ # DON'T forget do this
# install udev rules
sudo bash ./scripts/install_udev_rules.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
# run examples
python3 examples/depth_viewer.py
# network device, you need install ffmpeg
python3 examples/net_device.py
```

Other examples can be found in `examples` directory, Please refer to [examples/README.md](examples/README.md) for more.
### Generate stubs

```bash
source env.sh
pip3 install pybind11-stubgen
pybind11-stubgen  pyorbbecsdk
```


### For Windows

Please refer to [docs/README.md](docs/README_EN.md) for instructions on how to build and run the examples
on Windows.

## Documentation

Please refer to [docs/README.md](docs/README_EN.md) for more.

## License

Apache License 2.0
