# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
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

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class PrebuiltExtension(Extension):
    def __init__(self, name, lib_dir=''):
        super().__init__(name, sources=[])  # No sources to compile
        self.lib_dir = os.path.abspath(lib_dir)


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

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(extdir, exist_ok=True)  # Ensure the destination path exists
        self.copy_all_files(ext.lib_dir, extdir)

    def copy_all_files(self, source_dir, destination_dir):
        os.makedirs(destination_dir, exist_ok=True)  # Ensure the entire destination directory structure exists

        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            destination_path = os.path.join(destination_dir, item)

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


setup(
    name='pyorbbecsdk',
    version='1.3.1',
    author='Joe Dong',
    author_email='mocun@orbbec.com',
    description='pyorbbecsdk is a python wrapper for the OrbbecSDK',
    long_description='',
    ext_modules=[PrebuiltExtension('pyorbbecsdk', 'install/lib')],
    cmdclass={'build_ext': CustomBuildExt},
    zip_safe=False,
)
