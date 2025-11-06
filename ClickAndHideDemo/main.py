"""
main.py — Entrada del juego Click & Hide.

Inicializa Pygame y lanza la ejecución principal desde `game.py`.
"""

import pygame
from game import run_game


def main():
    """Inicia el juego."""
    pygame.init()
    run_game()
    pygame.quit()


if __name__ == "__main__":
    main()
