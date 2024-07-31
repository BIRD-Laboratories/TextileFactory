import argparse
from .core import FactorySimulation
from .params import load_params

def main():
    parser = argparse.ArgumentParser(description="Factory Simulation")
    parser.add_argument('--params', default='params.json', help='Path to the parameters JSON file')
    parser.add_argument('--print-only', action='store_true', help='Print the state arrays instead of rendering')
    args = parser.parse_args()

    params = load_params(args.params)
    simulation = FactorySimulation(params, print_only=args.print_only)
    simulation.run()

if __name__ == "__main__":
    main()