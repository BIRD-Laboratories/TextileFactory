import time
from .params import load_params
from .physics_2d import Physics2D

class FactorySimulation:
    def __init__(self, params, print_only=False):
        self.params = params
        self.physics = Physics2D(self.params)
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
            self.physics.materials.extend(updates["materials"])
            self.object_count += updates["object_count"]
            self.completed_count += updates["completed_count"]
            self.last_spawn_time = updates["last_spawn_time"]

            self.physics.update(dt)
            state_array = self.physics.get_state_array()

            if self.print_only:
                self.physics.print_state_array(state_array)
                break
            else:
                time.sleep(dt)
