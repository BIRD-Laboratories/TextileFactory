"""
Factory Simulation Program

This program simulates a factory layout with various stations and conveyor belts. Materials move through the factory,
undergoing processing at each station, and are eventually turned into a single "Fin" object. The simulation includes a Heads-Up
Display (HUD) to show current area, time per step, object count, completed count, and buttons to restart the simulation
and toggle automatic/manual movement.

Parameters to Edit:
- factory_layout: Dictionary containing the positions of each station.
- equipment_details: Dictionary containing details of each equipment type at each station.
- conveyor_paths: List of points forming a continuous path for the conveyor belts.
- material_radius: Radius of the materials.
- distance_threshold: Distance threshold for material movement.
- time_threshold: Time threshold for material movement.
- item_rate: Rate at which items are spawned.
- steps_per_second: Speed of material movement along the conveyor belt.
- hud_params: Dictionary containing parameters for the HUD, such as colors, positions, and button positions.
- box_params: Dictionary containing parameters for the completed area box, such as position, size, and color.

Usage:
- Press 'K' to spawn materials at the entrance.
- Click 'Restart' to reset the simulation.
- Click 'Auto'/'Manual' to toggle automatic/manual movement.
"""

import pygame
import pymunk
import pymunk.pygame_util
import time

# Initialize Pygame and Pymunk
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 0)  # Set gravity to zero
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Centralized parameters dictionary
params = {
    "factory_layout": {
        "Entrance": (50, 50),
        "Cutting Area": (350, 50),
        "Sewing Area": (500, 50),
        "Stuffing Area": (650, 50),
        "Finishing Area": (50, 200),
        "Quality Control": (200, 200),
        "Packaging Area": (350, 200),
        "Shipping Area": (500, 200),
        "Utilities": (650, 200),
        "Completed Area": (650, 400)  # New completed area
    },
    "equipment_details": {
        "Cutting Area": {"type": "Cutting Machine", "position": (350, 100), "speed": 5},
        "Sewing Area": {"type": "Sewing Machine", "position": (500, 100), "speed": 10},
        "Stuffing Area": {"type": "Stuffing Machine", "position": (650, 100), "speed": 2},
        "Finishing Area": {"type": "Finishing Table", "position": (50, 250), "speed": 1.5},
        "Quality Control": {"type": "Inspection Table", "position": (200, 250), "speed": 3},
        "Packaging Area": {"type": "Packaging Machine", "position": (350, 250), "speed": 2.5},
        "Shipping Area": {"type": "Loading Dock", "position": (500, 250), "speed": 4}
    },
    "conveyor_paths": [
        (50, 50), (350, 50), (500, 50), (650, 50), (50, 200), (200, 200), (350, 200), (500, 200), (650, 200), (650, 400)
    ],
    "material_radius": 10,
    "distance_threshold": 70,
    "time_threshold": 5,
    "item_rate": 1,
    "steps_per_second": 0.01,
    "hud_params": {
        "hud_height": height - 100,
        "hud_bg_color": (240, 240, 240),
        "hud_border_color": (100, 100, 100),
        "hud_text_color": (0, 0, 0),
        "button_color": (150, 150, 150),
        "button_text_color": (0, 0, 0),
        "button_restart_pos": (300, height - 90),
        "button_auto_move_pos": (450, height - 90),
        "button_width": 100,
        "button_height": 30,
        "button_stop_spawn_pos": (200, height - 90)
    },
    "box_params": {
        "box_width": 100,
        "box_height": 100,
        "box_color": (100, 100, 100)
    }
}

# Function to draw stations with solid colors and labels
def draw_stations():
    station_colors = [
        (255, 0, 0),   # Red
        (0, 255, 0),   # Green
        (0, 0, 255),   # Blue
        (255, 255, 0), # Yellow
        (255, 0, 255), # Magenta
        (0, 255, 255), # Cyan
        (128, 0, 128), # Purple
        (255, 165, 0), # Orange
        (0, 128, 0),   # Dark Green
        (0, 0, 128)    # Dark Blue
    ]

    for i, (name, pos) in enumerate(params["factory_layout"].items()):
        # Draw the station with a solid color
        station_width = 140
        station_height = 100
        station_rect = pygame.Rect(pos[0] - station_width // 2, pos[1] - station_height // 2, station_width, station_height)
        pygame.draw.rect(screen, station_colors[i % len(station_colors)], station_rect)

        # Draw the station name
        font = pygame.font.Font(None, 24)
        text = font.render(name, True, (0, 0, 0))
        text_rect = text.get_rect(center=pos)
        screen.blit(text, text_rect)

# Function to spawn materials
def spawn_material(pos, material_type):
    mass = 1
    radius = params["material_radius"]
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 1.0  # Set elasticity to 1.0 for frictionless interaction
    shape.friction = 0.0  # Set friction to 0.0 for frictionless interaction
    space.add(body, shape)
    return [body, shape, 0, time.time(), 0, material_type, 0.0, time.time()]  # Add start time

# Function to calculate movement time based on equipment speed
def calculate_movement_time(equipment_speed):
    # Time per step is 10 divided by the speed
    time_per_step = 10 / equipment_speed  # Time to process one unit
    return time_per_step

# Function to move materials along the conveyor belt
def move_material(material, path, speed):
    material[6] += speed  # Update path progress
    if material[6] >= 1.0:
        material[6] = 0.0
        material[4] += 1
        if material[4] >= len(path):
            material[4] = 0
            material[3] = time.time()
            material[2] += 1  # Move to the next area
    t = material[6]
    start_pos = path[material[4]]
    end_pos = path[(material[4] + 1) % len(path)]
    material[0].position = (start_pos[0] + t * (end_pos[0] - start_pos[0]), start_pos[1] + t * (end_pos[1] - start_pos[1]))

# Function to draw HUD at the bottom
def draw_hud(current_area, time_per_step, object_count, completed_count, auto_move, spawn_enabled):
    hud_params = params["hud_params"]
    hud_height = hud_params["hud_height"]
    hud_bg_color = hud_params["hud_bg_color"]
    hud_border_color = hud_params["hud_border_color"]
    hud_text_color = hud_params["hud_text_color"]
    button_color = hud_params["button_color"]
    button_text_color = hud_params["button_text_color"]
    button_restart_pos = hud_params["button_restart_pos"]
    button_auto_move_pos = hud_params["button_auto_move_pos"]
    button_stop_spawn_pos = (700, height - 90)  # New button position
    button_width = hud_params["button_width"]
    button_height = hud_params["button_height"]

    # Draw HUD background and border
    pygame.draw.rect(screen, hud_bg_color, (0, hud_height, width, 100))
    pygame.draw.rect(screen, hud_border_color, (0, hud_height, width, 100), 2)

    font = pygame.font.Font(None, 24)
    text_current_area = font.render(f"Current Area: {current_area}", True, hud_text_color)
    text_time_per_step = font.render(f"Time per Step: {time_per_step:.2f} s", True, hud_text_color)
    text_object_count = font.render(f"Object Count: {object_count}", True, hud_text_color)
    text_completed_count = font.render(f"Completed Count: {completed_count}", True, hud_text_color)

    screen.blit(text_current_area, (10, hud_height + 10))
    screen.blit(text_time_per_step, (10, hud_height + 40))
    screen.blit(text_object_count, (10, hud_height + 70))
    screen.blit(text_completed_count, (200, hud_height + 70))

    # Draw buttons
    restart_button = pygame.Rect(button_restart_pos[0], button_restart_pos[1], button_width, button_height)
    auto_move_button = pygame.Rect(button_auto_move_pos[0], button_auto_move_pos[1], button_width, button_height)
    stop_spawn_button = pygame.Rect(button_stop_spawn_pos[0], button_stop_spawn_pos[1], button_width, button_height)

    pygame.draw.rect(screen, button_color, restart_button)
    pygame.draw.rect(screen, button_color, auto_move_button)
    pygame.draw.rect(screen, button_color, stop_spawn_button)

    restart_text = font.render("Restart", True, button_text_color)
    auto_move_text = font.render("Auto" if auto_move else "Manual", True, button_text_color)
    stop_spawn_text = font.render("Stop Spawn" if spawn_enabled else "Start Spawn", True, button_text_color)

    screen.blit(restart_text, (button_restart_pos[0] + 10, button_restart_pos[1] + 5))
    screen.blit(auto_move_text, (button_auto_move_pos[0] + 10, button_auto_move_pos[1] + 5))
    screen.blit(stop_spawn_text, (button_stop_spawn_pos[0] + 10, button_stop_spawn_pos[1] + 5))

    return restart_button, auto_move_button, stop_spawn_button


# Function to draw objects with an outline
def draw_objects():
    for material in materials:
        pos = pymunk.pygame_util.to_pygame(material[0].position, screen)
        radius = int(material[1].radius)
        color = (255, 0, 0)  # Default color
        if material[5] == "Cot":
            color = (255, 165, 0)  # Orange for Cotton
        elif material[5] == "Fab":
            color = (0, 0, 255)  # Blue for Fabric
        elif material[5] == "Fin":
            color = (0, 255, 0)  # Green for Finished Material

        pygame.draw.circle(screen, color, pos, radius)
        pygame.draw.circle(screen, (0, 0, 0), pos, radius, 2)  # Outline

        font = pygame.font.Font(None, 24)
        text = font.render(material[5], True, (0, 0, 0))
        text_rect = text.get_rect(center=pos)
        screen.blit(text, text_rect)

# Function to draw conveyor belts
def draw_conveyor_belts():
    pygame.draw.lines(screen, (150, 150, 150), False, params["conveyor_paths"], 10)  # Thicker conveyor belts

# Function to draw the completed area box
def draw_completed_area_box():
    box_params = params["box_params"]
    box_position = params["factory_layout"]["Completed Area"]
    box_width = box_params["box_width"]
    box_height = box_params["box_height"]
    box_color = box_params["box_color"]

    box_rect = pygame.Rect(box_position[0] - box_width // 2, box_position[1] - box_height // 2, box_width, box_height)
    pygame.draw.rect(screen, box_color, box_rect)

    font = pygame.font.Font(None, 24)
    text = font.render("Completed Area", True, (255, 255, 255))
    text_rect = text.get_rect(center=box_position)
    screen.blit(text, text_rect)

# Function to check if material is within distance and time
def check_material_position(material, next_area_pos):
    current_pos = material[0].position
    distance = ((current_pos[0] - next_area_pos[0]) ** 2 + (current_pos[1] - next_area_pos[1]) ** 2) ** 0.5
    elapsed_time = time.time() - material[7]
    if distance > params["distance_threshold"] and elapsed_time > params["time_threshold"]:
        material[0].velocity = (0, 0)  # Freeze the material's movement
    else:
        material[0].velocity = (0, 0)  # Reset velocity to ensure it moves correctly

running = True
materials = []
current_area = "Entrance"
time_per_step = 0
object_count = 0
completed_count = 0
auto_move = True
spawn_enabled = True  # New variable to control spawning
restart_button = None
auto_move_button = None
stop_spawn_button = None
last_spawn_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                current_time = time.time()
                if current_time - last_spawn_time >= 1 / params["item_rate"]:
                    materials.append(spawn_material(params["factory_layout"]["Entrance"], "Cot"))
                    materials.append(spawn_material(params["factory_layout"]["Entrance"], "Fab"))
                    object_count += 2
                    last_spawn_time = current_time
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button and restart_button.collidepoint(event.pos):
                # Restart the simulation
                materials = []
                object_count = 0
                completed_count = 0
                current_area = "Entrance"
                time_per_step = 0
            elif auto_move_button and auto_move_button.collidepoint(event.pos):
                # Toggle automatic/manual movement
                auto_move = not auto_move
            elif stop_spawn_button and stop_spawn_button.collidepoint(event.pos):
                # Toggle spawning of new objects
                spawn_enabled = not spawn_enabled

    screen.fill((255, 255, 255))
    draw_conveyor_belts()
    draw_stations()
    draw_objects()
    draw_completed_area_box()
    restart_button, auto_move_button, stop_spawn_button = draw_hud(current_area, time_per_step, object_count, completed_count, auto_move, spawn_enabled)

    if auto_move:
        # Automatically move materials based on elapsed time
        for material in materials[:]:  # Use a copy of the list to avoid modifying it while iterating
            elapsed_time = time.time() - material[3]
            if elapsed_time >= time_per_step:
                current_area_index = material[2]
                next_area_index = (current_area_index + 1) % len(params["factory_layout"])
                next_area = list(params["factory_layout"].keys())[next_area_index]
                equipment_speed = params["equipment_details"][next_area]["speed"]
                time_per_step = calculate_movement_time(equipment_speed)
                path = params["conveyor_paths"]
                move_material(material, path, params["steps_per_second"])

                # Check if the material has completed the final step
                if next_area_index == len(params["factory_layout"]) - 1:
                    # Turn the completed material into a "Fin" object and keep it in the completed area
                    completed_area_pos = params["factory_layout"]["Completed Area"]
                    materials.append(spawn_material(completed_area_pos, "Fin"))
                    space.remove(material[0], material[1])
                    materials.remove(material)
                    object_count -= 1
                    completed_count += 1

                # Check material position and freeze if necessary
                next_area_pos = params["factory_layout"][next_area]
                check_material_position(material, next_area_pos)

    # Automatically spawn materials at a fixed interval
    if spawn_enabled:
        current_time = time.time()
        if current_time - last_spawn_time >= 1 / params["item_rate"]:
            materials.append(spawn_material(params["factory_layout"]["Entrance"], "Cot"))
            materials.append(spawn_material(params["factory_layout"]["Entrance"], "Fab"))
            object_count += 2
            last_spawn_time = current_time

    space.step(1 / 60.0)  # Update the physics engine
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
