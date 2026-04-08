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

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


class PrebuiltExtension(Extension):
    def __init__(self, name, lib_dir=""):
        super().__init__(name, sources=[])
        self.lib_dir = os.path.abspath(lib_dir)


class CustomBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        if not os.path.isdir(ext.lib_dir) or not os.listdir(ext.lib_dir):
            raise FileNotFoundError(
                f"Directory '{ext.lib_dir}' is empty or does not exist. " "Please compile with CMake first."
            )

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(extdir, exist_ok=True)
        self.copy_all_files(ext.lib_dir, extdir)

        # macOS: fix rpath for dylib dependencies
        if sys.platform == "darwin":
            self.fix_rpath(extdir)

    def copy_all_files(self, source_dir, destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            destination_path = os.path.join(destination_dir, item)

            if os.path.islink(source_path):
                link_target = os.readlink(source_path)
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                os.symlink(link_target, destination_path)
            elif os.path.isdir(source_path):
                self.copy_all_files(source_path, destination_path)
            else:
                shutil.copy2(source_path, destination_path)

    def fix_rpath(self, directory):
        """Fix rpath for .so files to find libOrbbecSDK.2.dylib using @loader_path"""
        for item in os.listdir(directory):
            if item.endswith(".so"):
                file_path = os.path.join(directory, item)
                try:
                    subprocess.run(
                        [
                            "install_name_tool",
                            "-change",
                            "@rpath/libOrbbecSDK.2.dylib",
                            "@loader_path/libOrbbecSDK.2.dylib",
                            file_path,
                        ],
                        check=True,
                        capture_output=True,
                    )
                    print(f"Fixed rpath for {file_path}")
                except subprocess.CalledProcessError:
                    pass  # rpath might already be correct


setup(
    ext_modules=[PrebuiltExtension("pyorbbecsdk", "install/lib")],
    cmdclass={"build_ext": CustomBuildExt},
    zip_safe=False,
)
