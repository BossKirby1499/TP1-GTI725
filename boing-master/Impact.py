import pgzero, pgzrun, pygame
import math, sys, random
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
from enum import Enum
from pgzero.builtins import Actor, animate, keyboard

# Class for an animation which is displayed briefly whenever the ball bounces
class Impact(Actor):
    def __init__(self, pos):
        super().__init__("blank", pos)
        self.time = 0

    def update(self):
        # There are 5 impact sprites numbered 0 to 4. We update to a new sprite every 2 frames.
        self.image = "impact" + str(self.time // 2)

        # The Game class maintains a list of Impact instances. In Game.update, if the timer for an object
        # has gone beyond 10, the object is removed from the list.
        self.time += 1