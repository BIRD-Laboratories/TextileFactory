import pygame
from .main import FactorySimulation
from .params import load_params

def render_simulation(params_file='params.json', print_only=False):
    params = load_params(params_file)
    simulation = FactorySimulation(params, print_only=print_only)

    pygame.init()
    screen = pygame.display.set_mode((params['global_resolution'][0], params['global_resolution'][1]))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.run()

        # Clear the screen
        screen.fill((255, 255, 255))

        # Render the state array
        state_array = simulation.physics.get_state_array()
        for x in range(len(state_array)):
            for y in range(len(state_array[x])):
                if state_array[x][y] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, 1, 1))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    render_simulation()