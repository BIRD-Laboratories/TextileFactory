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