import unittest
from TextileFactory.main import FactorySimulation
from TextileFactory.params import load_params

class TestFactorySimulation(unittest.TestCase):
    def setUp(self):
        self.params = load_params('params.json')  # Adjust the path as needed
        self.simulation = FactorySimulation(self.params)

    def test_initialization(self):
        self.assertEqual(self.simulation.params, self.params)
        self.assertIsNotNone(self.simulation.physics)
        self.assertFalse(self.simulation.print_only)
        self.assertEqual(self.simulation.current_area, "Entrance")
        self.assertEqual(self.simulation.time_per_step, 0)
        self.assertEqual(self.simulation.object_count, 0)
        self.assertEqual(self.simulation.completed_count, 0)
        self.assertTrue(self.simulation.auto_move)
        self.assertTrue(self.simulation.spawn_enabled)
        self.assertIsNotNone(self.simulation.last_spawn_time)

    def test_run_method(self):
        # This test assumes that the run method can be executed without infinite loop
        # You might need to modify the run method to allow for testing or use mocking
        self.simulation.run()
        self.assertGreater(self.simulation.object_count, 0)
        self.assertGreater(self.simulation.completed_count, 0)

if __name__ == "__main__":
    unittest.main()