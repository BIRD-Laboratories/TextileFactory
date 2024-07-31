import unittest
from unittest.mock import patch, MagicMock
import pygame
from TextileFactory.render import render_simulation
from TextileFactory.params import load_params

class TestRender(unittest.TestCase):
    def setUp(self):
        self.params = load_params('params.json')  # Adjust the path as needed

    @patch('TextileFactory.render.pygame.init')
    @patch('TextileFactory.render.pygame.display.set_mode')
    @patch('TextileFactory.render.pygame.time.Clock')
    @patch('TextileFactory.render.pygame.event.get')
    @patch('TextileFactory.render.pygame.display.flip')
    @patch('TextileFactory.render.pygame.quit')
    @patch('TextileFactory.render.FactorySimulation')
    def test_render_simulation_print_only_true(self, mock_factory_simulation, mock_pygame_quit, mock_pygame_display_flip, mock_pygame_event_get, mock_pygame_time_clock, mock_pygame_display_set_mode, mock_pygame_init):
        # Mock the FactorySimulation class
        mock_instance = mock_factory_simulation.return_value
        mock_instance.run.return_value = None

        # Mock Pygame functions
        mock_pygame_event_get.return_value = [MagicMock(type=pygame.QUIT)]

        # Run the render simulation function with print_only=True
        render_simulation(params_file='params.json', print_only=True)

        # Verify that the function was called with the correct arguments
        mock_factory_simulation.assert_called_once_with(self.params, print_only=True)
        mock_pygame_init.assert_called_once()
        mock_pygame_display_set_mode.assert_called_once_with((self.params['global_resolution'][0], self.params['global_resolution'][1]))
        mock_pygame_time_clock.assert_called_once()
        mock_pygame_event_get.assert_called_once()
        mock_pygame_display_flip.assert_called_once()
        mock_pygame_quit.assert_called_once()

    @patch('TextileFactory.render.pygame.init')
    @patch('TextileFactory.render.pygame.display.set_mode')
    @patch('TextileFactory.render.pygame.time.Clock')
    @patch('TextileFactory.render.pygame.event.get')
    @patch('TextileFactory.render.pygame.display.flip')
    @patch('TextileFactory.render.pygame.quit')
    @patch('TextileFactory.render.FactorySimulation')
    def test_render_simulation_print_only_false(self, mock_factory_simulation, mock_pygame_quit, mock_pygame_display_flip, mock_pygame_event_get, mock_pygame_time_clock, mock_pygame_display_set_mode, mock_pygame_init):
        # Mock the FactorySimulation class
        mock_instance = mock_factory_simulation.return_value
        mock_instance.run.return_value = None

        # Mock Pygame functions
        mock_pygame_event_get.return_value = [MagicMock(type=pygame.QUIT)]

        # Run the render simulation function with print_only=False
        render_simulation(params_file='params.json', print_only=False)

        # Verify that the function was called with the correct arguments
        mock_factory_simulation.assert_called_once_with(self.params, print_only=False)
        mock_pygame_init.assert_called_once()
        mock_pygame_display_set_mode.assert_called_once_with((self.params['global_resolution'][0], self.params['global_resolution'][1]))
        mock_pygame_time_clock.assert_called_once()
        mock_pygame_event_get.assert_called_once()
        mock_pygame_display_flip.assert_called_once()
        mock_pygame_quit.assert_called_once()

if __name__ == "__main__":
    unittest.main()