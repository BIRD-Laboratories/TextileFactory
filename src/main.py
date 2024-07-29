import time
from .params import load_params
from .physics2d_bindings import create_physics2d, spawn_material, vectorized_move_materials, update, print_state_array, free_physics2d

class FactorySimulation:
    def __init__(self, params, print_only=False):
        self.params = params
        self.physics = create_physics2d(
            self.params['global_resolution'][0],
            self.params['global_resolution'][1],
            self.params['distance_threshold'],
            self.params['time_threshold'],
            self.params['item_rate'],
            self.params['steps_per_second'],
            [Vec2(*pos) for pos in self.params['conveyor_paths']]
        )
        self.print_only = print_only
        self.current_area = "Entrance"
        self.time_per_step = 0
        self.object_count = 0
        self.completed_count = 0
        self.auto_move = True
        self.spawn_enabled = True
        self.last_spawn_time = time.time()

    def run(self):
        dt = 1 / 60.0

        while True:
            updates = self.physics.update_materials(self.auto_move, self.spawn_enabled, self.last_spawn_time)
            for material in updates["materials"]:
                spawn_material(self.physics, Vec2(*material['position']), material['type'])
            self.object_count += updates["object_count"]
            self.completed_count += updates["completed_count"]
            self.last_spawn_time = updates["last_spawn_time"]

            update(self.physics, dt)
            state_array = get_state_array(self.physics)

            if self.print_only:
                print_state_array(self.physics)
                break
            else:
                time.sleep(dt)

    def __del__(self):
        free_physics2d(self.physics)

if __name__ == "__main__":
    params = load_params()
    simulation = FactorySimulation(params, print_only=True)
    simulation.run()
