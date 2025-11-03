import pygame
import time
import os

from config import *
from utilities import clamp_money, draw_gradient_background, draw_header
from entities.player import Player
from entities.shop import Shop
from intro import play_intro
from menu.main_menu import show_main_menu
from menu.achievements_menu import Achievements  # Ahora es la clase

pygame.init()

# ----- CONFIGURACIÓN PANTALLA -----
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CLICK AND HIDE")
clock = pygame.time.Clock()

# ----- FONTS -----
base_font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf")
font_small = pygame.font.Font(base_font_path, 14)
font_medium = pygame.font.Font(base_font_path, 18)
font_big = pygame.font.Font(base_font_path, 28)

# ----- ESTADO DEL JUEGO -----
player = Player()
shop = Shop()
achievements_manager = Achievements()  # Instanciamos Achievements
running = True
state = "menu"
game_started = False

# ----- INTRO -----
play_intro(screen, "clase.png")

# ----- LOOP PRINCIPAL -----
while running:
    dt = clock.tick(FPS) / 1000.0
    now = time.time()
    mouse_pos = pygame.mouse.get_pos()

    # ----- MENU PRINCIPAL -----
    if state == "menu":
        choice = show_main_menu(screen, font_small, font_big, game_started, player, achievements_manager)
        if choice in ["EXIT", "SALIR"]:
            running = False
            continue
        elif choice in ["PLAY", "CONTINUE", "JUGAR", "CONTINUAR"]:
            state = "playing"
            if not game_started:
                player.reset(MONEY_START)
                shop.reset_items()
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
        elif state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player.click_rect.collidepoint(mouse_pos):
                player.click()
            shop.handle_click(mouse_pos, player)

    # ----- DIBUJOS -----
    if state == "playing":
        draw_gradient_background(screen, WIDTH, HEIGHT)
        draw_header(screen, font_medium, font_small, player)
        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        # Actualizamos logros y mostramos notificaciones
        game_state = {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": getattr(player, "upgrades_bought", 0)
        }
        achievements_manager.update(game_state)
        achievements_manager.draw_notifications(screen, font_small)

    pygame.display.flip()

pygame.quit()
