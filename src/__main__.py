from helpers.exceptions import GameOver, RestartGame
from space_rocks import SpaceRocks

if __name__ == "__main__":
    while True:
        try:
            space_rocks = SpaceRocks()
            space_rocks.main_loop()
        except GameOver:
            break
        except RestartGame:
            pass
