"""
main.py — Punto de entrada principal del juego Click & Hide.

Inicializa Pygame y ejecuta el modo de juego normal o demo según los argumentos de línea de comandos.

Uso:
    python main.py         # Ejecuta el juego normalmente
    python main.py --demo  # Ejecuta el modo demostración automático
"""

import argparse
import pygame


class Main:
    """Clase principal que inicializa y ejecuta el juego Click & Hide."""

    def __init__(self):
        """Inicializa Pygame, lee los argumentos y lanza el juego o la demo."""
        self.read_args()
        pygame.init()

        if not self.args.demo:
            print("Demo OFF — iniciando modo normal.")
            from game import run_game

            run_game()
        else:
            print("Demo ON — iniciando modo demostración.")
            from game import run_game_demo

            run_game_demo()

        pygame.quit()

    # --- ARGUMENTOS DE CONSOLA ---
    def read_args(self):
        """Lee los argumentos de ejecución desde la consola."""
        parser = argparse.ArgumentParser(
            description="Click & Hide — Juego de clicker con tienda y logros."
        )
        parser.add_argument(
            "--demo",
            action="store_true",
            help="Ejecuta el modo demo automático (sin menú ni intro).",
        )
        self.args = parser.parse_args()


# --- EJECUCIÓN DIRECTA ---
if __name__ == "__main__":
    Main()
