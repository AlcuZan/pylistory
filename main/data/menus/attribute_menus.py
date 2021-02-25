from abc import abstractmethod

from data import public
from data.menus.menus import SubMenu
from data.game1933 import Game1933
from data.player import Character
from data.utils import Window, MenuTitles


class MenuAttributeSelection(SubMenu):
    """Base class for attribute menus."""

    def __init__(
        self, window: Window, char: Character, has_confirm_button: bool = True
    ):
        super().__init__(window, has_confirm_button=has_confirm_button)
        self.char: Character = char
        self.add_selector_intelligence()
        self.add_selector_dexterity()
        self.add_selector_charisma()
        self.add_buttons()

    @property
    def _title_offset_x(self):
        """Title x position"""
        return self.window.screen_center_x - 300

    @property
    @abstractmethod
    def title(self):
        pass

    def add_selector_intelligence(self):
        self._add_selector(self.items, self.change_intelligence, "Intelligenz")

    def add_selector_dexterity(self):
        self._add_selector(self.items, self.change_dexterity, "Geschick")

    def add_selector_charisma(self):
        self._add_selector(self.items, self.change_charisma, "Charisma")

    def change_intelligence(self, selected, value):
        self.char.intelligence = value

    def change_dexterity(self, selected, value):
        self.char.dexterity = value

    def change_charisma(self, selected, value):
        self.char.charisma = value

    @property
    def items(self):
        """Selector items, which are values from 1 to 5 as a tuple, which contains the value as string as as int."""
        return [(str(i), i) for i in range(1, 6)]


class MenuAttributeSelectionP1(MenuAttributeSelection):
    """Menu for attribute selection for player 1."""

    def __init__(self, window: Window, char_menu_p2):
        self.char_menu_p2 = char_menu_p2
        super().__init__(window, public.p1_char)

    @property
    def title(self):
        return MenuTitles.ATTRIBUTES_P1

    @property
    def button_confirm_action(self):
        return self.char_menu_p2.menu


class MenuAttributeSelectionP2(MenuAttributeSelection):
    """Menu for attribute selection for player 1."""

    def __init__(self, window: Window):
        super().__init__(window, public.p2_char, has_confirm_button=False)

    @property
    def title(self):
        return MenuTitles.ATTRIBUTES_P2

    def start_game(self):
        """Start game action. Initializes game and closes menu"""
        game = Game1933(self.window, self.menu)
        self.menu.disable()
        self.menu.reset(1)
        game.start_scenario()

    def add_buttons(self):
        self.buttons.button_start_game(
            self.menu,
            self.start_game,  # action
        )
        self.buttons.button_back(self.menu)

    @property
    def button_confirm_action(self):
        return
