# Python binding for Orbbec SDK

A python binding for Orbbec SDK.

## Getting Started

### Get source code

```bash
git clone https://github.com/OrbbecDeveloper/pyorbbecsdk.git
```

### Install dependencies

```bash
sudo apt-get install python3-dev pybind11-dev python3-venv python3-pip
```

### Build

```bash
mkdir build
cd build
cmake ..
make -j4
make install
```

### Try examples

```bash
cd pyorbbecsdk
# set PYTHONPATH environment variable to include the lib directory in the install directory
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
# Skip this if you don't want virtual environment
python3 -m venv  ./venv
source ./venv/bin/activate
# install dependencies
pip install -r requirements.txt
# install udev rules
sudo bash ./scripts/install_udev_rules.sh
# run examples
python examples/depth_viewer.py
```

Other examples can be found in `examples` directory, Please refer to [examples/README.md](examples/README.md) for more.

### For Windows

Please refer to [docs/README.md](docs/README_EN.md) for instructions on how to build and run the examples
on Windows.

## Documentation

Please refer to [docs/README.md](docs/README_EN.md) for more.

## License

Apache License 2.0
