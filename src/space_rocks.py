import pygame as pg

from helpers.exceptions import ExitGame, RestartGame
from helpers.utils import get_random_position, load_sprite, print_text
from models.asteroid import Asteroid
from models.space_ship import Spaceship


class SpaceRocks:
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

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship(self._SPACESHIP_POSITION, self.bullets.append)

        for _ in range(self._NUM_ASTEROIDS):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self._MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def run_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pg.init()
        pg.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    raise ExitGame
                case pg.KEYDOWN:
                    match event.key:
                        case pg.K_ESCAPE:
                            raise ExitGame
                        case pg.K_RETURN:
                            raise RestartGame
                        case pg.K_SPACE:
                            if self.spaceship:
                                self.spaceship.shoot()

        # get user key
        if self.spaceship:
            is_key_pressed = pg.key.get_pressed()
            if is_key_pressed[pg.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pg.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pg.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        #  create a copies as removing elements from a list while iterating over it can cause errors
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pg.display.flip()
        self.clock.tick(self._FPS)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
