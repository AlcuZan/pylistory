from data.buttons import Buttons
from data.menus.char_selection_menus import CharMenu1933P1
from data.menus.menus import BaseMenu
from data.utils import Window, MenuTitles


class ScenarioMenu(BaseMenu):
    def __init__(self, window: Window):
        super().__init__(window)

    @property
    def _title_offset_x(self):
        """Title x position"""
        return self.window.screen_center_x - 180

    @property
    def title(self):
        return MenuTitles.SCENARIOS

    def add_buttons(self):
        buttons = Buttons()
        # Not implemented
        # buttons.button_start_1914_scenario(menu=self.menu, action=events.NONE)
        buttons.button_start_1933_scenario(self.menu, CharMenu1933P1(self.window).menu)
        # Not implemented
        # buttons.button_start_1949_scenario(self.menu, events.NONE)  # not implemented
        buttons.button_back(self.menu)
