import pygame 
import components

win_height = 720
win_width = 550

window = pygame.display.set_mode(size=(win_width, win_height)) # create window
ground = components.Ground(win_width=win_width)
pipes = [] 