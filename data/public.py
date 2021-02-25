"""Public module"""
from typing import Optional

import pygame

from data.player import Characters, Character

clock = pygame.time.Clock()
p1_char: Optional[Character] = Characters.ELIAS
p2_char: Optional[Character] = Characters.KLAUS
