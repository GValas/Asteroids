import pygame as pg

from helpers.utils import get_random_velocity, load_sprite
from models.game_object import GameObject


class Asteroid(GameObject):
    _SCALE_TABLE = {
        3: 1,
        2: 0.5,
        1: 0.25,
    }

    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        scale = self._SCALE_TABLE[size]
        sprite = pg.transform.rotozoom(load_sprite("asteroid"), 0, scale)
        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)
