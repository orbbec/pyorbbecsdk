# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http:# www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import os
import shutil
import subprocess
import sys

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Get current Python ABI tag (e.g., cp310, cp39)
def get_abi_tag():
    return f"cp{sys.version_info.major}{sys.version_info.minor}"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

class PrebuiltExtension(Extension):
    def __init__(self, name, lib_dir='', extensions_dir=''):
        super().__init__(name, sources=[])  # No sources to compile
        self.lib_dir = os.path.abspath(lib_dir)
        self.extensions_dir = os.path.abspath(extensions_dir) if extensions_dir else ''


class CustomBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # Check if the lib directory exists and contains files
        if not os.path.isdir(ext.lib_dir) or not os.listdir(ext.lib_dir):
            raise FileNotFoundError(
                f"Directory '{ext.lib_dir}' is empty or does not exist. "
                "Please compile the necessary components with CMake as described in the README."
            )

        # Get the package directory (pyorbbecsdk/)
        # The extension should be placed inside the pyorbbecsdk package
        ext_fullpath = self.get_ext_fullpath(ext.name)
        extdir = os.path.dirname(ext_fullpath)

        # If extdir doesn't end with pyorbbecsdk, we need to put files there
        if not extdir.endswith('pyorbbecsdk'):
            extdir = os.path.join(extdir, 'pyorbbecsdk')

        os.makedirs(extdir, exist_ok=True)
        self.copy_all_files(ext.lib_dir, extdir)

        # Copy extension libraries from extensions directory
        if ext.extensions_dir and os.path.isdir(ext.extensions_dir):
            self.copy_extension_libs(ext.extensions_dir, extdir)

        # Fix rpath for .so files on macOS
        if sys.platform == 'darwin':
            self.fix_rpath(extdir)

        # Copy type stub (.pyi) for IDE auto-completion (PEP 561)
        stub_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'stubs', 'pyorbbecsdk.pyi')
        if os.path.isfile(stub_src):
            stub_dst = os.path.join(extdir, 'pyorbbecsdk.pyi')
            shutil.copy2(stub_src, stub_dst)
            print(f"Copied type stub {stub_src} to {stub_dst}")

    def copy_all_files(self, source_dir, destination_dir):
        abi_tag = get_abi_tag()
        # Convert cp310 -> cpython-310 for matching filename
        abi_pattern = abi_tag.replace('cp', 'cpython-')
        os.makedirs(destination_dir, exist_ok=True)

        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            destination_path = os.path.join(destination_dir, item)

            # Skip .so files for other Python versions
            if item.endswith('.so') and not item.endswith(f'{abi_pattern}-darwin.so'):
                print(f"Skipping {item} (not for {abi_tag})")
                continue

            if os.path.islink(source_path):
                link_target = os.readlink(source_path)
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                os.symlink(link_target, destination_path)
                print(f"Preserved symbolic link {destination_path} -> {link_target}")
            elif os.path.isdir(source_path):
                self.copy_all_files(source_path, destination_path)
            else:
                shutil.copy2(source_path, destination_path)
                print(f"Copied {source_path} to {destination_path}")

    def copy_extension_libs(self, extensions_dir, destination_dir):
        """Copy extension libraries from extensions subdirectories to destination, preserving directory structure"""
        if not os.path.isdir(extensions_dir):
            return

        # Create extensions directory in destination
        ext_dest_dir = os.path.join(destination_dir, 'extensions')
        os.makedirs(ext_dest_dir, exist_ok=True)

        for subdir in os.listdir(extensions_dir):
            subdir_path = os.path.join(extensions_dir, subdir)
            if os.path.isdir(subdir_path):
                # Create subdirectory (filters, firmwareupdater, frameprocessor)
                sub_dest_dir = os.path.join(ext_dest_dir, subdir)
                os.makedirs(sub_dest_dir, exist_ok=True)

                for item in os.listdir(subdir_path):
                    if item.endswith('.dylib') or item.endswith('.so'):
                        source_path = os.path.join(subdir_path, item)
                        dest_path = os.path.join(sub_dest_dir, item)
                        if os.path.exists(dest_path):
                            os.remove(dest_path)
                        shutil.copy2(source_path, dest_path)
                        print(f"Copied extension library {source_path} to {dest_path}")

    def fix_rpath(self, directory):
        """Fix rpath for .so and .dylib files to find libOrbbecSDK.2.dylib using @loader_path"""
        for item in os.listdir(directory):
            if item.endswith('.so') or item.endswith('.dylib'):
                file_path = os.path.join(directory, item)
                # Skip the main SDK library itself
                if item.startswith('libOrbbecSDK'):
                    continue
                try:
                    # Change @rpath to @loader_path for the SDK library
                    subprocess.run([
                        'install_name_tool', '-change',
                        '@rpath/libOrbbecSDK.2.dylib',
                        '@loader_path/libOrbbecSDK.2.dylib',
                        file_path
                    ], check=True, capture_output=True)
                    print(f"Fixed rpath for {file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Could not fix rpath for {file_path}: {e}")


setup(
    name='pyorbbecsdk2',
    version='2.0.18',
    author='zhonghong',
    author_email='zhonghong@orbbec.com',
    description='pyorbbecsdk is a python wrapper for the OrbbecSDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyorbbecsdk'],
    package_dir={'': 'src'},
    package_data={'pyorbbecsdk': ['*.so', '*.dylib', 'extensions/**/*']},
    ext_modules=[PrebuiltExtension('pyorbbecsdk', 'install/lib', 'extensions')],
    cmdclass={'build_ext': CustomBuildExt},
    zip_safe=False,
)
