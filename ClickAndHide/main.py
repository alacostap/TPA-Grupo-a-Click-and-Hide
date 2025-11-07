"""
main.py — Entrada del juego Click & Hide.

Inicializa Pygame y lanza la ejecución principal desde `game.py`.
"""

import argparse
import pygame

class Main():

    def __init__(self):
        self.read_args()
        pygame.init()

        # Si estuviese correctamente estructurado, no seria necesario mantener dos copias del código
        if not self.args.demo:
            print("Demo OFF")
            from game import run_game
            """Inicia el juego."""
            run_game()

        else:
            print("Demo ON")
            from gameDemo import run_game_demo
            """Inicia la demo."""
            run_game_demo()

        pygame.quit()


    # https://docs.python.org/es/3/library/argparse.html
    def read_args(self):
        p = argparse.ArgumentParser(description="Mi programa")
        p.add_argument("--demo", action="store_true", help="Activa el modo demo")
        self.args = p.parse_args()



if __name__ == "__main__":
    Main()
