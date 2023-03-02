import random as rd

import pygame as pg


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = pg.image.load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return pg.math.Vector2(x % w, y % h)


def get_random_position(surface):
    return pg.math.Vector2(
        rd.randrange(surface.get_width()),
        rd.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = rd.randint(min_speed, max_speed)
    angle = rd.randrange(0, 360)
    return pg.math.Vector2(speed, 0).rotate(angle)


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return pg.mixer.Sound(path)


def print_text(surface, text, font, color=pg.Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = pg.math.Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)
