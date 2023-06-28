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
# run examples
python examples/depth_viewer.py
```

Other examples can be found in `examples` directory, Please refer to [examples/README.md](examples/README.MD) for more.

### For Windows

Please refer to [docs/windows_readme.MD](docs/windows_readme.MD) for instructions on how to build and run the examples
on Windows.

## Documentation

TODO

## License

Apache License 2.0
