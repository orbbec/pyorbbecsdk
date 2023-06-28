# Python binding for Orbbec SDK

A python binding for Orbbec SDK.

## Getting Started

### Get source code

```bash
git clone https://github.com/OrbbecDeveloper/pyorbbecsdk.git
```

### Install dependencies

```bash
sudo apt install python3-dev pybind11-dev
cd pyorbbecsdk
pip install -r requirements.txt
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
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/lib/
python examples/depth_viewer.py
```

Other examples can be found in `examples` directory.

### For Windows

Please refer to [docs/windows_readme.MD](docs/windows_readme.MD) for instructions on how to build and run the examples
on Windows.

## Documentation

TODO

## License

Apache License 2.0
