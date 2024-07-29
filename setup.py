from setuptools import setup, find_packages
import os

# Path to the precompiled shared library
precompiled_lib_path = os.path.join('src', 'physics2d.so')

# Ensure the precompiled library exists
if not os.path.exists(precompiled_lib_path):
    raise FileNotFoundError(f"Precompiled library not found at {precompiled_lib_path}. Please compile the C code manually.")

# Read the long description from README.md
long_description = ""
try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    print("README.md not found. Using an empty long description.")

setup(
    name="TextileFactory",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'TextileFactory': ['physics2d.so']
    },
    entry_points={
        "console_scripts": [
            "factory_simulation=factory_simulation.cli:main"
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
)