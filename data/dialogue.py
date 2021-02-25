""""Module that handles dialogue"""
from typing import List

import pygame

from config.config import TextBoxSettings
from data import utils
from data.textbox import TextBox, NarrationBox, BoxWithPortrait
from data.texts import TextForTextBox
from data.utils import Window, GameStates, Background


class DialogueHandler:
    def __init__(self, window: Window, game_map, dict_events: dict):
        self.window = window
        self.game_map = game_map
        self.dict_events = dict_events
        self.event = None
        self.name_event = None
        self.dict_speakers = None
        self.dict_texts = None
        self.speaker_index = 1
        self.lst_texts_s1 = None
        self.lst_texts_s2 = None
        self.text_index_s1 = 0
        self.text_index_s2 = 0
        self.lst_texts = None
        self.text_index = 0
        self.text = None
        self.speaker = None
        self.switch_speaker = True
        self.text_box = None
        self.state = GameStates
        self.narration = None

    def play_narrator_text(
        self, text: TextForTextBox or List[TextForTextBox], background=None
    ):
        if isinstance(text, TextForTextBox) and text.done:
            # Play nothing when text is done
            return
        if background is not None:
            bg = Background(self.window.screen, background)
            bg.draw()
        self.state = GameStates.NARRATION
        self.text_box = NarrationBox(window=self.window)
        text_to_draw: TextForTextBox = text
        text_is_list = False
        if isinstance(text, list):
            text_to_draw = text[self.text_index]
            text_is_list = True
        self.text_box.make_textbox(text_to_draw)

        while self.state.narration:
            pygame.display.update()
            if utils.continue_text():
                if not text_is_list:
                    # Only one text so go back
                    text.done = True
                    self.state = GameStates.DIALOGUE_DONE
                else:
                    # Space pressed so list +1
                    self.text_index += 1
                    if self.text_index <= len(text) - 1:
                        self.text_box.make_textbox(text[self.text_index])
                    else:
                        self.text_index = 0
                        self.state = GameStates.DIALOGUE_DONE

    def play_dialogue(self):
        self.text_box = BoxWithPortrait(self.window)
        self._set_speaker_and_texts()
        while self.state.dialogue:
            if utils.continue_text():
                # True per default
                if self.switch_speaker:
                    # Switching between speakers, only needed when text fits into one window, otherwise the speaker is
                    # the same
                    # Speaker 1 has spoken so speaker 2 is next and the text index of speaker 1 goes up 1
                    if self.speaker_index == 1:
                        self.speaker_index += 1
                        self.text_index_s1 += 1
                    elif self.speaker_index == 2:
                        self.speaker_index -= 1  # Go back to speaker 1
                        self.text_index_s2 += 1
                # More text so +1 on text index but same speaker
                else:
                    # Used text index isn't changed
                    if self.speaker_index == 1:
                        self.text_index_s1 += 1
                    else:
                        self.text_index_s2 += 1
                self._set_speaker_and_texts()
                # Is the text index in range of the list of texts? If not, the dialogue is done
                if self._more_text():
                    self._split_text()
                    self._make_textbox()
                else:
                    if self.narration is not None:
                        # TODO refactor
                        self.game_map.update(self.event)
                        self._reset_indices()
                        self.play_narrator_text(TextForTextBox(self.narration))
                        self._dialogue_done()
                    else:
                        self._dialogue_done()

            pygame.display.update()

    def _dialogue_done(self):
        """Handles what happens when a dialogue is done: remove the event, reset the indices, update display, change state"""
        del self.dict_events[self.name_event]
        self._reset_indices()
        pygame.display.update()
        self.state = GameStates.DIALOGUE_DONE

    def is_done(self):
        """Tells game if dialogue / narration is done"""
        if self.state.narration:
            return False
        elif self.state.dialogue:
            return False
        elif self.state.dialogue_done:
            return True

    def _more_text(self):
        """Check if there is more text to display"""
        if self.text_index <= len(self.lst_texts) - 1:
            return True
        return False

    def _split_text(self):
        """Splits up large texts if necessary. If it is, the speaker isn't switched. If it isn't, speaker is switched."""
        # 177 letters fit into the box, then the text needs to be split up
        if len(self.text) > TextBoxSettings.MAX_CHAR_DIALOGUE:
            # Delete the text that is too long, split it and reinsert the 2 parts
            self.lst_texts.pop(self.text_index)
            self.lst_texts.insert(
                self.text_index, self.text[: TextBoxSettings.MAX_CHAR_DIALOGUE]
            )
            self.lst_texts.insert(
                self.text_index + 1, self.text[TextBoxSettings.MAX_CHAR_DIALOGUE :]
            )
            self.switch_speaker = False
        else:  # There is no more text so switch speaker
            self.switch_speaker = True

    def _reset_indices(self):
        self.text_index = 0
        self.speaker_index = 1
        self.text_index_s1 = 0
        self.text_index_s2 = 0

    def _make_textbox(self):
        self.text = self.lst_texts[self.text_index]
        self.text_box.make_textbox(TextForTextBox(self.text, self.speaker))

    def _set_speaker_and_texts(self):
        """Sets the speaker and text, then shows it"""
        try:
            self.speaker = self.dict_speakers[f"speaker{self.speaker_index}"]
            self.lst_texts = self.dict_texts[
                self.dict_speakers[f"speaker{self.speaker_index}"]
            ]
            if self.speaker_index == 1:
                self.text_index = self.text_index_s1
            else:
                self.text_index = self.text_index_s2
            if self._more_text():
                self._make_textbox()
        except KeyError:
            self.state = GameStates.DIALOGUE_DONE
