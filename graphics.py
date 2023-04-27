import pygame
import numpy as np
import random
from pygame.locals import *
from creature import Creature
 
WIDTH = 900
HEIGHT = 500
ALIVE_LIST = []
HUNTED = []

#When not in predator range
def move_creature(creature):
    global HUNTED, ALIVE_LIST
    
    #Check if within predator, if so, die
    if predator.x - 5 < creature._x < predator.x + 75 and predator.y - 5 < creature._y < predator.y + 75:
        ALIVE_LIST.remove(creature)
        print("died")
        return
    #Check if within hunting radius, if so, run away from predator 
    if predator.x - 100 < creature._x < predator.x + 175 and predator.y - 100 < creature._y < predator.y + 175:
        HUNTED += [creature]

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
        predator.x += x_move
        predator.y += y_move
        #p_sense.x += x_move
        #p_sense.y += y_move
    HUNTED = []
    return

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

first_guy = Creature(450, 250, "gggggggggggggggggggggggg", None)
ALIVE_LIST += [first_guy]

p_image = pygame.image.load("predator.jpg")
p_image = pygame.transform.scale(p_image, (75, 75))
predator = Rect((200, 100), (75,75))
#p_sense = Rect((100, 0), (2750, 275))

clock = pygame.time.Clock()

# pick a font you have and set its size
myfont = pygame.font.SysFont("Comic Sans MS", 30)
# apply it to text on a label
label = myfont.render("Python and Pygame are Fun!", 1, (255,0,0))
# put the label object on the screen at point x=100, y=100


#MAIN LOOP
while True:
    clock.tick(30) #timer 30 fps
    
    #Quits game if ready
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    screen.fill((255,255,255))
    #pygame.draw.rect(screen, (255, 0, 0), p_sense)
    screen.blit(p_image, predator)

    #screen.blit(label, (100, 100))
    

    for creature in ALIVE_LIST :
        move_creature(creature)
        reproduce(creature)
        move_predator()
    
    pygame.display.update()