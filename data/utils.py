import sys
from enum import Enum, auto

import pygame
import pygame_menu
from pygame.surface import Surface

from config.config import Settings, Colors, Misc
from .paths import Portraits


class Window:
    """Class for program window"""

    def __init__(self):
        """Initializes window"""
        self.size = Settings.WINDOW_SIZE
        # The screen is the canvas that we do everything on
        self.screen: Surface = self.set_screen(self.size)
        pygame.display.set_caption(MenuTitles.GAME_TITLE)  # Sets window title

    @staticmethod
    def set_screen(size: Enum):
        if isinstance(size, Enum):
            size = size.value
        return pygame.display.set_mode(size)

    @property
    def screen_width(self):
        return self.screen.get_width()

    @property
    def screen_height(self):
        return self.screen.get_height()

    @property
    def screen_center(self):
        return self.screen.get_rect().center

    @property
    def screen_center_x(self):
        return self.screen.get_rect().centerx

    @property
    def screen_center_y(self):
        return self.screen.get_rect().centery


class Borders:
    def __init__(self, screen: pygame.Surface, rect):
        # Screen begins left top so that is the zero coordinate
        self.left = 0
        # Width of the screen minus width of given Rect (usually a player Rect)
        self.right = screen.get_width() - rect.width
        self.top = 0
        self.bottom = screen.get_height() - rect.height


class MenuPortraits:

    ELIAS = pygame_menu.baseimage.BaseImage(image_path=Portraits.ELIAS.value.path)
    KLAUS = pygame_menu.baseimage.BaseImage(image_path=Portraits.KLAUS.value.path)


def set_music(music_file, volume=Settings.VOLUME):
    """Sets music"""
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


class Background(pygame.sprite.Sprite):
    """Class for background"""

    # TODO only works for menu background right now because of hard coded path, that is needed for draw, that is currently only
    #  used for menu background. bgfun is funky, when you load the image there, the menu starts lagging like shit

    def __init__(self, screen: Surface, img):
        super().__init__()
        self.screen = screen
        # Loads the image and scales it to screen size
        self.image: pygame.Surface = pygame.transform.scale(
            load_img(img, convert=True), self.screen.get_size()
        )

    def draw(self):
        """Draws the image to the screen while scaling the image to the screen size"""
        self.screen.blit(self.image, Misc.DEFAULT_POS)


class CharName(Enum):
    ELIAS = "Elias"
    KLAUS = "Klaus"
    KREUZER = "Kreuzer"

    @property
    def klaus(self):
        return self == self.KLAUS

    @property
    def elias(self):
        return self == self.ELIAS


class MenuTitles:
    PLAYER = "Spieler"
    CHOOSE_ATTR = "Wähle deine Attribute!"
    CHOOSE_CHAR = "Wähle deinen Charakter!"
    GAME_TITLE = "Pylistory v0.1"
    OPTIONS = "Optionen"
    SCENARIOS = "Wähle das Szenario!"
    # CHARACTER_SELECTION_PLAYER_ONE = f"{PLAYER} 1: {CHOOSE_CHAR}"
    CHARACTER_SELECTION_PLAYER_ONE = f"{PLAYER} 1: Elias"
    # CHARACTER_SELECTION_PLAYER_TWO = f"{PLAYER} 2: {CHOOSE_CHAR}"
    CHARACTER_SELECTION_PLAYER_TWO = f"{PLAYER} 2: Klaus"
    ATTRIBUTES_P1 = f"{PLAYER} 1: {CHOOSE_ATTR}"
    ATTRIBUTES_P2 = f"{PLAYER} 2: {CHOOSE_ATTR}"


class GameStates(Enum):
    PAUSED = auto()
    PLAYING = auto()
    DIALOGUE = auto()
    DIALOGUE_DONE = auto()
    NARRATION = auto()
    QUIT = auto()
    CARPENTRY = auto()
    ATTIC = auto()
    TO_BE_CONTINUED = auto()
    QUIZ = auto()

    @property
    def playing(self):
        return self == self.PLAYING

    @property
    def dialogue(self):
        return self == self.DIALOGUE

    @property
    def dialogue_done(self):
        return self == self.DIALOGUE_DONE

    @property
    def paused(self):
        return self == self.PAUSED

    @property
    def narration(self):
        return self == self.NARRATION

    @property
    def quit(self):
        return self == self.QUIT

    @property
    def veggie_store(self):
        return self == self.VEGGIE_STORE

    @property
    def carpentry(self):
        return self == self.CARPENTRY

    @property
    def attic(self):
        return self == self.ATTIC

    @property
    def to_be_continued(self):
        return self == self.TO_BE_CONTINUED

    @property
    def quiz(self):
        return self == self.QUIZ


def load_img(image: pygame.Surface, convert=False, convert_alpha=True):
    img = pygame.image.load(image)
    if convert:
        img.convert()
    if convert_alpha:
        img.convert_alpha()

    return img


def scale_up_double(image: pygame.Surface):
    return pygame.transform.scale2x(image)


def flip_horizontal(image: pygame.Surface):
    return pygame.transform.flip(image, True, False)


def draw_hit_box(screen: pygame.Surface, rect):
    """Draws hit box on given surface for given rect (for testing purposes)"""
    return pygame.draw.rect(screen, Colors.RED, rect, 2)


def continue_text():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                return True
        elif event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                return False
        # Enables quitting the game via X button
        if event.type == pygame.QUIT:
            quit_game()


def mouse_clicked():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
        return False


def quit_game():
    pygame.quit()  # Disables pygame engine
    sys.exit()  # Exits program
