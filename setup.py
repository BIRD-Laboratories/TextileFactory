from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import os
import subprocess

class CustomBuildExtCommand(build_ext):
    """Customized setuptools build_ext command to compile the C program."""
    def run(self):
        # Compile the C program
        self.compile_c_program()
        # Run the default build_ext command
        build_ext.run(self)

    def compile_c_program(self):
        # Define the source file and the output shared library
        source_file = os.path.join('textilefactorylib', 'src', 'physics2d.c')
        output_library = os.path.join('textilefactorylib', 'src', 'physics2d.so')
        # Define the command to compile the C program
        compile_command = [
            'gcc', '-shared', '-o', output_library, source_file
        ]
        # Run the compilation command
        try:
            subprocess.check_call(compile_command)
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed with exit code {e.returncode}")
            print(f"Command: {e.cmd}")
            print(f"Output: {e.output}")
            raise

# Define the extension module
physics2d_module = Extension(
    'textilefactorylib.src.physics2d',
    sources=['textilefactorylib/src/physics2d.c'],
    language='c'
)

# Read the long description from README.md
long_description = ""
try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    print("README.md not found. Using an empty long description.")

setup(
    name="textilefactorylib",
    version="0.1",
    packages=find_packages(where='textilefactorylib/src'),
    package_dir={'': 'textilefactorylib/src'},
    package_data={
        'textilefactorylib.src': ['physics2d.so']
    },
    entry_points={
        "console_scripts": [
            "factory_simulation=textilefactorylib.src.cli:main"
        ]
    },
    author="Julian Herrera",
    author_email="jherrera282@mycod.us",
    description="A factory simulation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BIRD-Laboratories/TextileFactory",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    include_package_data=True,
    install_requires=[
        'pygame',  # Add Pygame as a dependency
    ],
    test_suite='tests',
    tests_require=[
        'unittest',  # Add unittest as a test dependency
    ],
    ext_modules=[physics2d_module],
    cmdclass={
        'build_ext': CustomBuildExtCommand
    }
)