import pygame
import numpy as np
import random
import time
from pygame.locals import *
from creature import Creature
 
WIDTH = 900
HEIGHT = 500
ALIVE_LIST = []
HUNTED = []
PREDATOR_START = False

#When not in predator range
def move_creature(creature):
    global HUNTED, ALIVE_LIST
    
    #Check if within predator, if so, die
    if predator.x - 30 < creature._x < predator.x + 105 and predator.y - 30 < creature._y < predator.y + 105 and PREDATOR_START:
        ALIVE_LIST.remove(creature)
        print("died")
        return
    #Check if within hunting radius, if so, run away from predator 
    if predator.x - 1000 < creature._x < predator.x + 1750 and predator.y - 1000 < creature._y < predator.y + 1750 and PREDATOR_START:
        HUNTED += [creature]

    if random.random() > 0.95:
        creature._angle = random.uniform(0, 2 * np.pi)
    x_move = np.cos(creature._angle) * creature._speed
    y_move = np.sin(creature._angle) * creature._speed
    pygame.draw.circle(screen, creature._color, (creature._x + x_move, creature._y + y_move), creature._size)
    creature._x += x_move
    creature._y += y_move
    if creature._x > WIDTH - creature._size / 2 or creature._x < 0 or creature._y > HEIGHT - creature._size / 2 or creature._y < 0:
        creature._angle = creature._angle - 180

def reproduce(creature):
    global PREDATOR_START
    if creature._r_meter <= 0:
        child_params = creature.generate_child_params() #parameters of child
        if child_params != None:
            global ALIVE_LIST  
            child = Creature(*child_params, generation = creature._generation + 1, parent = creature) #init
            print(child._generation)
            if child._generation == 3:
                PREDATOR_START = True
            creature.append_child(child)
            ALIVE_LIST  += [child] 
        creature._r_meter = creature._r_rate
    creature._r_meter -= 1

def move_predator():
    global HUNTED
    if len(HUNTED) != 0:
        hunted = None
        best_score = 0
        for creature in HUNTED:
            distance = np.sqrt(np.abs(predator.x - creature._x)**2 + np.abs(predator.y - creature._y)**2)
            score = creature._size / distance
            if score > best_score:
                best_score = score
                hunted = creature
        #Compute angle to hunted
        angle = np.arctan2((hunted._y - predator.y), (hunted._x - predator.x))
        x_move = np.cos(angle) 
        y_move = np.sin(angle)
        #Move towards hunted
        predator.x += x_move * 1.2
        predator.y += y_move * 1.2
        #p_sense.x += x_move
        #p_sense.y += y_move
    HUNTED = []
    screen.blit(p_image, predator)
    return

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

first_guy = Creature(450, 250, "gggggggggggggggggggggggg", 0, None)
ALIVE_LIST += [first_guy]

p_image = pygame.image.load("predator.jpg")
p_image = pygame.transform.scale(p_image, (75, 75))
predator = Rect((-70, 250), (75,75))
#p_sense = Rect((100, 0), (2750, 275))

clock = pygame.time.Clock()

"""
# pick a font you have and set its size
myfont = pygame.font.SysFont("Comic Sans MS", 30)
# apply it to text on a label
label = myfont.render("Python and Pygame are Fun!", 1, (255,0,0))
# put the label object on the screen at point x=100, y=100
"""

start = time.time()

#MAIN LOOP
while True:
    clock.tick(30) #timer 30 fps
    
    #Quits game if ready
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    #pygame.draw.rect(screen, (255, 0, 0), p_sense)
    if time.time() - start <= 30:
        screen.fill((150, 255, 150))
        #screen.blit(label, (100, 100))
        for creature in ALIVE_LIST:
            move_creature(creature)
            reproduce(creature)
        if PREDATOR_START:
            move_predator()
    else:
        screen.fill((0, 0, 0))
        for creature in ALIVE_LIST:
            pygame.draw.circle(screen, creature._color, (creature._x, creature._y), creature._size)
        screen.blit(p_image, predator)
        pass #display end analysis
    pygame.display.update()
    