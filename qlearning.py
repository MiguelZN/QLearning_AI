'''
Miguel Zavala
4/26/20
CISC481-Intro to AI
Homework 4: Q-learning
Dr.Rahmat
'''

from enum import Enum

class TILE_TYPES(Enum):
    START = 'start'
    GOAL = 'goal'
    FORBIDDEN = 'forbidden'
    WALL = 'wall'
    ORDINARY = 'ordinary'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other,TILE_TYPES):
            if(other.value==self.value):
                return True
        elif(isinstance(other,str)):
            if(self.value==other):
                return True

        return False

class Tile:
    def __init__(self, type=TILE_TYPES.ORDINARY):
        self.value = None
        self.type = type

class Board(list):
    def __init__(self):
        ''

print(TILE_TYPES.ORDINARY == 'ordinary')
print(TILE_TYPES.ORDINARY == TILE_TYPES.ORDINARY)