"""
game.py — Lógica principal del juego Click & Hide.

Contiene tanto el modo normal (con menú, intro y guardado)
como el modo demo (automático, sin menú ni intro).
"""

import pygame
import os
import time

from config import WIDTH, HEIGHT, FPS, MONEY_START
from auxiliary import draw_gradient_background, draw_header
from entities.player import Player
from entities.shop import Shop
from entities.achievements import Achievements
from intro import play_intro
from menu.main_menu import show_main_menu
from save import save_game, load_game


# --- MODO NORMAL DEL JUEGO ---
def run_game():
    """
    Ejecuta el bucle principal del juego Click & Hide.

    Este modo incluye:
      - Menú principal con opciones de juego.
      - Pantalla de introducción.
      - Sistema de guardado/carga de progreso.
      - Gestión de clics, compras y logros.

    Comportamiento:
      - Usa `ESC` para volver al menú.
      - Guarda el progreso automáticamente tras cada acción.
      - Dibuja interfaz principal (fondo, cabecera, tienda, etc.).

    """
    # --- Configuración de pantalla ---
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLICK AND HIDE")
    clock = pygame.time.Clock()

    # --- Fuentes ---
    base_font_path = os.path.join(
        os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf"
    )
    font_small = pygame.font.Font(base_font_path, 14)
    font_medium = pygame.font.Font(base_font_path, 18)
    font_big = pygame.font.Font(base_font_path, 28)

    # --- Estado inicial ---
    player = Player()
    shop = Shop()
    achievements_manager = Achievements()
    load_game(player, shop)  # Carga el progreso anterior (si existe)

    running = True
    state = "menu"
    header_height = 60
    game_started = player.total_clicks > 0 or player.money != MONEY_START

    # --- Intro inicial ---
    play_intro(screen, "clase.png")

    # --- Bucle principal ---
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # --- Menú principal ---
        if state == "menu":
            choice = show_main_menu(
                screen, font_small, font_big, game_started, player, achievements_manager
            )
            if choice in ["EXIT", "SALIR"]:
                running = False
                continue
            elif choice in ["PLAY", "JUGAR"]:
                state = "playing"
                if not game_started:
                    player.reset(MONEY_START)
                    shop.init_items()
                    game_started = True
                continue
            elif choice in ["CONTINUE", "CONTINUAR"]:
                state = "playing"
                continue
            elif choice in ["ACHIEVEMENTS", "LOGROS", "CREDITS", "CRÉDITOS"]:
                continue  # Futuras implementaciones

        # --- Gestión de eventos ---
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
                        save_game(player, shop)
                    shop.handle_click(mouse_pos, player, achievements_manager)
                    save_game(player, shop)
                shop.handle_scroll(event)
                shop.handle_mouse_events(
                    event, mouse_pos, header_height, HEIGHT - header_height
                )

        # --- Actualización y dibujo ---
        if state == "playing":
            draw_gradient_background(screen, WIDTH, HEIGHT)
            draw_header(screen, font_medium, font_small, player)
            player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
            shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

            # Dinero pasivo
            player.apply_auto_income()
            save_game(player, shop)

            # Actualización de logros
            game_state = {
                "money": player.money,
                "total_clicks": player.total_clicks,
                "upgrades_bought": sum(item.amount for item in shop.items),
            }
            achievements_manager.update_achievements(game_state)
            achievements_manager.manage_notifications(screen, font_small)

        pygame.display.flip()


# --- MODO DEMO AUTOMÁTICO ---
def run_game_demo():
    """
    Ejecuta una versión automática del juego (modo demostración).

    Este modo no incluye menú ni intro, y funciona sin interacción del jugador.

    Características:
      - Realiza clics automáticos periódicos.
      - Compra ítems de la tienda según el dinero disponible.
      - Se cierra automáticamente después de 30 segundos.

    Ideal para pruebas rápidas o capturas de pantalla.

    """
    # --- Configuración de pantalla ---
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLICK AND HIDE — DEMO")
    clock = pygame.time.Clock()

    # --- Fuentes ---
    base_font_path = os.path.join(
        os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf"
    )
    font_small = pygame.font.Font(base_font_path, 14)
    font_medium = pygame.font.Font(base_font_path, 18)
    font_big = pygame.font.Font(base_font_path, 28)

    # --- Estado inicial ---
    player = Player()
    shop = Shop()
    achievements_manager = Achievements()
    header_height = 60

    player.reset(MONEY_START)
    shop.init_items()

    # --- Límite temporal de la demo ---
    start_time = time.time()
    max_duration = 30  # segundos

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # Salida automática tras el límite
        if time.time() - start_time > max_duration:
            print("Demo finalizada automáticamente.")
            running = False

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- IA: clics y compras automáticas ---
        player.click()
        for item in shop.items:
            while player.money >= item.cost:
                player.money -= item.cost
                item.amount += 1
                item.cost = int(item.cost * 1.15)
                if item.tipo == "click":
                    player.click_income += item.base_income
                else:
                    player.auto_income += item.base_income
                player.upgrades_bought = getattr(player, "upgrades_bought", 0) + 1

                game_state = {
                    "money": player.money,
                    "total_clicks": player.total_clicks,
                    "upgrades_bought": player.upgrades_bought,
                }
                achievements_manager.update_achievements(game_state)

        # --- Dibujo ---
        draw_gradient_background(screen, WIDTH, HEIGHT)
        draw_header(screen, font_medium, font_small, player)
        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        # Dinero pasivo + logros
        player.apply_auto_income()
        game_state = {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": sum(item.amount for item in shop.items),
        }
        achievements_manager.update_achievements(game_state)
        achievements_manager.manage_notifications(screen, font_small)

        pygame.display.flip()
