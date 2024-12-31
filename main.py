# main loop of the program
import pygame 
import config
import components
import population
from sys import exit

pygame.init()
clock = pygame.time.Clock()
population = population.Population(200) # create a population of players initially with 1 play

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def main():
    pipes_spawn_time = 10
    while True: 
        quit_game() # listens to check if user wants to exit

        config.window.fill((0, 0, 0)) # fill the screen with black
        config.ground.draw(window=config.window) # spawn the ground in the loop
        
        if pipes_spawn_time <= 0: 
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for p in config.pipes: 
            p.draw(config.window)
            p.update()
            if p.off_screen: 
                config.pipes.remove(p)

        population.show_generation(config.window)
        if not population.extinct():
            population.update_live_players()
        else: 
            config.pipes.clear()
            population.natural_selection()

        clock.tick(180) # frames per second
        pygame.display.flip()
main()
