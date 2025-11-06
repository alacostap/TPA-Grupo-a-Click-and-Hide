"""
game.py — Versión automática (IA simple) del juego Click & Hide.
El juego se ejecuta solo: la IA hace clics y compra ítems automáticamente.
"""

import pygame
import time
import os
from config import WIDTH, HEIGHT, FPS, MONEY_START
from auxiliary import draw_gradient_background, draw_header
from entities.player import Player
from entities.shop import Shop
from entities.achievements import Achievements


def run_game():
    """Ejecuta el juego de forma automática con una IA básica."""
    # ----- CONFIGURACIÓN PANTALLA -----
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLICK AND HIDE — Modo Automático (IA)")
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
    running = True
    header_height = 60

    # Reiniciar jugador y tienda
    player.reset(MONEY_START)
    shop.init_items()

    # ----- VARIABLES IA -----
    last_click_time = 0
    click_interval = 0.2  # segundos entre clics automáticos
    buy_interval = 1.0    # cada segundo intenta comprar algo
    last_buy_time = 0

    # ----- LOOP PRINCIPAL -----
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # ----- EVENTOS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

        # ----- IA: CLICK AUTOMÁTICO -----
        now = time.time()
        if now - last_click_time >= click_interval:
            player.click()  # simula click
            last_click_time = now

        # ----- IA: COMPRA AUTOMÁTICA -----
        if now - last_buy_time >= buy_interval:
            affordable_items = [item for item in shop.items if player.can_afford(item["cost"])]
            if affordable_items:
                # compra el más barato disponible
                cheapest = min(affordable_items, key=lambda x: x["cost"])
                player.money -= cheapest["cost"]
                cheapest["amount"] += 1
                cheapest["cost"] = int(cheapest["cost"] * 1.15)
                if cheapest["tipo"] == "click":
                    player.click_income += cheapest["base_income"]
                else:
                    player.auto_income += cheapest["base_income"]
            last_buy_time = now

        # ----- DINERO PASIVO -----
        player.apply_auto_income()

        # ----- DIBUJO -----
        draw_gradient_background(screen, WIDTH, HEIGHT)
        draw_header(screen, font_medium, font_small, player)
        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        # ----- LOGROS -----
        game_state = {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": sum(i["amount"] for i in shop.items)
        }
        achievements_manager.update(game_state)
        achievements_manager.draw_notifications(screen, font_small)

        pygame.display.flip()

    pygame.quit()
