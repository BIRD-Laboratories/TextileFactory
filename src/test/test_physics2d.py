import unittest
from TextileFactory.physics2d_bindings import Physics2D

class TestPhysics2D(unittest.TestCase):
    def setUp(self):
        self.params = {
            "global_resolution": [80, 60],
            "factory_layout": {
                "Entrance": [5, 5],
                "Completed Area": [65, 40]
            },
            "conveyor_paths": [
                [5, 5], [65, 40]
            ],
            "equipment_details": {
                "Entrance": {"speed": 5}
            },
            "distance_threshold": 7,
            "time_threshold": 5,
            "item_rate": 1,
            "steps_per_second": 0.01
        }
        self.physics = Physics2D(self.params)

    def test_spawn_material(self):
        material = self.physics.spawn_material([5, 5], "Cot")
        self.assertEqual(material['position'].tolist(), [5, 5])
        self.assertEqual(material['type'], "Cot")

    def test_calculate_movement_time(self):
        time = self.physics.calculate_movement_time(5)
        self.assertEqual(time, 2)

    def test_vectorized_move_materials(self):
        material = self.physics.spawn_material([5, 5], "Cot")
        self.physics.vectorized_move_materials([material], self.params["conveyor_paths"], 0.5)
        self.assertNotEqual(material['position'].tolist(), [5, 5])

    def test_update_materials(self):
        updates = self.physics.update_materials(True, True, 0)
        self.assertGreater(len(updates["materials"]), 0)