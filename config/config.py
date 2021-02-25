"""Module for settings"""
from enum import Enum

import pygame_menu
from pygame_menu import font

from data.paths import Paths


class Colors:
    """Class for colors"""

    BLACK = (0, 0, 0)
    NEAR_BLACK = (1, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    TEXTBOX = (247, 224, 158)


class Resolutions(Enum):
    DEFAULT = (1280, 704)
    CARPENTRY = (1500, 1000)
    REICH_LAW_GAZETTE = (650, 867)


class Settings:
    MUTE = 1
    MENU_ENABLED = 1
    SELECTABLE_CHARS = False
    ATTRIBUTES_ENABLED = False
    # TODO make variable according to resolution
    WINDOW_SIZE = Resolutions.DEFAULT  # px
    FPS = 30
    TARGET_FPS = 60
    PLAYER_VEL = 3  # TODO change according to resolution
    # The lower the value, the faster the animation
    ANIMATION_SPEED = 150  # milli seconds
    DOUBLE_SCALE = True
    DRAW_HIT_BOXES = False
    VOLUME = 0.2  # %
    MENU_VOLUME = 0.2  # %
    PRINT_MOUSE_POS = False
    TEST = 0


class ThemeSettings:
    OPACITY = 0.7
    FONT = font.FONT_OPEN_SANS_ITALIC
    FONT_COLOR = Colors.WHITE
    MENUBAR = pygame_menu.widgets.MENUBAR_STYLE_NONE


class TextBoxSettings:
    TEXT_COLOR = Colors.BLACK
    FONT_NAME = Paths.DEFAULT_FONT
    FONT_SIZE = 22
    NARRATION_TEXT_WIDTH = 750
    NARRATION_BOX_SIZE = (800, 700)
    NARRATION_TEXT_OFFSET_LEFT = 50
    NARRATION_TEXT_OFFSET_TOP = 20
    # Dialogue has no extra box width because the base img is already big enough
    DIALOGUE_TEXT_WIDTH = 700
    DIALOGUE_TEXT_OFFSET_LEFT = 80
    DIALOGUE_TEXT_OFFSET_TOP = 50
    ITEMS_LIST_BOX_OFFSET_LEFT = 350
    ITEMS_LIST_BOX_SIZE = (800, 200)
    ITEMS_LIST_TEXT_OFFSET_TOP = 20
    ITEMS_LIST_TEXT_OFFSET_LEFT = 100
    UNIFORM_DESCRIPTION_BOX_SIZE = (1250, 150)
    UNIFORM_DESCRIPTION_TEXT_WIDTH = 1000
    UNIFORM_DESCRIPTION_BOX_OFFSET_LEFT = 260
    UNIFORM_DESCRIPTION_TEXT_OFFSET_TOP = 10
    UNIFORM_DESCRIPTION_TEXT_OFFSET_LEFT = 200
    OFFSET_CHAR_PORTRAIT_X = 15
    OFFSET_CHAR_PORTRAIT_Y = 10
    MAX_CHAR_DIALOGUE = 177
    # TODO
    # 340
    # 764


class QuizSettings:
    WAIT_TIME = 2000  # ms
    WAIT_TIME_LONGER = 4000  # ms


class Misc:
    """Miscellaneous stuff"""

    DEFAULT_POS = (0, 0)
    DOCUMENT_POS = (-630, 0)
