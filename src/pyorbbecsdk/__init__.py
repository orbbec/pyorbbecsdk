# Orbbec SDK Python Bindings
__version__ = "2.0.18"

# 导入编译的模块
try:
    from .pyorbbecsdk import *
except ImportError as e:
    print(f"⚠️  无法加载 pyorbbecsdk: {e}")
