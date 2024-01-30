import pgzero, pgzrun, pygame
import math, sys, random
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
from enum import Enum
from pgzero.builtins import Actor, animate, keyboard
from AIHandler import AIHandler

class Bat(Actor):

    def __init__(self, player, eventhandler,game=None):

        x = 40 if player == 0 else 760
        y = HALF_HEIGHT
        super().__init__("blank", (x, y))
        self.game = game
        self.player = player
        self.score = 0

        # move_func is a function we may or may not have been passed by the code which created this object. If this bat
        # is meant to be player controlled, move_func will be a function that when called, returns a number indicating
        # the direction and speed in which the bat should move, based on the keys the player is currently pressing.
        # If move_func is None, this indicates that this bat should instead be controlled by the AI method.
        if eventhandler != None:
            self.eventhandler = eventhandler
        else:
            self.eventhandler = AIHandler(self.game,self.x,self.y)
        
        # Each bat has a timer which starts at zero and counts down by one every frame. When a player concedes a point,
        # their timer is set to 20, which causes the bat to display a different animation frame. It is also used to
        # decide when to create a new ball in the centre of the screen - see comments in Game.update for more on this.
        # Finally, it is used in Game.draw to determine when to display a visual effect over the top of the background
        self.timer = 0

    def update(self):
        self.timer -= 1

        # Our movement function tells us how much to move on the Y axis
        y_movement = self.eventhandler.execute(self.game,self.x,self.y)

        # Apply y_movement to y position, ensuring bat does not go through the side walls
        self.y = min(400, max(80, self.y + y_movement))

        # Choose the appropriate sprite. There are 3 sprites per player - e.g. bat00 is the left-hand player's
        # standard bat sprite, bat01 is the sprite to use when the ball has just bounced off the bat, and bat02
        # is the sprite to use when the bat has just missed the ball and the ball has gone out of bounds.
        # bat10, 11 and 12 are the equivalents for the right-hand player

        frame = 0
        if self.timer > 0:
            if self.game.ball.out():
                frame = 2
            else:
                frame = 1

        self.image = "bat" + str(self.player) + str(frame)
    