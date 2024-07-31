import unittest
from unittest.mock import patch, MagicMock
from textilefactorylib.src.render import render_simulation
from textilefactorylib.src.params import load_params
import pygame

class TestRender(unittest.TestCase):
    def setUp(self):
        self.params = load_params('params.json')  # Adjust the path as needed

    @patch('TextileFactory.render.render_simulation')
    def test_render_simulation_print_only_true(self, mock_render_simulation):
        # Mock the render_simulation function
        mock_render_simulation.return_value = None

        # Run the render simulation function with print_only=True
        render_simulation(params_file='params.json', print_only=True)

        # Verify that the function was called with the correct arguments
        mock_render_simulation.assert_called_once_with(params_file='params.json', print_only=True)

    @patch('TextileFactory.render.render_simulation')
    def test_render_simulation_print_only_false(self, mock_render_simulation):
        # Mock the render_simulation function
        mock_render_simulation.return_value = None

        # Run the render simulation function with print_only=False
        render_simulation(params_file='params.json', print_only=False)

        # Verify that the function was called with the correct arguments
        mock_render_simulation.assert_called_once_with(params_file='params.json', print_only=False)

if __name__ == "__main__":
    unittest.main()