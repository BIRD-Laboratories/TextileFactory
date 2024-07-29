from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sys
import platform

class CustomBuildExtCommand(build_ext):
    def run(self):
        # Compile the C code into a shared library
        try:
            if platform.system() == "Windows":
                subprocess.run(["gcc", "-shared", "-o", "physics2d.dll", "src/physics2d.c"], check=True)
            else:
                subprocess.run(["gcc", "-shared", "-o", "physics2d.so", "src/physics2d.c"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed with error: {e}")
            sys.exit(1)
        build_ext.run(self)

physics2d_module = Extension(
    'physics2d',
    sources=['src/physics2d.c'],
    include_dirs=[],
    libraries=[],
    library_dirs=[]
)

setup(
    name="factory_simulation",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "ctypes"
    ],
    entry_points={
        "console_scripts": [
            "factory_simulation=factory_simulation.cli:main"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A factory simulation library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/factory_simulation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    ext_modules=[physics2d_module],
    cmdclass={
        'build_ext': CustomBuildExtCommand
    }
)