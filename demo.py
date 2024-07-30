import pygame
from TextileFactory.render import render_simulation

def main():
    # Initialize Pygame
    pygame.init()

    # Run the render simulation in image mode
    render_simulation(params_file='params.json', print_only=False)

if __name__ == "__main__":
    main()