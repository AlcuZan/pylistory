from enum import Enum
from typing import Optional

import pygame

from config.config import TextBoxSettings, Colors
from data import ptext as ptext
from data.paths import Backgrounds, Portraits, Paths
from data.texts import TextForTextBox
from data.utils import Window, load_img, flip_horizontal, scale_up_double


class TextBox:
    """Class for text boxes"""

    # TODO not to be instantiated

    def __init__(
        self,
        window: Window = None,  # TODO refactor because we either need only window or surf
        surf: pygame.Surface = None,
        box_y_pos=None,  # For positioning
        text_offset_left=None,
        text_offset_top=None,
        box_size=None,
        text_width=None,
        make_bigger=False,
        box_pos=None,
    ):
        self.window = window
        self.surf = surf
        self.background = load_img(Backgrounds.BACKGROUND_TEXTBOX)
        self.text_offset_left = text_offset_left
        self.text_offset_top = text_offset_top
        self.text_width = text_width
        if make_bigger:
            self.background = pygame.transform.scale(self.background, box_size)
        if box_y_pos is not None:
            self.rect = self.background.get_rect(centery=box_y_pos)
        elif box_pos is not None:
            self.rect = self.background.get_rect(center=box_pos)
        else:
            # Box appears in the top middle of the screen
            self.rect = self.background.get_rect(centerx=self.window.screen_center_x)
        # This will hold the complete image that gets printed to the screen. The image contains the background and text
        # and char portrait if available
        self.image: pygame.Surface = Optional[None]
        self.img_char_speaking = None

    def make_textbox(self, text_item: dict or str or list, update_display=False):
        """Creates background image, puts the text onto it using ptext and executes drawing"""
        # textbox_width is the width of the text itself, not the width of the box
        # TODO undurchsichtig, es sollte *immer* TextForTextBox genutzt werden
        if isinstance(text_item, str):
            text_item = TextForTextBox(text_item)
        elif isinstance(text_item, dict):
            text_item = TextForTextBox(text_item["text"], text_item["speaker"])
        elif isinstance(text_item, TextForTextBox):
            if isinstance(text_item.speaker, Enum):
                text_item.speaker = text_item.speaker.value
        # This is the "base" surface where the background image, char portrait and text are being drawn onto
        image = pygame.Surface(self.rect.size)
        # Enables transparency
        image.set_colorkey(Colors.BLACK)
        # Draws the background image
        image.blit(self.background, (0, 0))
        # Reset portrait
        self.img_char_speaking = None
        if not isinstance(text_item, list):
            for portrait in Portraits:
                # TODO maybe to the loading stuff somewhere else
                # Determines which char is speaking (in case it's not the narrator) and loads the corresponding image
                # upper() is needed because Portraits contains Enums which are all written in capital letters
                if text_item.speaker is not None and (
                    text_item.speaker.upper() == portrait.name
                    or text_item.speaker == portrait.name
                ):
                    self.img_char_speaking = load_img(portrait.value.path)
                    # Some portraits need flipping and scaling TODO that kinda sucks
                    if portrait.value.modify:
                        self.img_char_speaking = flip_horizontal(self.img_char_speaking)
                        self.img_char_speaking = scale_up_double(self.img_char_speaking)

            # Draws the text
            self._draw_text(text_item.text, self.text_width, image)

            if self.img_char_speaking is not None:
                # Draw char portrait
                image.blit(
                    self.img_char_speaking,
                    (
                        TextBoxSettings.OFFSET_CHAR_PORTRAIT_X,
                        TextBoxSettings.OFFSET_CHAR_PORTRAIT_Y,
                    ),
                )
        else:
            text_item = [f"{text}\n" for text in text_item]
            text = "".join(text_item)
            self._draw_text(text, self.text_width, image)
        self._draw(image)
        if update_display:
            # TODO refactor, nur an manchen stellen nicht gewollt zb wenn elias flieht
            pygame.display.update()

    def _draw_text(self, text, textbox_width, image):
        ptext.draw(
            text,
            (self.text_offset_left, self.text_offset_top),
            color=Colors.NEAR_BLACK,
            fontname=Paths.DEFAULT_FONT,
            fontsize=TextBoxSettings.FONT_SIZE,
            width=textbox_width,
            surf=image,
        )

    def _draw(self, image):
        """Draws the whole image including the text"""

        def draw(surf):
            surf.blit(image, self.rect)

        if self.window is not None:
            draw(self.window.screen)
        else:
            draw(self.surf)


class BoxWithPortrait(TextBox):
    def __init__(self, window, box_pos=None, box_y_pos=None):
        super().__init__(
            window=window,
            text_offset_left=TextBoxSettings.DIALOGUE_TEXT_OFFSET_LEFT,
            text_offset_top=TextBoxSettings.DIALOGUE_TEXT_OFFSET_TOP,
            box_pos=box_pos,
            box_y_pos=box_y_pos,
            text_width=TextBoxSettings.DIALOGUE_TEXT_WIDTH,
        )


class NarrationBox(TextBox):
    def __init__(self, window):
        super().__init__(
            window=window,
            box_size=TextBoxSettings.NARRATION_BOX_SIZE,
            make_bigger=True,
            text_width=TextBoxSettings.NARRATION_TEXT_WIDTH,
            text_offset_left=TextBoxSettings.NARRATION_TEXT_OFFSET_LEFT,
            text_offset_top=TextBoxSettings.NARRATION_TEXT_OFFSET_TOP,
        )


class ItemListBox(TextBox):
    def __init__(self, window):
        box_y_pos = window.screen_center_y + TextBoxSettings.ITEMS_LIST_BOX_OFFSET_LEFT
        super().__init__(
            window=window,
            box_size=TextBoxSettings.ITEMS_LIST_BOX_SIZE,
            make_bigger=True,
            text_offset_left=TextBoxSettings.ITEMS_LIST_TEXT_OFFSET_LEFT,
            text_offset_top=TextBoxSettings.ITEMS_LIST_TEXT_OFFSET_TOP,
            box_y_pos=box_y_pos,
        )


class UniformDescriptionBox(TextBox):
    def __init__(self, window):
        box_y_pos = (
            window.screen_center_y + TextBoxSettings.UNIFORM_DESCRIPTION_BOX_OFFSET_LEFT
        )
        super().__init__(
            window=window,
            box_size=TextBoxSettings.UNIFORM_DESCRIPTION_BOX_SIZE,
            make_bigger=True,
            box_y_pos=box_y_pos,
            text_offset_top=TextBoxSettings.UNIFORM_DESCRIPTION_TEXT_OFFSET_TOP,
            text_offset_left=TextBoxSettings.UNIFORM_DESCRIPTION_TEXT_OFFSET_LEFT,
            text_width=TextBoxSettings.UNIFORM_DESCRIPTION_TEXT_WIDTH,
        )
