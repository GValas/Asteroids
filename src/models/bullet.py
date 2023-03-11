import pygame as pg

from helpers.utils import load_sprite
from models.game_object import GameObject


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface: pg.Surface):
        self.position = self.position + self.velocity
