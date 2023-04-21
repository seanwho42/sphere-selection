import pygame
import numpy as np
import random
from pygame.locals import *
from creature import Creature
 
WIDTH = 900
HEIGHT = 500
ALIVE_LIST = []

#When not in predator range
def move_creature(creature):
    if random.random() > 0.95:
        creature._angle = random.uniform(0, 2 * np.pi)
    x_move = np.cos(creature._angle) * creature._speed
    y_move = np.sin(creature._angle) * creature._speed
    pygame.draw.circle(screen, creature._color, (creature._x + x_move, creature._y + y_move), creature._size)
    creature._x += x_move
    creature._y += y_move

def reproduce(creature):
    if creature._r_meter <= 0:
        child_params = creature.generate_child_params() #parameters of child
        if child_params != None:
            global ALIVE_LIST  
            child = Creature(*child_params, parent = creature) #init
            creature.append_child(child)
            ALIVE_LIST  += [child] 
        creature._r_meter = creature._r_rate
    creature._r_meter -= 1

pygame.init()
	
screen = pygame.display.set_mode((WIDTH,HEIGHT))

first_guy = Creature(450, 250, "gggggggggggggggggggggggg", None)
ALIVE_LIST += [first_guy]

clock = pygame.time.Clock()

#MAIN LOOP
while True:
    clock.tick(30) #timer 30 fps
    
    #Quits game if ready
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    screen.fill((255,255,255))

    for creature in ALIVE_LIST :
        move_creature(creature)
        reproduce(creature)
    
    pygame.display.update()