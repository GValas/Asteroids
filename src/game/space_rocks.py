from typing import List

import pygame as pg

from game.abstract_game import AbstractGame
from helpers.exceptions import ExitGame, RestartGame
from helpers.utils import get_random_position, load_sprite, print_text
from models.asteroid import Asteroid
from models.bullet import Bullet
from models.space_ship import Spaceship


class SpaceRocks(AbstractGame):
    _MIN_ASTEROID_DISTANCE = 250
    _NUM_ASTEROIDS = 6
    _SCREEN_DIMENSIONS = (800, 600)
    _SPACESHIP_POSITION = (400, 300)
    _FPS = 60

    def __init__(self):
        self._init_pygame()
        self.screen = pg.display.set_mode(self._SCREEN_DIMENSIONS)
        self.background = load_sprite("space", False)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 64)
        self.message = ""

        self.asteroids: List[Asteroid] = []
        self.bullets: List[Bullet] = []
        self.spaceship = Spaceship(self._SPACESHIP_POSITION, self.bullets.append)

        for _ in range(self._NUM_ASTEROIDS):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self._MIN_ASTEROID_DISTANCE
                ):
                    break

            new_asteroid = Asteroid(position, self.asteroids.append)
            self.asteroids.append(new_asteroid)

    def _init_pygame(self):
        pg.init()
        pg.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pg.event.get():
            match event.type:
                # window quit button
                case pg.QUIT:
                    raise ExitGame

                # user keyboard input
                case pg.KEYDOWN:
                    match event.key:
                        # press escape to quit game
                        case pg.K_ESCAPE:
                            raise ExitGame

                        # press enter to start new game
                        case pg.K_RETURN:
                            raise RestartGame

                        # press space to shoot
                        case pg.K_SPACE:
                            if self.spaceship:
                                self.spaceship.shoot()

        # get key continuously pressed by user
        if self.spaceship:
            is_key_pressed = pg.key.get_pressed()
            if is_key_pressed[pg.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pg.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pg.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        self._move_objects()
        self._handle_asteroids_collision()
        self._handle_spaceship_asteroids_collision()
        self._handle_bullets_asteroids_collision()
        self._remove_off_screen_bullets()
        self._check_won_game()

    def _move_objects(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

    def _check_won_game(self):
        if not self.asteroids and self.spaceship:
            self.message = "You won!"

    def _handle_asteroids_collision(self):
        asteroids = self.asteroids[:]
        while asteroids:
            a1 = asteroids.pop()
            for a2 in asteroids:
                if a1.collides_with(a2):
                    a1.velocity, a2.velocity = a2.velocity, a1.velocity

    def _handle_spaceship_asteroids_collision(self):
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

    def _remove_off_screen_bullets(self):
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    def _handle_bullets_asteroids_collision(self):
        #  create a copies as removing elements from a list while iterating over it can cause errors
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pg.display.update()
        self.clock.tick(self._FPS)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
