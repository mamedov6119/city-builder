from gameconfig import *;
from gui.window import Window;

import arcade, arcade.gui;

class Game:
    window = Window()

    def __init__(self):
        # Setup & launch
        arcade.run()