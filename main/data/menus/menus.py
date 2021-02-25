"""Module for main menu"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from pygame_menu import events, themes
from pygame_menu.menu import Menu
from pygame_menu.widgets import Selector, Button

from data import utils
from config.config import Settings, ThemeSettings
from data.paths import Sound
from data.utils import (
    Window,
)
from data.buttons import Buttons


class BaseMenu(ABC):
    """Abstract menu class, not supposed to be instantiated directly."""

    def __init__(self, window: Window, only_buttons: bool = True):
        """Basic init to create a menu."""
        self.window = window
        if not Settings.MUTE:
            utils.set_music(Sound.MENU_MUSIC, Settings.MENU_VOLUME)
        self._selector_widget: Optional[Selector] = None
        self.menu = self.create_menu()
        self.buttons = Buttons()
        if only_buttons:
            self.add_buttons()

    @property
    def _theme(self):
        """Sets theme"""
        theme = themes.THEME_DARK.copy()
        theme.set_background_color_opacity(
            ThemeSettings.OPACITY
        )  # Makes menu a little transparent
        theme.title_font = ThemeSettings.FONT
        theme.title_font_color = ThemeSettings.FONT_COLOR
        theme.title_bar_style = ThemeSettings.MENUBAR  # No menu bar

        theme.widget_font = ThemeSettings.FONT
        theme.widget_offset = (self._widget_offset_x, 0)
        # theme.title_font_size = 100  # Title size
        # Center title
        theme.title_offset = self._theme_title_offset
        theme.menubar_close_button = False  # Removes close button

        return theme

    @property
    def _theme_title_offset(self):
        return (
            self._title_offset_x,
            self._title_offset_y,
        )

    @property
    def _title_offset_x(self):
        return self.window.screen_center_x - 70

    @property
    def _title_offset_y(self):
        return self.window.screen_center_y - 200

    @property
    def _widget_offset_x(self):
        return 0

    @property
    @abstractmethod
    def title(self):
        """Title of the menu. Must be set in subclass."""
        pass

    @abstractmethod
    def add_buttons(self):
        pass

    def create_menu(self, title=None, onclose: bool = False) -> Menu:
        """Creates the menu with all needed parameters."""
        # Disables X button to close the game if True
        onclose = events.DISABLE_CLOSE if not onclose else events.CLOSE
        title = title if title is not None else self.title

        return Menu(
            height=self.window.size.value[1],  # Menu is as big as the window
            width=self.window.size.value[0],
            title=title,
            theme=self._theme,
            onclose=onclose,
        )

    def _add_selector(self, items: List[Tuple], onchange: callable, title: str = None):
        """Adds Selector to the menu."""
        title = (
            "" if title is None else title.ljust(15)
        )  # Adds vertical space after the title
        return self.menu.add_selector(
            title=title,
            items=items,
            onchange=onchange,
        )

    def add_button_confirm(self, action):
        return self.buttons.button_confirm(self.menu, action)

    def remove_content(self):
        """Removes all widgets."""
        for widget in self.menu.get_widgets():
            self.menu.remove_widget(widget)


class SubMenu(BaseMenu):
    """Class for submenus that contain selectors."""

    def __init__(self, window, has_confirm_button: bool = True):
        super().__init__(window, only_buttons=False)
        self.has_confirm_button = has_confirm_button
        self.button_confirm: Optional[Button] = None

    def _add_submenu_buttons(self):
        if self.has_confirm_button:
            self.button_confirm = self.add_button_confirm(self.button_confirm_action)
        self.buttons.button_back(self.menu)

    def add_buttons(self):
        self._add_submenu_buttons()

    @property
    @abstractmethod
    def button_confirm_action(self):
        pass
