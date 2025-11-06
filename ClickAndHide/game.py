"""
game.py — Lógica principal del juego Click & Hide.

Contiene el bucle principal, manejo de menús, eventos y dibujo de pantalla.
Incluye la gestión de dinero pasivo, clics, tienda y logros.
"""

import pygame
import time
import os

from config import WIDTH, HEIGHT, FPS, MONEY_START
from auxiliary import draw_gradient_background, draw_header
from entities.player import Player
from entities.shop import Shop
from entities.achievements import Achievements
from intro import play_intro
from menu.main_menu import show_main_menu
from menu.achievements_menu import show_achievements_panel


def run_game():
    """Ejecuta el bucle principal del juego con menú, eventos, tienda y logros."""
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
    running = True
    state = "menu"
    game_started = False
    header_height = 60

    # ----- INTRO -----
    play_intro(screen, "clase.png")

    # ----- LOOP PRINCIPAL -----
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # ----- MENÚ PRINCIPAL -----
        if state == "menu":
            choice = show_main_menu(screen, font_small, font_big, game_started, player, achievements_manager)
            if choice in ["EXIT", "SALIR"]:
                running = False
                continue
            elif choice in ["PLAY", "CONTINUE", "JUGAR", "CONTINUAR"]:
                state = "playing"
                if not game_started:
                    player.reset(MONEY_START)
                    shop.init_items()
                    game_started = True
            continue

        # ----- EVENTOS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            elif state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if player.click_rect.collidepoint(mouse_pos):
                        player.click()
                    # Aquí llamamos a handle_click con achievements_manager
                    shop.handle_click(mouse_pos, player, achievements_manager)
                shop.handle_scroll(event)
                shop.handle_mouse_events(event, mouse_pos, header_height, HEIGHT - header_height)

        # ----- DIBUJO Y ACTUALIZACIONES -----
        if state == "playing":
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
                "upgrades_bought": sum(item["amount"] for item in shop.items)
            }

            # Actualiza logros y prepara notificaciones
            achievements_manager.update_achievements(game_state)

            # Dibuja todas las notificaciones activas
            achievements_manager.manage_notifications(screen, font_small)

        pygame.display.flip()
