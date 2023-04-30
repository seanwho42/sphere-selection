#todo
#predator
#link creatures in tree
#at end of simulation display full tree

import pygame
import random
from genome import translate, transcribe

class Creature():
    def __init__(self, x, y, genome, generation, children = None, parent = None):
        self._x = x
        self._y = y
        self._angle = 0 # In radians
        self._genome = genome

        attributes = translate(genome)
        
        self._is_alive = True
        self._color = attributes[0]
        self._size = attributes[1] / 3
        self._speed = attributes[2] / 63
        self._r_rate = attributes[3] * 10 # Reproduction rate
        self._r_meter = self._r_rate #Holds how long until next reproduction
        self._max_offspring = attributes[4]

        self._generation = generation
        self._children = [children]
        self._parent = parent

    def generate_child_params(self):
        if self._max_offspring != 0:
            child_x = self._x + random.uniform(-5, 5)
            child_y = self._y + random.uniform(-5, 5)
            child_genome = transcribe(self._genome)

            self._max_offspring -= 1

            return child_x, child_y, child_genome
        return None

    """
    def traverse_tree(self, root):
        layers = [root]
        while layers[layers.len() - 1].len() != 0:
            temp_list = []
            for i in layers[layers.len() - 1]:
                for j in range(i._children):
                    temp_list.append(current._chidlren[j])
                layers.append(temp_list)
        return(layers)
    """

    def get_data(self):
        return self.data

    # Sets this node's data.
    def set_data(self, new_data):
        self.data = new_data

    # Gets this node's next pointer.
    def get_children(self):
        return self._children

    # Sets this node's next pointer.
    def append_child(self, child):
        self._children.append(child)

    # Gets this node's previous pointer.
    def get_parent(self):
        return self._parent