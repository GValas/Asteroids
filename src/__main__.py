from helpers.exceptions import ExitGame, GameOver, RestartGame
from space_rocks import SpaceRocks

if __name__ == "__main__":
    while True:
        try:
            game = SpaceRocks()
            game.run_loop()

        except RestartGame:
            pass

        except ExitGame:
            break

        except GameOver:
            break
