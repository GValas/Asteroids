from pygame.math import Vector2
from pygame.transform import rotozoom

from helpers.utils import load_sound, load_sprite, wrap_position
from models.bullet import Bullet
from models.game_object import GameObject

UP = Vector2(0, -1)


class Spaceship(GameObject):
    _MANEUVERABILITY = 3
    _ACCELERATION = 0.25
    _BULLET_SPEED = 3
    _FRICTION = 0.99

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self._MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self._ACCELERATION

    def decelerate(self):
        self.velocity *= self._FRICTION

    def shoot(self):
        bullet_velocity = self.direction * self._BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
        self.decelerate()
