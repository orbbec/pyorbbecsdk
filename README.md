# Python binding for Orbbec SDK

A python binding for Orbbec SDK.

## Getting Started

### Get source code

```bash
git clone https://github.com/OrbbecDeveloper/pyorbbecsdk.git
```

### Install dependencies

```bash
sudo apt-get install python3-dev python3-venv python3-pip
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
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
# install udev rules
sudo bash ./scripts/install_udev_rules.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
# run examples
python3 examples/depth_viewer.py
```

Other examples can be found in `examples` directory, Please refer to [examples/README.md](examples/README.md) for more.

### For Windows

Please refer to [docs/README.md](docs/README_EN.md) for instructions on how to build and run the examples
on Windows.

## Documentation

Please refer to [docs/README.md](docs/README_EN.md) for more.

## License

Apache License 2.0
