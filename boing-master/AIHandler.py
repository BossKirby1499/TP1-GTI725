from EventHandler import EventHandler
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE

class AIHandler(EventHandler):

    def __init__(self ,game ,x = None ,y =None):
        self.game = game
        self.x = x
        self.y = y
    def execute(self,game,x,y):
        # Returns a number indicating how the computer player will move - e.g. 4 means it will move 4 pixels down
        # the screen.
        self.game = game
        self.x = x
        self.y= y
        # To decide where we want to go, we first check to see how far we are from the ball.
        x_distance = abs(self.game.ball.x - self.x)

        # If the ball is far away, we move towards the centre of the screen (HALF_HEIGHT), on the basis that we don't
        # yet know whether the ball will be in the top or bottom half of the screen when it reaches our position on
        # the X axis. By waiting at a central position, we're as ready as it's possible to be for all eventualities.
        target_y_1 = HALF_HEIGHT

        # If the ball is close, we want to move towards its position on the Y axis. We also apply a small offset which
        # is randomly generated each time the ball bounces. This is to make the computer player slightly less robotic
        # - a human player wouldn't be able to hit the ball right in the centre of the bat each time.
        target_y_2 = self.game.ball.y + self.game.ai_offset

        # The final step is to work out the actual Y position we want to move towards. We use what's called a weighted
        # average - taking the average of the two target Y positions we've previously calculated, but shifting the
        # balance towards one or the other depending on how far away the ball is. If the ball is more than 400 pixels
        # (half the screen width) away on the X axis, our target will be half the screen height (target_y_1). If the
        # ball is at the same position as us on the X axis, our target will be target_y_2. If it's 200 pixels away,
        # we'll aim for halfway between target_y_1 and target_y_2. This reflects the idea that as the ball gets closer,
        # we have a better idea of where it's going to end up.
        weight1 = min(1, x_distance / HALF_WIDTH)
        weight2 = 1 - weight1

        target_y = (weight1 * target_y_1) + (weight2 * target_y_2)

        # Subtract target_y from our current Y position, then make sure we can't move any further than MAX_AI_SPEED
        # each frame
        return min(MAX_AI_SPEED, max(-MAX_AI_SPEED, target_y - self.y))