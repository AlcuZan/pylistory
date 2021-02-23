"""Module for sprite sheet handling"""
import pygame
import json

from data import utils
from data.paths import MapAssets
from config.config import Colors


class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename  # of the sprite sheet
        self.sprite_sheet = utils.load_img(filename, convert=True)
        self.metadata = MapAssets.SPRITE_SHEET_METADATA
        self.data = None
        self.get_json()

    def get_json(self):
        """Gets JSON information. Only works if JSON is in JSON-TP-Hash format."""
        with open(self.metadata) as file:
            self.data = json.load(file)
            file.close()

    def _get_sprite(self, x, y, width, height) -> pygame.Surface:
        """Gets sprite from sprite sheet using metadata from JSON file."""
        # Surface with width and height of the sprite
        sprite = pygame.Surface((width, height))
        # Handles transparency (there would be a black border around the image if this wasn't done)
        sprite.set_colorkey(Colors.BLACK)
        # Paste image from sprite sheet
        # noinspection PyTypeChecker
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def parse_sprite(self, name: str) -> pygame.Surface:
        """Parses sprite with given name from sprite sheet."""
        # Looks for the sprite in the data from the JSON and extracts the metadata
        sprite = self.data["frames"][name]["frame"]
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        # Creates an image out of the extracted metadata
        image = self._get_sprite(x, y, width, height)
        return image
