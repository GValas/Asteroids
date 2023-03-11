import random as rd

import pygame as pg


def load_sprite(name: str, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = pg.image.load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface: pg.Surface) -> pg.Vector2:
    x, y = position
    w, h = surface.get_size()
    return pg.Vector2(x % w, y % h)


def get_random_position(surface: pg.Surface) -> pg.Vector2:
    return pg.Vector2(
        rd.randrange(surface.get_width()),
        rd.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = rd.randint(min_speed, max_speed)
    angle = rd.randrange(0, 360)
    return pg.Vector2(speed, 0).rotate(angle)


def load_sound(name: str):
    path = f"assets/sounds/{name}.wav"
    return pg.mixer.Sound(path)


def print_text(surface: pg.Surface, text: str, font, color=pg.Color("tomato")) -> None:
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = pg.Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)
