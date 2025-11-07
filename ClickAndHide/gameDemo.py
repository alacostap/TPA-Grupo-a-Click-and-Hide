"""
game.py — Lógica principal del juego Click & Hide (Versión Demo).

Contiene la ejecución automática del juego sin menú ni intro,
con IA sencilla que hace clic y compra ítems automáticamente.
"""

import pygame
import time
import os

from config import WIDTH, HEIGHT, FPS, MONEY_START
from auxiliary import draw_gradient_background, draw_header
from entities.player import Player
from entities.shop import Shop
from entities.achievements import Achievements


def run_game_demo():
    """Ejecuta el juego automáticamente sin menú ni intro, con IA sencilla."""
    # ----- CONFIGURACIÓN PANTALLA -----
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLICK AND HIDE")
    clock = pygame.time.Clock()

    # ----- FUENTES -----
    base_font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf")
    font_small = pygame.font.Font(base_font_path, 14)
    font_medium = pygame.font.Font(base_font_path, 18)
    font_big = pygame.font.Font(base_font_path, 28)

    # ----- ESTADO DEL JUEGO -----
    player = Player()
    shop = Shop()
    achievements_manager = Achievements()
    header_height = 60

    # ----- INICIALIZAR JUEGO -----
    player.reset(MONEY_START)
    shop.init_items()

    # ----- LOOP PRINCIPAL -----
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # ----- EVENTOS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # ----- IA SENCILLA: clic automático -----
        player.click()  # clic automático

        # ----- IA COMPRA AUTOMÁTICA -----
        for item in shop.items:
            while player.money >= item.cost:
                # Compramos directamente sin depender de rects
                player.money -= item["cost"]
                item["amount"] += 1
                item["cost"] = int(item["cost"] * 1.15)

                if item["tipo"] == "click":
                    player.click_income += item["base_income"]
                else:
                    player.auto_income += item["base_income"]

                if not hasattr(player, "upgrades_bought"):
                    player.upgrades_bought = 0
                player.upgrades_bought += 1

                # Actualizar logros
                game_state = {
                    "money": player.money,
                    "total_clicks": player.total_clicks,
                    "upgrades_bought": player.upgrades_bought
                }
                achievements_manager.update_achievements(game_state)

        # ----- DIBUJO Y ACTUALIZACIONES -----
        draw_gradient_background(screen, WIDTH, HEIGHT)
        draw_header(screen, font_medium, font_small, player)
        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        # ----- DINERO PASIVO -----
        player.apply_auto_income()

        # ----- ACTUALIZACIÓN DE LOGROS -----
        game_state = {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": sum(item.amount for item in shop.items)
        }
        achievements_manager.update_achievements(game_state)
        achievements_manager.manage_notifications(screen, font_small)

        pygame.display.flip()
