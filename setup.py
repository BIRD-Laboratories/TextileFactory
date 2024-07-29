from setuptools import setup, find_packages
import os

# Path to the precompiled shared library
precompiled_lib_path = os.path.join('src', 'physics2d.so')

# Ensure the precompiled library exists
if not os.path.exists(precompiled_lib_path):
    raise FileNotFoundError(f"Precompiled library not found at {precompiled_lib_path}. Please compile the C code manually.")

setup(
    name="factory_simulation",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'factory_simulation': ['physics2d.so']
    },
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
)