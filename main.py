"""
Main script of the Serious Game Pylistory.
Utilizes the functionality of pygame-menu by Pablo Pizarro R. and parts of EXAMPLE - GAME SELECTOR and
EXAMPLE - DYNAMIC WIDGET UPDATE.
(https://github.com/ppizarror/pygame-menu/blob/master/pygame_menu/examples/game_selector.py).

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""
import os

import pygame

import data.utils
from data import public
from data.utils import Window
from config.config import Settings
from data.game1933 import Game1933
from data.menus.main_menu import MainMenu


class Pylistory:
    """Main class"""

    def __init__(self):
        """Starts the main program."""

        # Window starting position
        x = 200
        y = 30
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (x, y)

        pygame.init()
        # Init window
        self.window = Window()
        # Flag that defines if the program is running or not
        self.running = True
        if Settings.MENU_ENABLED:
            self.main_menu = MainMenu(self.window)
        self.main_loop()

    def main_loop(self):
        """Main program loop"""
        if Settings.MENU_ENABLED:
            while self.running:
                # Menu loop
                public.clock.tick(Settings.FPS)  # Sets frame rate

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # User clicked close
                        self.running = False  # We are done so loop gets closed
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            data.utils.quit_game()

                self.main_menu.menu.mainloop(
                    surface=self.window.screen, bgfun=self.main_menu.background.draw
                )
        else:
            game = Game1933(self.window)
            game.start_scenario()


if __name__ == "__main__":
    main = Pylistory()
