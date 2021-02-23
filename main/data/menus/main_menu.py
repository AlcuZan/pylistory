from data.menus.menus import BaseMenu
from data.menus.scenario_menu import ScenarioMenu
from data.paths import Backgrounds
from data.utils import Window, Background, MenuTitles


class MainMenu(BaseMenu):
    """Class for main menu."""

    def __init__(self, window: Window):
        super().__init__(window)

    @property
    def background(self):
        """Menu background"""
        return Background(self.window.screen, Backgrounds.MENU_BACKGROUND)

    @property
    def title(self):
        """Returns title"""
        return MenuTitles.GAME_TITLE

    def add_buttons(self):
        self.buttons.button_scenario_choice(self.menu, ScenarioMenu(self.window).menu)
        self.buttons.button_quit(self.menu)
