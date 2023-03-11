from game.space_rocks import SpaceRocks
from helpers.exceptions import ExitGame, RestartGame

if __name__ == "__main__":
    while True:
        try:
            game = SpaceRocks()
            game.run_loop()

        except RestartGame:
            pass

        except ExitGame:
            break
