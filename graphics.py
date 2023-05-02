import pygame
import numpy as np
import matplotlib as plt
import pandas as pd
import random
import time
from pygame.locals import *
from creature import Creature
 
WIDTH = 900
HEIGHT = 500
ALIVE_LIST = []
HUNTED = []
PREDATOR_START = False
BACKGROUND_COLOR = (150, 255, 150)

#When not in predator range
def move_creature(creature):
    global HUNTED, ALIVE_LIST
    
    #Check if within predator, if so, die
    if predator.x - predator.width + 10 < creature._x < predator.x + predator.width + 5 and predator.y - predator.height +10  < creature._y < predator.y + predator.height - 5 and PREDATOR_START:
        if creature._camouflaged and creature._invuln_timer <= 0 and random.random() > 0.5:
            creature._invuln_timer = 300 #amount of invuln
            print(creature._color_diff)
        elif creature._invuln_timer > 0:
            creature._invuln_timer -= 1
        else:
            ALIVE_LIST.remove(creature)
            creature._is_alive = False
            #print("died")
            return
    else:
        creature._invuln_timer = 30
    #Collision with top and bottom
    if creature._y > HEIGHT - creature._size or creature._y < 0:
        creature._y = ((creature._y + creature._size) // HEIGHT) * HEIGHT - (creature._size) * ((creature._y + creature._size) // HEIGHT)
        if creature._angle < np.pi / 2 or creature._angle > -np.pi / 2:
            creature._angle = np.pi
        else:
            creature._angle = 0
    #Collision with right
    if creature._x > WIDTH - creature._size or creature._x < 0:
        creature._x = ((creature._x + creature._size) // WIDTH) * WIDTH - (creature._size) * ((creature._x + creature._size) // WIDTH)
        if creature._angle < np.pi and creature._angle > 0:
            creature._angle = -np.pi / 2
        else:
            creature._angle = np.pi / 2
    #Checks if prey is in predator's range (lock on mechanism)
    elif PREDATOR_START and not creature._camouflaged:
        HUNTED += [creature]
        #Run away area
        if predator.x - 100 < creature._x < predator.x + 175 and predator.y - 100 < creature._y < predator.y + 175:
            creature._angle = np.arctan2((creature._y - predator.y), (creature._x - predator.x)) + creature._run_variance * np.pi / 180
        #Random movement
        elif random.random() > 0.95: 
            creature._angle = random.uniform(0, 2 * np.pi)
    #Random movement
    elif random.random() > 0.95:
        creature._angle = random.uniform(0, 2 * np.pi)

    x_move = np.cos(creature._angle) * creature._speed
    y_move = np.sin(creature._angle) * creature._speed
    pygame.draw.circle(screen, creature._color, (creature._x + x_move, creature._y + y_move), creature._size)
    creature._x += x_move
    creature._y += y_move

def reproduce(creature):
    global PREDATOR_START
    if creature._r_meter <= 0:
        child_params = creature.generate_child_params() #parameters of child
        if child_params != None:
            global ALIVE_LIST  
            child = Creature(*child_params, generation = creature._generation + 1, parent = creature) #init
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
        predator.x += x_move * 1.6
        predator.y += y_move * 1.6
        #p_sense.x += x_move
        #p_sense.y += y_move
    HUNTED = []
    predator.x -= 35
    predator.y -= 35
    screen.blit(p_image, predator)
    predator.x += 35
    predator.y += 35
    return

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

first_guy = Creature(450, 250, "gggggggggggggggggggggggg", 0, None)
ALIVE_LIST += [first_guy]

p_image = pygame.image.load("predator.jpg")
p_image = pygame.transform.scale(p_image, (75, 75))
predator = Rect((-70, (HEIGHT - 75) / 2), (75,75))
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

def tree_traverse(creature, log):
    # tree traversal recursive function which logs all creatures to csv

    # print(f"creature:{creature}")
    # print(f"children:{creature._children}")
    # object_id, genome, is_alive, color, color_diff, camoflauged, size, speed, r_rate, max_offspring, generation, parent_id
    log.write(f"{creature}, {creature._genome}, {creature._is_alive}, {creature._color}, {creature._color_diff}, {creature._camouflaged}, {creature._size}, {creature._speed}, {creature._r_rate}, {creature._max_offspring}, {creature._generation}, {creature._parent}\n")
    for child in creature._children:
        if child is not None:
            tree_traverse(child, log)

def log_histogram():
    sv = pd.read_csv('creature-logSun Apr 30 18_01_32 2023.csv')
    #speed
    # sv[sv [' is_alive'] == 'true'][' is_alive'], ['object_id'], [' genome'], [' color'], [' color_diff'], [' camoflauged'], [' size'], [' speed'], [' r_rate'], [' max_offspring'], [' generation'], [' parent_id']
    alives = sv[sv[' is_alive'] == 'true'][' is_alive'], [' speed'], [' camoflauged']
    plt.hist(sv[' speed'], 20)
    plt.ylabel('Amount of Creatures')
    plt.xlabel('Speed')
    plt.title('Varying Speed in Creatures')
    plt.show()

    #size
    plt.hist(sv[' size'], 20)
    plt.ylabel('Amount of Creatures')
    plt.xlabel('Size')
    plt.title('Varying Size in Creatures')
    plt.show()

    #color dif
    plt.hist(sv[' color_diff'], 20)
    plt.ylabel('Amount of Creatures')
    plt.xlabel('Color Difference')
    plt.title('Color Difference from the Background in Creatures')
    plt.show()


#MAIN LOOP
while True:
    clock.tick(30) #timer 30 fps
    
    #Quits game if ready
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    #pygame.draw.rect(screen, (255, 0, 0), p_sense)
    if time.time() - start <= 12:
        screen.fill(BACKGROUND_COLOR)
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
        log_file = open(f"creature-log-{time.asctime(time.localtime(time.time()))}.csv", "a")
        cumulative_log_file = open("cumulative-creature-log.csv", "a")
        log_file.write(f'object_id, genome, is_alive, color, color_diff, camouflaged, size, speed, r_rate, max_offspring, generation, parent_id\n')
        # print(first_guy)
        # todo make a keyboard thing here so it waits for us to hit a given key
        tree_traverse(first_guy, log_file)
        tree_traverse(first_guy, cumulative_log_file)
        time.sleep(60)
        break
        #tree_traverse(first_guy, log_file)
    pygame.display.update()
    