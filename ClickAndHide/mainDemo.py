"""
main.py — Entrada de la demo del juego Click & Hide.

Inicializa Pygame y lanza la ejecución principal desde `game.py`.
"""

import pygame
from gameDemo import run_game_demo


def main():
    """Inicia el juego."""
    pygame.init()
    run_game_demo()
    pygame.quit()


if __name__ == "__main__":
    main()
