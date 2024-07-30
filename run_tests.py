import sys
import os
import unittest
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from TextileFactory import *
#from TextileFactory.main import FactorySimulation
#from TextileFactory.params import load_params
#from TextileFactory.render import render_simulation
#from TextileFactory.physics2d_bindings import Physics2D

class TestTextileFactory(unittest.TestCase):
    @patch('TextileFactory.core.FactorySimulation')
    def test_factory_simulation(self, mock_factory_simulation):
        # Mock the FactorySimulation class
        mock_instance = mock_factory_simulation.return_value
        mock_instance.run.return_value = None

        # Create a mock params dictionary
        mock_params = {
            'global_resolution': [80, 60],
            'distance_threshold': 7,
            'time_threshold': 5,
            'item_rate': 1,
            'steps_per_second': 0.01,
            'conveyor_paths': [[5, 5], [65, 40]]
        }

        # Create an instance of FactorySimulation with mock params
        simulation = FactorySimulation(mock_params)

        # Verify that the FactorySimulation instance was created with the correct params
        mock_factory_simulation.assert_called_once_with(mock_params)

        # Run the simulation
        simulation.run()

        # Verify that the run method was called
        mock_instance.run.assert_called_once()

    @patch('TextileFactory.render.render_simulation')
    def test_render_simulation(self, mock_render_simulation):
        # Mock the render_simulation function
        mock_render_simulation.return_value = None

        # Create a mock params file
        mock_params_file = 'mock_params.json'

        # Run the render simulation function with mock params file and print_only=True
        render_simulation(params_file=mock_params_file, print_only=True)

        # Verify that the function was called with the correct arguments
        mock_render_simulation.assert_called_once_with(params_file=mock_params_file, print_only=True)

    @patch('TextileFactory.physics2d_bindings.Physics2D')
    def test_physics2d(self, mock_physics2d):
        # Mock the Physics2D class
        mock_instance = mock_physics2d.return_value

        # Create a mock params dictionary
        mock_params = {
            'global_resolution': [80, 60],
            'distance_threshold': 7,
            'time_threshold': 5,
            'item_rate': 1,
            'steps_per_second': 0.01,
            'conveyor_paths': [[5, 5], [65, 40]]
        }

        # Create an instance of Physics2D with mock params
        physics = Physics2D(mock_params)

        # Verify that the Physics2D instance was created with the correct params
        mock_physics2d.assert_called_once_with(mock_params)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover('test', pattern='test_*.py')

    # Create a TestRunner with higher verbosity
    runner = unittest.TextTestRunner(verbosity=2)

    # Run the test suite with verbose output
    result = runner.run(suite)

    # Print detailed test results
    if not result.wasSuccessful():
        print("\nFailed tests:")
        for failure in result.failures:
            print(f"Failure: {failure[0]}")
            print(failure[1])
        for error in result.errors:
            print(f"Error: {error[0]}")
            print(error[1])

    print(f"\nRan {result.testsRun} tests in total.")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")