# Import modules into the package namespace
from .main import FactorySimulation
from .cli import main as cli_main
from .render import render_simulation
from .params import load_params
from .physics2d_bindings import *

# You can also define package-level variables or functions
__version__ = '0.1'