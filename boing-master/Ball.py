import pgzero, pgzrun, pygame
import math, sys, random
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
from enum import Enum
from pgzero.builtins import Actor, animate, keyboard
from Impact import Impact

class Ball(Actor):
    def __init__(self, dx,game):
        super().__init__("ball", (0,0))

        self.x, self.y = HALF_WIDTH, HALF_HEIGHT

        # dx and dy together describe the direction in which the ball is moving. For example, if dx and dy are 1 and 0,
        # the ball is moving to the right, with no movement up or down. If both values are negative, the ball is moving
        # left and up, with the angle depending on the relative values of the two variables. If you're familiar with
        # vectors, dx and dy represent a unit vector. If you're not familiar with vectors, see the explanation in the
        # book.
        self.dx, self.dy = dx, 0

        self.speed = 5
        self.game = game

    def update(self):
        # Each frame, we move the ball in a series of small steps - the number of steps being based on its speed attribute
        for i in range(self.speed):
            # Store the previous x position
            original_x = self.x

            # Move the ball based on dx and dy
            self.x += self.dx
            self.y += self.dy

            # Check to see if ball needs to bounce off a bat

            # To determine whether the ball might collide with a bat, we first measure the horizontal distance from the
            # ball to the centre of the screen, and check to see if its edge has gone beyond the edge of the bat.
            # The centre of each bat is 40 pixels from the edge of the screen, or to put it another way, 360 pixels
            # from the centre of the screen. The bat is 18 pixels wide and the ball is 14 pixels wide. Given that these
            # sprites are anchored from their centres, when determining if they overlap or touch, we need to look at
            # their half-widths - 9 and 7. Therefore, if the centre of the ball is 344 pixels from the centre of the
            # screen, it can bounce off a bat (assuming the bat is in the right position on the Y axis - checked
            # shortly afterwards).
            # We also check the previous X position to ensure that this is the first frame in which the ball crossed the threshold.
            if abs(self.x - HALF_WIDTH) >= 344 and abs(original_x - HALF_WIDTH) < 344:

                # Now that we know the edge of the ball has crossed the threshold on the x-axis, we need to check to
                # see if the bat on the relevant side of the arena is at a suitable position on the y-axis for the
                # ball collide with it.

                if self.x < HALF_WIDTH:
                    new_dir_x = 1
                    bat = self.game.bats[0]
                else:
                    new_dir_x = -1
                    bat = self.game.bats[1]

                difference_y = self.y - bat.y

                if difference_y > -64 and difference_y < 64:
                    # Ball has collided with bat - calculate new direction vector

                    # To understand the maths used below, we first need to consider what would happen with this kind of
                    # collision in the real world. The ball is bouncing off a perfectly vertical surface. This makes for a
                    # pretty simple calculation. Let's take a ball which is travelling at 1 metre per second to the right,
                    # and 2 metres per second down. Imagine this is taking place in space, so gravity isn't a factor.
                    # After the ball hits the bat, it's still going to be moving at 2 m/s down, but it's now going to be
                    # moving 1 m/s to the left instead of right. So its speed on the y-axis hasn't changed, but its
                    # direction on the x-axis has been reversed. This is extremely easy to code - "self.dx = -self.dx".
                    # However, games don't have to perfectly reflect reality.
                    # In Pong, hitting the ball with the upper or lower parts of the bat would make it bounce diagonally
                    # upwards or downwards respectively. This gives the player a degree of control over where the ball
                    # goes. To make for a more interesting game, we want to use realistic physics as the starting point,
                    # but combine with this the ability to influence the direction of the ball. When the ball hits the
                    # bat, we're going to deflect the ball slightly upwards or downwards depending on where it hit the
                    # bat. This gives the player a bit of control over where the ball goes.

                    # Bounce the opposite way on the X axis
                    self.dx = -self.dx

                    # Deflect slightly up or down depending on where ball hit bat
                    self.dy += difference_y / 128

                    # Limit the Y component of the vector so we don't get into a situation where the ball is bouncing
                    # up and down too rapidly
                    self.dy = min(max(self.dy, -1), 1)

                    # Ensure our direction vector is a unit vector, i.e. represents a distance of the equivalent of
                    # 1 pixel regardless of its angle
                    self.dx, self.dy = self.normalised(self.dx,self.dy)

                    # Create an impact effect
                    self.game.impacts.append(Impact((self.x - new_dir_x * 10, self.y)))

                    # Increase speed with each hit
                    self.speed += 1

                    # Add an offset to the AI player's target Y position, so it won't aim to hit the ball exactly
                    # in the centre of the bat
                    self.game.ai_offset = random.randint(-10, 10)

                    # Bat glows for 10 frames
                    bat.timer = 10

                    # Play hit sounds, with more intense sound effects as the ball gets faster
                    self.game.play_sound("hit", 5)  # play every time in addition to:
                    if self.speed <= 10:
                        self.game.play_sound("hit_slow", 1)
                    elif self.speed <= 12:
                        self.game.play_sound("hit_medium", 1)
                    elif self.speed <= 16:
                        self.game.play_sound("hit_fast", 1)
                    else:
                        self.game.play_sound("hit_veryfast", 1)

            # The top and bottom of the arena are 220 pixels from the centre
            if abs(self.y - HALF_HEIGHT) > 220:
                # Invert vertical direction and apply new dy to y so that the ball is no longer overlapping with the
                # edge of the arena
                self.dy = -self.dy
                self.y += self.dy

                # Create impact effect
                self.game.impacts.append(Impact(self.pos))

                # Sound effect
                self.game.play_sound("bounce", 5)
                self.game.play_sound("bounce_synth", 1)

    def out(self):
        # Has ball gone off the left or right edge of the screen?
        return self.x < 0 or self.x > WIDTH
    
    def normalised(self,x, y):
    # Return a unit vector
    # Get length of vector (x,y) - math.hypot uses Pythagoras' theorem to get length of hypotenuse
    # of right-angle triangle with sides of length x and y
    # todo note on safety
        length = math.hypot(x, y)
        return (x / length, y / length)
