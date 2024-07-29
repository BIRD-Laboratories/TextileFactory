#!/bin/bash

# Directory where the C code and Python scripts will be located
SRC_DIR="src"
BUILD_DIR="build"

# Ensure the build directory exists
mkdir -p $BUILD_DIR

# Create the src directory and necessary files if they don't exist
create_file_if_not_exists() {
    local file_path=$1
    local file_content=$2
    if [ ! -f $file_path ]; then
        echo "$file_content" > $file_path
        echo "Created $file_path"
    fi
}

mkdir -p $SRC_DIR

create_file_if_not_exists "$SRC_DIR/physics2d.c" "$(cat <<'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    float x, y;
} Vec2;

typedef struct {
    Vec2 position;
    Vec2 velocity;
    char type[4];
    int area;
    time_t start_time;
    float path_progress;
    int path_index;
} Material;

typedef struct {
    int width, height;
    Material *materials;
    int material_count;
    float distance_threshold;
    float time_threshold;
    float item_rate;
    float steps_per_second;
    Vec2 *conveyor_paths;
    int conveyor_path_count;
} Physics2D;

Physics2D* create_physics2d(int width, int height, float distance_threshold, float time_threshold, float item_rate, float steps_per_second, Vec2 *conveyor_paths, int conveyor_path_count) {
    Physics2D *physics = (Physics2D*)malloc(sizeof(Physics2D));
    physics->width = width;
    physics->height = height;
    physics->materials = NULL;
    physics->material_count = 0;
    physics->distance_threshold = distance_threshold;
    physics->time_threshold = time_threshold;
    physics->item_rate = item_rate;
    physics->steps_per_second = steps_per_second;
    physics->conveyor_paths = conveyor_paths;
    physics->conveyor_path_count = conveyor_path_count;
    return physics;
}

void spawn_material(Physics2D *physics, Vec2 pos, const char *material_type) {
    physics->material_count++;
    physics->materials = (Material*)realloc(physics->materials, physics->material_count * sizeof(Material));
    Material *material = &physics->materials[physics->material_count - 1];
    material->position = pos;
    material->velocity.x = 0.0;
    material->velocity.y = 0.0;
    strncpy(material->type, material_type, 3);
    material->type[3] = '\0';
    material->area = 0;
    material->start_time = time(NULL);
    material->path_progress = 0.0;
    material->path_index = 0;
}

void vectorized_move_materials(Physics2D *physics, float speed) {
    for (int i = 0; i < physics->material_count; i++) {
        Material *material = &physics->materials[i];
        material->path_progress += speed;
        if (material->path_progress >= 1.0) {
            material->path_index++;
            material->path_progress = 0.0;
        }
        material->path_index %= physics->conveyor_path_count;

        Vec2 start_pos = physics->conveyor_paths[material->path_index];
        Vec2 end_pos = physics->conveyor_paths[(material->path_index + 1) % physics->conveyor_path_count];
        float t = material->path_progress;

        material->position.x = start_pos.x + t * (end_pos.x - start_pos.x);
        material->position.y = start_pos.y + t * (end_pos.y - start_pos.y);
    }
}

void update(Physics2D *physics, float dt) {
    for (int i = 0; i < physics->material_count; i++) {
        Material *material = &physics->materials[i];
        material->position.x += material->velocity.x * dt;
        material->position.y += material->velocity.y * dt;
    }
}

void get_state_array(Physics2D *physics, int **state_array) {
    for (int i = 0; i < physics->material_count; i++) {
        Material *material = &physics->materials[i];
        int x = (int)material->position.x;
        int y = (int)material->position.y;
        if (0 <= x && x < physics->width && 0 <= y && y < physics->height) {
            if (strcmp(material->type, "Cot") == 0) {
                state_array[x][y] = 1;
            } else if (strcmp(material->type, "Fab") == 0) {
                state_array[x][y] = 2;
            } else if (strcmp(material->type, "Fin") == 0) {
                state_array[x][y] = 3;
            }
        }
    }
}

void print_state_array(Physics2D *physics, int **state_array) {
    for (int y = 0; y < physics->height; y++) {
        for (int x = 0; x < physics->width; x++) {
            printf("%d ", state_array[x][y]);
        }
        printf("\n");
    }
}

void free_physics2d(Physics2D *physics) {
    free(physics->materials);
    free(physics);
}
EOF
)"

create_file_if_not_exists "$SRC_DIR/physics2d_bindings.py" "$(cat <<'EOF'
import ctypes
import os

# Load the shared library
_lib_path = os.path.join(os.path.dirname(__file__), 'physics2d.so')
physics2d_lib = ctypes.CDLL(_lib_path)

# Define the structures
class Vec2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class Material(ctypes.Structure):
    _fields_ = [("position", Vec2),
                ("velocity", Vec2),
                ("type", ctypes.c_char * 4),
                ("area", ctypes.c_int),
                ("start_time", ctypes.c_long),
                ("path_progress", ctypes.c_float),
                ("path_index", ctypes.c_int)]

class Physics2D(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("materials", ctypes.POINTER(Material)),
                ("material_count", ctypes.c_int),
                ("distance_threshold", ctypes.c_float),
                ("time_threshold", ctypes.c_float),
                ("item_rate", ctypes.c_float),
                ("steps_per_second", ctypes.c_float),
                ("conveyor_paths", ctypes.POINTER(Vec2)),
                ("conveyor_path_count", ctypes.c_int)]

# Define the functions
physics2d_lib.create_physics2d.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.POINTER(Vec2), ctypes.c_int]
physics2d_lib.create_physics2d.restype = ctypes.POINTER(Physics2D)

physics2d_lib.spawn_material.argtypes = [ctypes.POINTER(Physics2D), Vec2, ctypes.c_char_p]

physics2d_lib.vectorized_move_materials.argtypes = [ctypes.POINTER(Physics2D), ctypes.c_float]

physics2d_lib.update.argtypes = [ctypes.POINTER(Physics2D), ctypes.c_float]

physics2d_lib.get_state_array.argtypes = [ctypes.POINTER(Physics2D), ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]

physics2d_lib.print_state_array.argtypes = [ctypes.POINTER(Physics2D), ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]

physics2d_lib.free_physics2d.argtypes = [ctypes.POINTER(Physics2D)]

# Helper functions
def create_physics2d(width, height, distance_threshold, time_threshold, item_rate, steps_per_second, conveyor_paths):
    conveyor_paths_array = (Vec2 * len(conveyor_paths))(*conveyor_paths)
    return physics2d_lib.create_physics2d(width, height, distance_threshold, time_threshold, item_rate, steps_per_second, conveyor_paths_array, len(conveyor_paths))

def spawn_material(physics, pos, material_type):
    physics2d_lib.spawn_material(physics, pos, material_type.encode('utf-8'))

def vectorized_move_materials(physics, speed):
    physics2d_lib.vectorized_move_materials(physics, speed)

def update(physics, dt):
    physics2d_lib.update(physics, dt)

def get_state_array(physics):
    state_array = [[0 for _ in range(physics.contents.height)] for _ in range(physics.contents.width)]
    state_array_ptr = (ctypes.POINTER(ctypes.c_int) * physics.contents.width)(*([ctypes.cast(ctypes.pointer(ctypes.c_int(0)), ctypes.POINTER(ctypes.c_int)) for _ in range(physics.contents.height)]))
    for i in range(physics.contents.width):
        state_array_ptr[i] = (ctypes.c_int * physics.contents.height)(*state_array[i])
    physics2d_lib.get_state_array(physics, state_array_ptr)
    for i in range(physics.contents.width):
        for j in range(physics.contents.height):
            state_array[i][j] = state_array_ptr[i][j]
    return state_array

def print_state_array(physics):
    state_array = get_state_array(physics)
    physics2d_lib.print_state_array(physics, (ctypes.POINTER(ctypes.c_int) * physics.contents.width)(*([ctypes.cast(ctypes.pointer(ctypes.c_int(0)), ctypes.POINTER(ctypes.c_int)) for _ in range(physics.contents.height)])))

def free_physics2d(physics):
    physics2d_lib.free_physics2d(physics)
EOF
)"

create_file_if_not_exists "$SRC_DIR/main.py" "$(cat <<'EOF'
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
EOF
)"

create_file_if_not_exists "$SRC_DIR/params.py" "$(cat <<'EOF'
def load_params():
    return {
        'global_resolution': (10, 10),
        'distance_threshold': 1.0,
        'time_threshold': 1.0,
        'item_rate': 1.0,
        'steps_per_second': 1.0,
        'conveyor_paths': [(0, 0), (1, 1), (2, 2)]
    }
EOF
)"

cat <<EOF > src/factory_simulation/core.py
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
EOF

cat <<EOF > src/factory_simulation/cli.py
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
EOF

cat <<EOF > src/factory_simulation/main.py
from .cli import main

if __name__ == "__main__":
    main()
EOF

cat <<EOF > src/factory_simulation/params.py
import json

def load_params(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)
    return params
EOF

cat <<EOF > params.json
{
    "global_resolution": [80, 60],
    "factory_layout": {
        "Entrance": [5, 5],
        "Cutting Area": [35, 5],
        "Sewing Area": [50, 5],
        "Stuffing Area": [65, 5],
        "Finishing Area": [5, 20],
        "Quality Control": [20, 20],
        "Packaging Area": [35, 20],
        "Shipping Area": [50, 20],
        "Utilities": [65, 20],
        "Completed Area": [65, 40]
    },
    "equipment_details": {
        "Cutting Area": {"type": "Cutting Machine", "position": [35, 10], "speed": 5},
        "Sewing Area": {"type": "Sewing Machine", "position": [50, 10], "speed": 10},
        "Stuffing Area": {"type": "Stuffing Machine", "position": [65, 10], "speed": 2},
        "Finishing Area": {"type": "Finishing Table", "position": [5, 25], "speed": 1.5},
        "Quality Control": {"type": "Inspection Table", "position": [20, 25], "speed": 3},
        "Packaging Area": {"type": "Packaging Machine", "position": [35, 25], "speed": 2.5},
        "Shipping Area": {"type": "Loading Dock", "position": [50, 25], "speed": 4}
    },
    "conveyor_paths": [
        [5, 5], [35, 5], [50, 5], [65, 5], [5, 20], [20, 20], [35, 20], [50, 20], [65, 20], [65, 40]
    ],
    "material_radius": 1,
    "distance_threshold": 7,
    "time_threshold": 5,
    "item_rate": 1,
    "steps_per_second": 0.01,
    "hud_params": {
        "hud_height": 500,
        "hud_bg_color": [240, 240, 240],
        "hud_border_color": [100, 100, 100],
        "hud_text_color": [0, 0, 0],
        "button_color": [150, 150, 150],
        "button_text_color": [0, 0, 0],
        "button_restart_pos": [300, 510],
        "button_auto_move_pos": [450, 510],
        "button_width": 100,
        "button_height": 30,
        "button_stop_spawn_pos": [200, 510]
    },
    "box_params": {
        "box_width": 10,
        "box_height": 10,
        "box_color": [100, 100, 100]
    }
}
EOF

cat <<EOF > setup.py
from setuptools import setup, find_packages

setup(
    name="factory_simulation",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "jax",
        "jaxlib"
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
EOF