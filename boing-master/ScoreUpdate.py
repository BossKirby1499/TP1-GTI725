import pgzero, pgzrun, pygame
import math, sys, random
from Observer import Observer 
from Ball import Ball
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
class ScoreUpdate(Observer):
    def update(self, game):
        if game.ball.out():
            # Work out which player gained a point, based on whether the ball
            # was on the left or right-hand side of the screen
            scoring_player = 1 if game.ball.x < WIDTH // 2 else 0
            losing_player = 1 - scoring_player

            # We use the timer of the player who has just conceded a point to decide when to create a new ball in the
            # centre of the level. This timer starts at zero at the beginning of the game and counts down by one every
            # frame. Therefore, on the frame where the ball first goes off the screen, the timer will be less than zero.
            # We set it to 20, which means that this player's bat will display a different animation frame for 20
            # frames, and a new ball will be created after 20 frames
            if game.bats[losing_player].timer < 0:
                game.bats[scoring_player].score += 1

                game.play_sound("score_goal", 1)

                game.bats[losing_player].timer = 20

            elif game.bats[losing_player].timer == 0:
                # After 20 frames, create a new ball, heading in the direction of the player who just missed the ball
                direction = -1 if losing_player == 0 else 1
                game.ball = Ball(direction,game)
