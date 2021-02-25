"""Module for quiz (last major event)"""
from enum import Enum, auto

import pygame
import thorpy
from thorpy import Box

from config.config import TextBoxSettings, Colors, Misc, QuizSettings
from data import utils
from data.paths import Backgrounds
from data.textbox import BoxWithPortrait
from data.texts import Questions, TextForTextBox, Dialogues, NarrationTexts
from data.utils import Window, load_img, Background


class QuestionStates(Enum):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
    FOURTH = auto()
    FIFTH = auto()

    @property
    def first(self):
        return self == self.FIRST

    @property
    def second(self):
        return self == self.SECOND

    @property
    def third(self):
        return self == self.THIRD

    @property
    def fourth(self):
        return self == self.FOURTH

    @property
    def fifth(self):
        return self == self.FIFTH


class Quiz:
    def __init__(self, window: Window, center):
        # Todo no hardcoding
        self.window = window
        self.center = center
        # Loads background image for box
        self.box_bg = load_img(Backgrounds.BACKGROUND_TEXTBOX)
        self.background = Background(self.window.screen, Backgrounds.QUIZ_BG)
        self.question_box: Box = None
        self.dialogue_box = BoxWithPortrait(window=window, box_pos=window.screen_center)
        self.chances = 2
        self.quiz_over = False
        self.quiz_failed = False
        self._first_question()

    @staticmethod
    def _update_and_wait(wait_time=QuizSettings.WAIT_TIME):
        pygame.display.update()
        pygame.time.wait(wait_time)  # ms

    def _decide_next_question(self):
        if self.question_state.first:
            self._second_question()
        elif self.question_state.second:
            self._third_question()
        elif self.question_state.third:
            self._fourth_question()
        elif self.question_state.fourth:
            self._fifth_question()
        elif self.question_state.fifth:
            self.menu.leave = True

    def _correct_answer(self):
        """If the answer is correct, Kreuzer acknowledges it and the next question appears"""
        if self.question_state.fifth:
            text = Dialogues.KREUZER_CORRECT_CHOICE_LAST
            wait_time = QuizSettings.WAIT_TIME_LONGER
        else:
            text = Dialogues.KREUZER_CORRECT_CHOICE_DEFAULT
            wait_time = QuizSettings.WAIT_TIME
        self.dialogue_box.make_textbox(text, True)
        self._update_and_wait(wait_time)
        if self.question_state.fifth:
            self.background.draw()
            self._play_last_dialogue()
        self._decide_next_question()

    def _wrong_answer(self):
        """This happens if the player answers incorrectly. Player gets one more chance, then it's game over."""
        self.chances -= 1
        if self.chances > 0:
            text = (
                Dialogues.KREUZER_WRONG_CHOICE_LAST
                if self.question_state.fifth
                else Dialogues.KREUZER_WRONG_CHOICE_DEFAULT
            )
        else:
            text = Dialogues.KREUZER_TOO_MANY_WRONG_CHOICES
            self.quiz_over = True
        self.dialogue_box.make_textbox(text)
        self._update_and_wait()
        while self.quiz_over:
            self.menu.leave = True
            self.quiz_failed = True
            self.window.screen.fill(Colors.BLACK)
            self.dialogue_box.make_textbox(NarrationTexts.QUIZ_FAILED, True)
            if utils.continue_text():
                self.quiz_over = False
                return
        self._decide_next_question()

    def _button_wrong_answer(self, text):
        return thorpy.make_button(text, func=self._wrong_answer)

    def _button_correct_answer(self, text):
        return thorpy.make_button(text, func=self._correct_answer)

    @staticmethod
    def _make_question(text):
        return thorpy.make_text(text, font_size=TextBoxSettings.FONT_SIZE)

    def _first_question(self):
        self.question_state = QuestionStates.FIRST
        self.question = self._make_question(Questions.FIRST)
        self.button1 = self._button_wrong_answer("1) 10.01.1933")
        self.button2 = self._button_correct_answer("2) 30.01.1933")
        self.button3 = self._button_wrong_answer("3) 04.02.1934")
        self._set_quiz_box()

    def _second_question(self):
        self.question_state = QuestionStates.SECOND
        self.question = self._make_question(Questions.SECOND)
        self.button1 = self._button_wrong_answer(
            "1) Die Verordnung zum Schutz von Volk und Staat"
        )
        self.button2 = self._button_wrong_answer("2) Der Uniformswechsel der Wehrmacht")
        self.button3 = self._button_correct_answer(
            "3) Die geplante Ernennung Hitlers zum Reichskanzler"
        )
        self._set_quiz_box()

    def _third_question(self):
        self.question_state = QuestionStates.THIRD
        self.question = self._make_question(Questions.THIRD)
        self.button1 = self._button_correct_answer(
            "1) 28.02.1933, Einschränkung der Meinungs-, Presse- und Versammlungsfreiheit"
        )
        self.button2 = self._button_wrong_answer(
            "2) 21.04.1933, Ernennung Hitlers zum Reichskanzler"
        )
        self.button3 = self._button_wrong_answer(
            "3) 01.01.1933, Erlaubnis, jeden Juden bei Verdacht in Schutzhaft nehmen zu dürfen"
        )
        self._set_quiz_box()

    def _fourth_question(self):
        self.question_state = QuestionStates.FOURTH
        self.question = self._make_question(Questions.FOURTH)
        self.button1 = self._button_wrong_answer(
            "1) Kann an beiden Armen getragen werden"
        )
        self.button2 = self._button_wrong_answer("2) Am rechten Arm")
        self.button3 = self._button_correct_answer("3) Am linken Arm")
        self._set_quiz_box()

    def _fifth_question(self):
        self.question_state = QuestionStates.FIFTH
        self.question = self._make_question(Questions.FIFTH)
        self.button1 = self._button_correct_answer("1) Scharführer")
        self.button2 = self._button_wrong_answer("2) Reichskanzler")
        self.button3 = self._button_wrong_answer("3) Reichspropagandaleiter")
        self._set_quiz_box()

    def _set_quiz_box(self):
        self.background.draw()
        self.lst_elements = [self.question, self.button1, self.button2, self.button3]
        for button in self.lst_elements:
            # Make buttons bigger (width x2, height stays as it is)
            size = button.get_size()
            button.set_size((size[0] * 2, size[1] + 10))
            button.set_font_size(TextBoxSettings.FONT_SIZE)
            button.set_main_color(Colors.TEXTBOX)
        self.question_box = thorpy.Box(elements=self.lst_elements)
        # Sets position
        self.question_box.set_center(self.center)
        self.question_box.move((-100, 100))
        size = self.question_box.get_size()
        self.question_box.set_size((size[0] + 200, size[1] + 100))
        # Scale background image to self.box size
        img = pygame.transform.scale(self.box_bg, self.question_box.get_size())
        self.question_box.set_image(img)
        # Centers elements
        thorpy.store(frame=self.question_box.get_rect(), elements=self.lst_elements)
        self.question_box.blit()
        self.menu = thorpy.Menu(self.question_box)
        for element in self.menu.get_population():
            element.surface = self.window.screen

    def _play_last_dialogue(self):
        while True:
            self.dialogue_box.make_textbox(Dialogues.KLAUS_LAST_DIALOGUE, True)
            if utils.continue_text():
                break
        while True:
            self.dialogue_box.make_textbox(Dialogues.ELIAS_LAST_DIALOGUE, True)
            if utils.continue_text():
                break
