# Orbbec SDK Python Bindings
__version__ = "2.0.18"

import sys
import os

def _load_module():
    import importlib.util
    import sys

    abi_tag = f"cpython-{sys.version_info.major}{sys.version_info.minor}"
    module_name = f"pyorbbecsdk.{abi_tag}-darwin.so"

    pkg_dir = os.path.dirname(__file__)
    module_path = os.path.join(pkg_dir, module_name)

    if not os.path.exists(module_path):
        raise ImportError(f"Module file not found: {module_path}")

    spec = importlib.util.spec_from_file_location("pyorbbecsdk", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["pyorbbecsdk"] = module
    spec.loader.exec_module(module)
    return module

try:
    _pyorbbecsdk = _load_module()
    globals().update(vars(_pyorbbecsdk))
except ImportError as e:
    print(f"Could not load pyorbbecsdk: {e}")
