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
        # Skip the compilation step entirely
        # Directly handle copying of pre-built libraries
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(extdir, exist_ok=True)  # Ensure the destination path exists
        self.copy_all_files(ext.lib_dir, extdir)

    def copy_all_files(self, source_dir, destination_dir):
        # Ensure the entire destination directory structure exists
        os.makedirs(destination_dir, exist_ok=True)

        # Iterate through all items in the source directory
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            destination_path = os.path.join(destination_dir, item)

            # Check if the item is a symbolic link
            if os.path.islink(source_path):
                # Preserve the symbolic link
                link_target = os.readlink(source_path)
                # Remove existing destination file or link if it exists
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                os.symlink(link_target, destination_path)
                print(f"Preserved symbolic link {destination_path} -> {link_target}")
            elif os.path.isdir(source_path):
                # Recursively copy directory
                self.copy_all_files(source_path, destination_path)
            else:
                # Copy the file, preserving metadata
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
