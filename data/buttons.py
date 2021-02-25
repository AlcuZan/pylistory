"""Module for buttons"""
from enum import Enum
from typing import NamedTuple

from pygame_menu.events import MenuAction
from pygame_menu import events, Menu


class ButtonTextEntry(NamedTuple):  # TODO maybe obsolete
    text: str
    button_id: str


class ButtonTexts(Enum):
    SCENARIO_CHOICE = ButtonTextEntry("Start", "start")
    OPTIONS = ButtonTextEntry("Optionen", "options")
    BACK = ButtonTextEntry("Zurück", "back")
    CONFIRM = ButtonTextEntry("Bestätigen", "confirm")
    QUIT = ButtonTextEntry("Beenden", "quit")
    START = ButtonTextEntry("Spiel starten", "start_game")
    SCENARIO_1933 = ButtonTextEntry("1933 (Machtergreifung)", "scenario_1933")
    SCENARIO_1949 = ButtonTextEntry("1949 (Gründung der DDR)", "scenario_1949")
    SCENARIO_1914 = ButtonTextEntry("1914 (Ausbruch 1. Weltkrieg)", "scenario_1914")


class Buttons:
    """Class for all buttons"""

    @staticmethod
    def add_button(
        button_text: ButtonTexts, action: Menu or MenuAction or callable, menu: Menu
    ):
        """Adds given button to given menu.
        Args:
            button_text:
                Contains text and ID for the button
            action:
                Determines what happens when button is pressed (like opening a new menu, closing the window etc)
            menu:
                Menu that the button is part of
        """
        # noinspection PyTypeChecker
        return menu.add_button(
            button_text.value.text, action, button_id=button_text.value.button_id
        )

    def button_back(self, menu):
        return self.add_button(
            ButtonTexts.BACK,
            events.BACK,
            menu,
        )

    def button_quit(self, menu):
        return self.add_button(
            ButtonTexts.QUIT,
            events.EXIT,
            menu,
        )

    def button_confirm(self, menu, action):
        """Creates confirm button with given action (usually opening a new menu)."""
        return self.add_button(
            ButtonTexts.CONFIRM,
            action,
            menu,
        )

    def button_scenario_choice(self, menu, action):
        return self.add_button(
            ButtonTexts.SCENARIO_CHOICE,
            action,
            menu,
        )

    def button_options(self, menu, action):
        return self.add_button(
            ButtonTexts.OPTIONS,
            action,
            menu,
        )

    def button_start_1933_scenario(self, menu, action):
        return self.add_button(
            ButtonTexts.SCENARIO_1933,
            action,
            menu,
        )

    def button_start_1914_scenario(self, menu, action):
        return self.add_button(
            ButtonTexts.SCENARIO_1914,
            action,
            menu,
        )

    def button_start_1949_scenario(self, menu, action):
        return self.add_button(
            ButtonTexts.SCENARIO_1949,
            action,
            menu,
        )

    def button_start_game(self, menu, action):
        return self.add_button(
            ButtonTexts.START,
            action,
            menu,
        )
