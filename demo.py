import pygame
import TextileFactory

def main():
    # Initialize Pygame
    #pygame.init()

    # Run the render simulation in image mode
    TextileFactory.render_simulation(params_file='params.json', print_only=True)

if __name__ == "__main__":
    main()