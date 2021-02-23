from abc import abstractmethod
from typing import Optional

import pygame_menu
from pygame_menu.widgets import Image, Label, Button

from data import public
from config.config import Colors, Settings
from data.menus.menus import SubMenu
from data.menus.attribute_menus import (
    MenuAttributeSelectionP1,
    MenuAttributeSelectionP2,
)
from data.game1933 import Game1933
from data.player import Characters
from data.utils import Window, CharName, MenuTitles


class CharMenu1933(SubMenu):
    """Base class for character menus."""

    def __init__(self, window: Window, has_confirm_button=True):
        super().__init__(window, has_confirm_button)
        self._image_widget: Optional[Image] = None
        self._backstory_widget: Optional[Label] = None
        self.button_confirm: Optional[Button] = None
        self.warn_same_chars: Optional[Label] = None
        self._other_backstory = None
        self.menu_backstory = self.add_backstory_menu()

    @property
    @abstractmethod
    def title(self):
        """Title of the menu. Must be set in subclass."""
        pass

    @property
    def _title_offset_x(self):
        return self.window.screen_center_x - 120

    def _on_selector_change(self, selected: tuple, value: str):
        """Method executed when selector changes."""
        self._update_from_selection(value)

    @abstractmethod
    def _update_from_selection(self, index):
        pass

    @staticmethod
    def selector_modes() -> dict:
        return {1: Characters.ELIAS.selector_mode, 2: Characters.KLAUS.selector_mode}

    @property
    def standard_selector_items(self):
        return [(Characters.ELIAS.name.value, 1), (Characters.KLAUS.name.value, 2)]

    def selector_items(self):
        return self.standard_selector_items

    def check_same_chars(self):
        """Checks if both players have chosen the same character. If they do, confirm button is removed and a warning
        is added. If they don't, nothing happens.
        """
        if public.p2_char is not None and public.p1_char.name == public.p2_char.name:
            self.button_confirm.hide()
            self.warn_same_chars.show()
        else:
            self.button_confirm.show()
            self.warn_same_chars.hide()

    @staticmethod
    def warning_message(char: Optional[CharName] = None) -> Label:
        return Label(f"Spieler 1 hat bereits {char.value} ausgewählt!", "warn_p1")

    def _add_warn_same_chars(self, char: CharName):
        """Adds a warning to the menu that only appears if both players selected the same characters."""
        self.warn_same_chars = self.menu.add_label(
            self.warning_message(char).get_title(),
            self.warning_message(char).get_id(),
            font_color=Colors.RED,
        )

    def _update_img_and_txt(self, index):
        # Changes the image according to selected item
        self._image_widget.set_image(self.selector_modes()[index]["image"])
        # TODO fix this, Klaus backstory still shows when switching back to Elias
        # Changes the backstory according to selected item
        # if isinstance(self._backstory_widget, list):
        #     for w in self._backstory_widget:
        #         w.set_title(self.selector_modes()[index]["backstory"])
        # else:
        #     self._backstory_widget.set_title(self.selector_modes()[index]["backstory"])

        changed = False
        if index == 2 and self._other_backstory is not None:
            for label in self._backstory_widget:
                label.hide()
            for label in self._other_backstory:
                label.show()
            changed = True
        if changed and index == 1:
            for label in self._backstory_widget:
                label.show()
            for label in self._other_backstory:
                label.hide()

    def add_backstory_menu(self):
        theme = self._theme
        theme.menubar_close_button = True
        # TODO duplicate code
        return pygame_menu.Menu(
            height=self.window.size.value[1],  # Menu is as big as the window
            width=self.window.size.value[0],
            title="",
            theme=theme,
        )


class CharMenu1933P1(CharMenu1933):
    """Menu for character selection for player 1."""

    def __init__(self, window: Window):
        super().__init__(window)
        self.char_menu_p2 = CharMenu1933P2(self.window)
        self._image_widget = self.menu.add_image(
            image_path=self.selector_modes()[1]["image"]
        )
        # Backstory in backstory submenu
        self._backstory_widget = self.menu_backstory.add_label(
            self.selector_modes()[1]["backstory"], max_char=80
        )
        # TODO switching the backstory doesnt work
        if Settings.SELECTABLE_CHARS:
            self._backstory_widget = self.menu_backstory.add_label(
                self.selector_modes()[1]["backstory"], max_char=80
            )
            self._other_backstory = self.menu_backstory.add_label(
                self.selector_modes()[2]["backstory"], max_char=80
            )
            for label in self._other_backstory:
                label.hide()
                # Char selector
                self._selector_widget = self._add_selector(
                    onchange=self._on_selector_change, items=self.selector_items()
                )
        # self._backstory_widget = self.menu.add_label(
        #     title=self.selector_modes()[1]["backstory"]
        # )
        self.menu.add_button("Hintergrundgeschichte", self.menu_backstory)
        self.add_buttons()
        if Settings.SELECTABLE_CHARS:
            # Shows default char
            self._update_from_selection(self._selector_widget.get_value()[0][1])

    @property
    def title(self):
        return MenuTitles.CHARACTER_SELECTION_PLAYER_ONE

    @property
    def button_confirm_action(self):
        if Settings.ATTRIBUTES_ENABLED:
            return MenuAttributeSelectionP1(self.window, self.char_menu_p2).menu
        return self.char_menu_p2.menu

    def _update_from_selection(self, index):
        """Changes widgets depending on index"""
        self._update_img_and_txt(index)
        # Sets character
        # TODO button doesnt know that player changes
        public.p1_char = self.selector_modes()[index]["char"]

        if not self.char_menu_p2.menu.get_widgets():
            self.char_menu_p2.add_content()
        else:
            self.char_menu_p2.remove_content()
            self.char_menu_p2.add_content()


class CharMenu1933P2(CharMenu1933):
    """Menu for character selection for player 2."""

    def __init__(
        self,
        window: Window,
    ):
        super().__init__(window)
        self._image_widget = None
        self._backstory_widget = None
        if not Settings.SELECTABLE_CHARS:
            self._image_widget = self.menu.add_image(
                image_path=self.selector_modes()[2]["image"]
            )
        # Backstory in backstory submenu
        self._backstory_widget = self.menu_backstory.add_label(
            self.selector_modes()[2]["backstory"], max_char=80
        )
        self.menu.add_button("Hintergrundgeschichte", self.menu_backstory)
        self.add_buttons()

    @property
    def title(self):
        return MenuTitles.CHARACTER_SELECTION_PLAYER_TWO

    def add_content(self):
        """Adds content to the menu. Called after player one has chosen his character (if choosing characters is enabled)."""
        self._image_widget = self.menu.add_image(
            image_path=self.selector_modes()[1]["image"]
        )
        self._backstory_widget = self.menu.add_label(
            title=self.selector_modes()[1]["backstory"]
        )
        self._selector_widget = self._add_selector(
            self.selector_items(), self._on_selector_change
        )
        self.add_buttons()
        self._add_warn_same_chars(public.p1_char.name)
        self._update_from_selection(self._selector_widget.get_value()[0][1])

    def start_game(self):
        """Initializes game and closes menu"""
        game = Game1933(self.window, self.menu)
        self.menu.disable()
        self.menu.reset(1)
        game.start_scenario()

    @property
    def button_confirm_action(self):
        """Determines what happens when you press the confirm button"""
        if Settings.ATTRIBUTES_ENABLED:
            return MenuAttributeSelectionP2(self.window).menu
        else:
            return self.start_game

    def selector_items(self):
        """Selector items change (or don't change) according to the character player one has chosen."""
        items = self.standard_selector_items
        if public.p1_char.name.klaus:
            return items
        if public.p1_char.name.elias:
            items[0], items[1] = items[1], items[0]
            return items

    def _update_from_selection(self, index):
        """Changes widgets depending on index and adds warn message if needed"""
        self._update_img_and_txt(index)
        public.p2_char = self.selector_modes()[index]["char"]
        self.check_same_chars()
