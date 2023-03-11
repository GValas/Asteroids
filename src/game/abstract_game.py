from abc import ABC, abstractmethod


class AbstractGame(ABC):
    @abstractmethod
    def _handle_input(self):
        pass

    @abstractmethod
    def _process_game_logic(self):
        pass

    @abstractmethod
    def _draw(self):
        pass

    def run_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
