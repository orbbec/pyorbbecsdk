# Type Stubs for pyorbbecsdk

This directory contains Python type stub files (`.pyi`) for the pyorbbecsdk package.

## What are .pyi files?

`.pyi` files are type stub files that provide type information for Python packages. They enable:
- **IDE Autocomplete**: Smart code completion in VS Code, PyCharm, etc.
- **Type Checking**: Static type analysis with tools like mypy or pyright
- **Better Documentation**: Inline documentation for classes and functions

## Usage

> 💡 **Recommended: Use Virtual Environment**
>
> This documentation assumes you're using a Python virtual environment. If you haven't set one up yet, please follow the [Virtual Environment Guide](../README.md#recommended-use-virtual-environment) first.

### Scenario 1: pip install (Recommended)

When you install from PyPI, stubs are automatically included:

```bash
pip install --upgrade pyorbbecsdk2
```

**Verification**: After installation, check if stubs are present:

```bash
# Linux/macOS
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
# Expected output example: /home/user/.local/lib/python3.x/site-packages/pyorbbecsdk

# Windows PowerShell
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
# Expected output example: C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.x\LocalCache\local-packages\Python3x\site-packages\pyorbbecsdk
```

If the directory contains `.pyi` files, stubs are already available and you can skip to [IDE Configuration](#ide-configuration).

### Scenario 2: Source Build

When building from source, stubs need to be manually copied to the package directory.

#### Step 1: Find your package installation path

Run the following command to find where pyorbbecsdk is installed:

**Linux/macOS:**
```bash
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
```

**Windows PowerShell:**
```powershell
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
```

**Windows CMD:**
```cmd
python -c "import pyorbbecsdk; import os; print(os.path.dirname(pyorbbecsdk.__file__))"
```

**Example output:**
```
/home/user/pyorbbecsdk/build/lib/pyorbbecsdk
```

**Note:** Save this path for the next step.

#### Step 2: Copy stubs to the package directory

Navigate to your pyorbbecsdk source directory (where this README is located), then run:

**Linux/macOS:**
```bash
# Replace with your actual path from Step 1
PACKAGE_PATH="/home/user/pyorbbecsdk/build/lib/pyorbbecsdk"
cp stubs/*.pyi "$PACKAGE_PATH/"
```

**Windows PowerShell:**
```powershell
# Replace with your actual path from Step 1
$PackagePath = "C:\Users\User\pyorbbecsdk\build\lib\pyorbbecsdk"
Copy-Item "stubs\*.pyi" "$PackagePath\"
```

**Windows CMD:**
```cmd
:: Replace with your actual path from Step 1
set PACKAGE_PATH=C:\Users\User\pyorbbecsdk\build\lib\pyorbbecsdk
copy stubs\*.pyi "%PACKAGE_PATH%\"
```

#### Step 3: Verify the stubs are copied

Check that the `.pyi` files are now in the package directory:

**Linux/macOS:**
```bash
ls -la "$PACKAGE_PATH/*.pyi"
```

**Windows PowerShell:**
```powershell
Get-ChildItem "$PackagePath\*.pyi"
```

**Windows CMD:**
```cmd
dir "%PACKAGE_PATH%\*.pyi"
```

You should see `__init__.pyi` and `pyorbbecsdk.pyi` listed.

## IDE Configuration

### VS Code (with Pylance)

No additional configuration needed if stubs are in the package directory. Pylance will automatically detect them.

To verify stubs are working:
```python
from pyorbbecsdk import Context, Pipeline, Config

pipeline = Pipeline()
pipeline.start()  # Try typing: you should see autocomplete suggestions
```

If autocomplete doesn't work, try reloading VS Code:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "Developer: Reload Window"
3. Press Enter

### PyCharm

PyCharm should automatically detect stubs in the package directory.

If not, you can add the stubs directory as an external documentation path:
1. Go to `File` → `Settings` (or `PyCharm` → `Preferences` on macOS)
2. Navigate to `Project` → `Python Interpreter`
3. Click the gear icon → `Show All`
4. Select your interpreter → Click the folder icon (`Interpreter Paths`)
5. Add the path to the stubs directory

## FAQ

### Q: I copied the stubs but still don't get code completion?

**A:** Try these steps:
1. **Restart your IDE** - Most IDEs cache type information and need a restart
2. **Verify stub location** - Ensure `.pyi` files are in the same directory as `__init__.py`:
   ```bash
   python -c "import pyorbbecsdk; import os; print(os.listdir(os.path.dirname(pyorbbecsdk.__file__)))"
   ```
   You should see `__init__.py`, `__init__.pyi`, and `pyorbbecsdk.pyi` in the output.

3. **Check IDE settings** - Ensure your IDE's Python language server is enabled (Pylance for VS Code, Python plugin for PyCharm)

### Q: How do I confirm the stubs path is correct?

**A:** Run this Python script:

```python
import pyorbbecsdk
import os

package_dir = os.path.dirname(pyorbbecsdk.__file__)
print(f"Package directory: {package_dir}")

files = os.listdir(package_dir)
stubs = [f for f in files if f.endswith('.pyi')]
print(f"Stubs found: {stubs}")

if stubs:
    print("✓ Stubs are correctly installed!")
else:
    print("✗ No stubs found. Please copy .pyi files to the directory above.")
```

### Q: Do I need to reinstall stubs after rebuilding the package?

**A:** Yes. If you rebuild the package from source (e.g., run `pip install .` again), the installation directory may change or be cleaned, so you need to copy the stubs again following [Scenario 2](#scenario-2-source-build).

### Q: Are these stubs required to run the code?

**A:** No. The stubs are only for development convenience (autocomplete and type checking). Your code will run fine without them.

## Generating Stubs

To regenerate stubs from the compiled module:

```bash
# Install pybind11-stubgen
pip install pybind11-stubgen

# Generate stubs
pybind11-stubgen pyorbbecsdk -o .

# Fix the generated stubs (if needed)
python scripts/fix_pyi.py pyorbbecsdk.pyi
```

## Files

- `__init__.pyi`: Module exports and type definitions
- `pyorbbecsdk.pyi`: Main type definitions for all classes and functions
