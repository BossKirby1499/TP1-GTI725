import pgzero, pgzrun, pygame
import math, sys, random
from constants import WIDTH,HALF_HEIGHT,HALF_WIDTH,HEIGHT,MAX_AI_SPEED,PLAYER_SPEED,TITLE
from enum import Enum
from Bat import Bat
from Ball import Ball
from ScoreUpdate import ScoreUpdate
from BatHandler import BatHandler
from BatHandlerPlayer2 import BatHandlerPlayer2
from  AIHandler import AIHandler

# Check Python version number. sys.version_info gives version as a tuple, e.g. if (3,7,2,'final',0) for version 3.7.2.
# Unlike many languages, Python can compare two tuples in the same way that you can compare numbers.
if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
    sys.exit()

# Check Pygame Zero version. This is a bit trickier because Pygame Zero only lets us get its version number as a string.
# So we have to split the string into a list, using '.' as the character to split on. We convert each element of the
# version number into an integer - but only if the string contains numbers and nothing else, because it's possible for
# a component of the version to contain letters as well as numbers (e.g. '2.0.dev0')
# We're using a Python feature called list comprehension - this is explained in the Bubble Bobble/Cavern chapter.
pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
    sys.exit()



def sign(x):
    # Returns -1 or 1 depending on whether number is positive or negative
    return -1 if x < 0 else 1


class Game:
    def __init__(self, controls1 = None, controls2 = None):
        # Create a list of two bats, giving each a player number and a function to use to receive
        # control inputs (or the value None if this is intended to be an AI player)
        self.observers = []
        
        self.bats = [Bat(0, controls1,self), Bat(1, controls2,self)]

        # Create a ball object
        self.ball = Ball(-1,self)

        # Create an empty list which will later store the details of currently playing impact
        # animations - these are displayed for a short time every time the ball bounces
        self.impacts = []

        # Add an offset to the AI player's target Y position, so it won't aim to hit the ball exactly
        # in the centre of the bat
        self.ai_offset = 0

    def attach(self,observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)
    
    def update(self):
        # Update all active objects
        for obj in self.bats + [self.ball] + self.impacts:
            obj.update()

        # Remove any expired impact effects from the list. We go through the list backwards, starting from the last
        # element, and delete any elements those time attribute has reached 10. We go backwards through the list
        # instead of forwards to avoid a number of issues which occur in that scenario. In the next chapter we will
        # look at an alternative technique for removing items from a list, using list comprehensions.
        for i in range(len(self.impacts) - 1, -1, -1):
            if self.impacts[i].time >= 10:
                del self.impacts[i]
        self.notify()
        # Has ball gone off the left or right edge of the screen?
       # if self.ball.out():
            # Work out which player gained a point, based on whether the ball
            # was on the left or right-hand side of the screen
           # scoring_player = 1 if self.ball.x < WIDTH // 2 else 0
            #losing_player = 1 - scoring_player

            # We use the timer of the player who has just conceded a point to decide when to create a new ball in the
            # centre of the level. This timer starts at zero at the beginning of the game and counts down by one every
            # frame. Therefore, on the frame where the ball first goes off the screen, the timer will be less than zero.
            # We set it to 20, which means that this player's bat will display a different animation frame for 20
            # frames, and a new ball will be created after 20 frames
         #   if self.bats[losing_player].timer < 0:
          #      self.bats[scoring_player].score += 1

          #      game.play_sound("score_goal", 1)

           #     self.bats[losing_player].timer = 20

          #  elif self.bats[losing_player].timer == 0:
                # After 20 frames, create a new ball, heading in the direction of the player who just missed the ball
          #      direction = -1 if losing_player == 0 else 1
          #      self.ball = Ball(direction,self)

    def draw(self):
        # Draw background
        screen.blit("table", (0,0))

        # Draw 'just scored' effects, if required
        for p in (0,1):
            if self.bats[p].timer > 0 and game.ball.out():
                screen.blit("effect" + str(p), (0,0))

        # Draw bats, ball and impact effects - in that order. Square brackets are needed around the ball because
        # it's just an object, whereas the other two are lists - and you can't directly join an object onto a
        # list without first putting it in a list
        for obj in self.bats + [self.ball] + self.impacts:
            obj.draw()

        # Display scores - outer loop goes through each player
        for p in (0,1):
            # Convert score into a string of 2 digits (e.g. "05") so we can later get the individual digits
            score = "{0:02d}".format(self.bats[p].score)
            # Inner loop goes through each digit
            for i in (0,1):
                # Digit sprites are numbered 00 to 29, where the first digit is the colour (0 = grey,
                # 1 = blue, 2 = green) and the second digit is the digit itself
                # Colour is usually grey but turns red or green (depending on player number) when a
                # point has just been scored
                colour = "0"
                other_p = 1 - p
                if self.bats[other_p].timer > 0 and game.ball.out():
                    colour = "2" if p == 0  else "1"
                image = "digit" + colour + str(score[i])
                screen.blit(image, (255 + (160 * p) + (i * 55), 46))

    def play_sound(self, name, count=1, menu_sound=False):
        # Some sounds have multiple varieties. If count > 1, we'll randomly choose one from those
        # We don't play any in-game sound effects if player 0 is an AI player - as this means we're on the menu
        # Updated Jan 2022 - some Pygame installations have issues playing ogg sound files. play_sound can skip sound
        # errors without stopping the game, but it previously couldn't be used for menu-only sounds
        if isinstance(self.bats[0].eventhandler, AIHandler) or menu_sound:
            # Pygame Zero allows you to write things like 'sounds.explosion.play()'
            # This automatically loads and plays a file named 'explosion.wav' (or .ogg) from the sounds folder (if
            # such a file exists)
            # But what if you have files named 'explosion0.ogg' to 'explosion5.ogg' and want to randomly choose
            # one of them to play? You can generate a string such as 'explosion3', but to use such a string
            # to access an attribute of Pygame Zero's sounds object, we must use Python's built-in function getattr
            try:
                getattr(sounds, name + str(random.randint(0, count - 1))).play()
            except Exception as e:
                pass


class State(Enum):
    MENU = 1
    PLAY = 2
    GAME_OVER = 3

num_players = 1

# Is space currently being held down?
space_down = False


# Pygame Zero calls the update and draw functions each frame

def update():
    global state, game, num_players, space_down

    # Work out whether the space key has just been pressed - i.e. in the previous frame it wasn't down,
    # and in this frame it is.
    space_pressed = False
    if keyboard.space and not space_down:
        space_pressed = True
    space_down = keyboard.space

    if state == State.MENU:
        if space_pressed:
            # Switch to play state, and create a new Game object, passing it the controls function for
            # player 1, and if we're in 2 player mode, the controls function for player 2 (otherwise the
            # 'None' value indicating this player should be computer-controlled)
            state = State.PLAY
            batHandler1 = BatHandler()
            batHandler2 = BatHandlerPlayer2()
            scoreUpdate = ScoreUpdate()

            game = Game(batHandler1,   (batHandler2 if num_players == 2 else None))
            game.attach(scoreUpdate)
        else:
            # Detect up/down keys
            if num_players == 2 and keyboard.up:
                game.play_sound("up", menu_sound=True)
                num_players = 1
            elif num_players == 1 and keyboard.down:
                game.play_sound("down", menu_sound=True)
                num_players = 2

            # Update the 'attract mode' game in the background (two AIs playing each other)

            game.update()

    elif state == State.PLAY:
        # Has anyone won?
        if max(game.bats[0].score, game.bats[1].score) > 9:
            state = State.GAME_OVER
        else:
            game.update()

    elif state == State.GAME_OVER:
        if space_pressed:
            # Reset to menu state
            state = State.MENU
            num_players = 1

            # Create a new Game object, without any players
            game = Game()

def draw():
    game.draw()

    if state == State.MENU:
        menu_image = "menu" + str(num_players - 1)
        screen.blit(menu_image, (0,0))

    elif state == State.GAME_OVER:
        screen.blit("over", (0,0))


# The mixer allows us to play sounds and music
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)

    music.play("theme")
    music.set_volume(0.3)
except Exception:
    # If an error occurs (e.g. no sound device), just ignore it
    pass

# Set the initial game state
state = State.MENU

# Create a new Game object, without any players
game = Game()

# Tell Pygame Zero to start - this line is only required when running the game from an IDE such as IDLE or PyCharm
pgzrun.go()
