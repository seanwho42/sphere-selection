import pygame
import random
from genome import translate, transcribe

class Creature():

    def __init__(self, x, y, genome):
        self._x = x
        self._y = y
        self._angle = 0 # In radians
        self._genome = genome

        attributes = translate(genome)
        
        self._color = attributes[0]
        self._size = attributes[1] / 3
        self._speed = attributes[2] / 63
        self._r_rate = attributes[3] * 10 # Reproduction rate
        self._r_meter = self._r_rate #Holds how long until next reproduction
        self._max_offspring = attributes[4]

    def generate_child(self):
        if self._max_offspring != 0:
            child_x = self._x + random.uniform(-5, 5)
            child_y = self._y + random.uniform(-5, 5)
            child_genome = transcribe(self._genome)

            return child_x, child_y, child_genome
        return None