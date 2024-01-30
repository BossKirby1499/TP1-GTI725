import pgzero, pgzrun, pygame
import keyboard
import math, sys, random
from EventHandler import EventHandler
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
class BatHandlerPlayer2(EventHandler):

    def __init__(self):
        self

    def execute(self,game=None,x=None,y=None):
        move = 0
        if keyboard.is_pressed("m"):
            move = PLAYER_SPEED
        elif keyboard.is_pressed("k"):
            move = -PLAYER_SPEED
        return move