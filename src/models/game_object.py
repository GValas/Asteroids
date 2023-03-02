import pygame as pg

from helpers.utils import wrap_position


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = pg.math.Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() * 0.5
        self.velocity = pg.math.Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - pg.math.Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
