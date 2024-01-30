import pgzero, pgzrun, pygame
import keyboard
import math, sys, random
from EventHandler import EventHandler
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
class BatHandler(EventHandler):

    def __init__(self):
        self

    def execute(self,game=None,x=None,y=None):
        move = 0
        if keyboard.is_pressed(keyboard.KEY_DOWN):
            move = PLAYER_SPEED
        elif keyboard.is_pressed(keyboard.KEY_UP):
            move = -PLAYER_SPEED
        return move