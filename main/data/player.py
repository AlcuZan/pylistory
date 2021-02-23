"""Player module"""
from dataclasses import dataclass
from enum import Enum, auto
import time
from typing import Optional

import pygame
from pygame import K_UP, K_w, K_DOWN, K_s, K_LEFT, K_a, K_RIGHT, K_d, KEYDOWN, KEYUP
import pygame_menu

from data import utils
from data.textbox import TextBox, BoxWithPortrait
from data.texts import Backstories, Dialogues
from data.utils import (
    CharName,
    MenuPortraits,
    Borders,
    scale_up_double,
    draw_hit_box,
    Window,
)

from config.config import Settings
from data.paths import MapAssets
from data.sprite_sheet import SpriteSheet


@dataclass
class Character:
    name: CharName
    portrait: pygame_menu.baseimage.BaseImage
    _char_image_names: Optional[dict]
    backstory_txt: str
    # Attributes
    intelligence: int = 1
    dexterity: int = 1
    charisma: int = 1

    @property
    def selector_mode(self) -> dict:
        return {"char": self, "image": self.portrait, "backstory": self.backstory_txt}

    @property
    def sprite_sheet(self):
        return SpriteSheet(MapAssets.SPRITE_SHEET)

    def get_frames(self, category):
        lst_sprites = []
        for name in self._char_image_names[category]:
            lst_sprites.append(self.sprite_sheet.parse_sprite(name))
        return lst_sprites

    @property
    def walking_frames_right(self):
        return self.get_frames("facing_right")

    @property
    def walking_frames_left(self):
        return self.get_frames("facing_left")

    @property
    def walking_frames_up(self):
        return self.get_frames("facing_up")

    @property
    def walking_frames_down(self):
        return self.get_frames("facing_down")


def get_sprite_names(numbers: list):
    return [f"sprite{num}" for num in numbers]


class Characters:

    ELIAS = Character(
        CharName.ELIAS,
        MenuPortraits.ELIAS,
        {
            "facing_up": get_sprite_names([26, 53, 80]),
            "facing_down": get_sprite_names([25, 52, 79]),
            "facing_left": get_sprite_names([24, 51, 78]),
            "facing_right": get_sprite_names([27, 54, 81]),
        },
        Backstories.ELIAS,
    )
    KLAUS = Character(
        CharName.KLAUS,
        MenuPortraits.KLAUS,
        {
            "facing_up": get_sprite_names([350, 377, 397]),
            "facing_down": get_sprite_names([349, 376, 396]),
            "facing_left": get_sprite_names([348, 375, 395]),
            "facing_right": get_sprite_names([351, 378, 398]),
        },
        Backstories.KLAUS,
    )


class States(Enum):
    IDLE = "idle"
    MOVING_RIGHT = auto()
    MOVING_LEFT = auto()
    MOVING_UP = auto()
    MOVING_DOWN = auto()

    @property
    def moving_right(self):
        return self == self.MOVING_RIGHT

    @property
    def moving_left(self):
        return self == self.MOVING_LEFT

    @property
    def moving_up(self):
        return self == self.MOVING_UP

    @property
    def moving_down(self):
        return self == self.MOVING_DOWN


class Keys:
    """Class for keyboard keys"""

    def __init__(self, p_num: int):
        self._p_num = p_num
        self.left = self.get_left()
        self.right = self.get_right()
        self.up = self.get_up()
        self.down = self.get_down()

    def get_left(self):
        return {1: K_LEFT, 2: K_a}.get(self._p_num)

    def get_right(self):
        return {1: K_RIGHT, 2: K_d}.get(self._p_num)

    def get_up(self):
        return {1: K_UP, 2: K_w}.get(self._p_num)

    def get_down(self):
        return {1: K_DOWN, 2: K_s}.get(self._p_num)


class Player(pygame.sprite.Sprite):
    """Player class"""

    def __init__(
        self,
        char: Character = None,
        window: Window = None,
        keys: Keys = None,
        pos_x=None,
        pos_y=None,
    ):
        super().__init__()
        # Information about the character that was chosen by the player
        self.char = char
        self.window = window
        self.pos_x = pos_x
        self.pos_y = pos_y
        # The first image that we blit is the character facing down and standing still
        self.current_image: pygame.Surface = self.char.walking_frames_down[0]
        if Settings.DOUBLE_SCALE:
            self.current_image: pygame.Surface = scale_up_double(
                self.char.walking_frames_down[0]
            )
        # Gets rect from first image
        self.rect = self.current_image.get_rect()
        # Spawn position
        self.rect.midbottom = (pos_x, pos_y)
        # Screen borders
        self.borders = Borders(self.window.screen, self.rect)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.state = States.IDLE
        self.LEFT_KEY_PRESSED = False
        self.RIGHT_KEY_PRESSED = False
        self.UP_KEY_PRESSED = False
        self.DOWN_KEY_PRESSED = False
        self.keys = keys
        self.prev_time = time.time()
        self.dt = 0
        self.can_move = True
        # This box has another position than the standard dialogue box
        self.text_box = BoxWithPortrait(window=window, box_y_pos=window.screen_center_y)

    # TODO make controls variable (e.g. via settings)

    def update(self, game_map):
        """Updates the player image depending on the input, which determines the direction he is facing,
         which will determine the direction he is moving and the sprites that need to be used to visualize
        that direction."""
        # Resets velocity
        self.velocity_y = 0
        self.velocity_x = 0
        # Changes velocities according to which key is pressed, for example the right key press increases the velocity
        # in horizontal direction. Also checks for borders, so the velocity will not change if a border is reached.
        if self.can_move:
            if self.rect.left > self.borders.left and self.LEFT_KEY_PRESSED:
                self.velocity_x = -Settings.PLAYER_VEL
            elif self.rect.right < self.borders.right and self.RIGHT_KEY_PRESSED:
                self.velocity_x = Settings.PLAYER_VEL
            elif self.rect.top > self.borders.top and self.UP_KEY_PRESSED:
                self.velocity_y = -Settings.PLAYER_VEL
            elif self.rect.bottom < self.borders.bottom and self.DOWN_KEY_PRESSED:
                self.velocity_y = Settings.PLAYER_VEL

        self._set_state()
        self._animate()
        self._check_collision_and_move(
            game_map.tile_renderer.lst_obstacles,
            game_map.tile_renderer.lst_elias_escape_events,
        )

    def reset(self):
        """Resets velocities, state and sets all key presses to False"""
        self.velocity_x = 0
        self.velocity_y = 0
        self._set_state()
        self.LEFT_KEY_PRESSED = False
        self.RIGHT_KEY_PRESSED = False
        self.UP_KEY_PRESSED = False
        self.DOWN_KEY_PRESSED = False

    def _check_collision_and_move(self, lst_obstacles, lst_elias_escape_events):
        """Moves the player while checking for collisions. First moving is executed and if a collision is detected
        the position is reset.
        """
        # Makes game frame rate independent
        # Reference: https://github.com/ChristianD37/YoutubeTutorials/blob/master/Framerate%20Independence/demo.py
        self.now = time.time()
        self.dt = self.now - self.prev_time
        self.prev_time = self.now
        self._move_horizontal()
        self._move_vertical()
        # If a collision is detected, the position of the player is reset to the opposite border
        # For example the player moves right and collides with an object on his right side, then his right position is
        # reset to the left position of the object, so he cannot proceed
        for obstacle in lst_obstacles:
            collision = self.rect.colliderect(obstacle.rect)
            if Settings.DRAW_HIT_BOXES:
                draw_hit_box(self.window.screen, obstacle)
            if self.state.moving_right:
                # There is an obstacle, that the player rect connects with
                if collision:
                    self.rect.right = obstacle.rect.left
            if self.state.moving_left:
                if collision:
                    self.rect.left = obstacle.rect.right
            if self.state.moving_up:
                if collision:
                    self.rect.top = obstacle.rect.bottom
            if self.state.moving_down:
                if collision:
                    self.rect.bottom = obstacle.rect.top
        klaus = self.char.name.klaus
        elias = self.char.name.elias
        for event in lst_elias_escape_events:
            # todo duplicate code
            collision = self.rect.colliderect(event.rect)
            if collision:
                if elias:
                    self.textbox_elias_cant_proceed()
                if klaus:
                    self.textbox_klaus_cant_proceed()
            if self.state.moving_right:
                # There is an obstacle, that the player rect connects with
                if collision:
                    self.rect.right = event.rect.left
            if self.state.moving_left:
                if collision:
                    self.rect.left = event.rect.right
            if self.state.moving_up:
                if collision:
                    self.rect.top = event.rect.bottom
            if self.state.moving_down:
                if collision:
                    self.rect.bottom = event.rect.top

    def textbox_elias_cant_proceed(self):
        self.text_box.make_textbox(Dialogues.ELIAS_CANT_PROCEED)

    def textbox_klaus_cant_proceed(self):
        self.text_box.make_textbox(Dialogues.KLAUS_CANT_PROCEED)

    def _frame_rate_independent_vel(self, vel):
        return vel * self.dt * Settings.TARGET_FPS

    def _move_horizontal(self):
        self.rect.x += self._frame_rate_independent_vel(self.velocity_x)

    def _move_vertical(self):
        self.rect.y += self._frame_rate_independent_vel(self.velocity_y)

    def _set_state(self):
        """Sets the state of the player, which is depending on velocity."""
        self.state = States.IDLE
        # When the player is moving, state changes
        if self.velocity_x > 0:
            self.state = States.MOVING_RIGHT
        if self.velocity_x < 0:
            self.state = States.MOVING_LEFT
        if self.velocity_y > 0:
            self.state = States.MOVING_DOWN
        if self.velocity_y < 0:
            self.state = States.MOVING_UP

    def _get_animation(self, frames: list):
        """Cycles through given frames to dynamically change the current image, thus creating an animation effect."""
        now = pygame.time.get_ticks()
        if now - self.last_updated > Settings.ANIMATION_SPEED:
            self.last_updated = now
            self.current_frame: int = (self.current_frame + 1) % len(frames)
            self.current_image = frames[self.current_frame]
            if Settings.DOUBLE_SCALE:
                self.current_image = scale_up_double(frames[self.current_frame])

    def _animate(self):
        """Handles animation."""
        if self.state.moving_right:
            self._get_animation(self.char.walking_frames_right)
        if self.state.moving_left:
            self._get_animation(self.char.walking_frames_left)
        if self.state.moving_up:
            self._get_animation(self.char.walking_frames_up)
        if self.state.moving_down:
            self._get_animation(self.char.walking_frames_down)

    def draw(self):
        """Draws the player image onto the screen."""
        self.window.screen.blit(self.current_image, self.rect)
        if Settings.DRAW_HIT_BOXES:
            draw_hit_box(self.window.screen, self.rect)

    def handle_movement_input(self, event):
        """Handles keyboard input that effect player movement."""
        if event.type == KEYDOWN:
            if event.key == self.keys.left:
                self.LEFT_KEY_PRESSED = True
            elif event.key == self.keys.right:
                self.RIGHT_KEY_PRESSED = True
            elif event.key == self.keys.up:
                self.UP_KEY_PRESSED = True
            elif event.key == self.keys.down:
                self.DOWN_KEY_PRESSED = True
        if event.type == KEYUP:
            self.state = States.IDLE
            if event.key == self.keys.left:
                self.LEFT_KEY_PRESSED = False
            elif event.key == self.keys.right:
                self.RIGHT_KEY_PRESSED = False
            elif event.key == self.keys.up:
                self.UP_KEY_PRESSED = False
            elif event.key == self.keys.down:
                self.DOWN_KEY_PRESSED = False
