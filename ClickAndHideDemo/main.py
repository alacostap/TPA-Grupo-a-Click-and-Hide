import pygame
import time
import os

from config import *
from utilities import clamp_money, draw_gradient_background, draw_header
from entities.player import Player
from entities.shop import Shop

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
running = True
state = "playing"        # Arranca directamente en modo juego
game_started = True
header_height = 60

# ----- AUTO MODO -----
auto_mode = True         # Si está True, el juego se juega solo
auto_click_timer = 0
auto_buy_timer = 0

# ----- INTRO -----
# Sin intro en este modo automático
# Inicializa el jugador y la tienda
player.reset(MONEY_START)
shop.reset_items()

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
                running = False  # sale completamente
            elif event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

        elif not auto_mode:
            # Click manual
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.click_rect.collidepoint(mouse_pos):
                    player.click()
                shop.handle_click(mouse_pos, player)

            # Scroll con la rueda
            shop.handle_scroll(event)

            # Arrastre del slider
            shop.handle_mouse_events(event, mouse_pos, header_height, HEIGHT - header_height)

    # ----- LÓGICA PRINCIPAL -----
    if state == "playing":
        # ---------- AUTO JUEGO ----------
        if auto_mode:
            # Auto clic cada 0.2 segundos
            auto_click_timer += dt
            if auto_click_timer >= 0.2:
                player.click()
                auto_click_timer = 0

            # Auto compra cada 1.5 segundos
            auto_buy_timer += dt
            if auto_buy_timer >= 1.5:
                affordable_items = [item for item in shop.items if item.cost <= player.money]
                if affordable_items:
                    cheapest = min(affordable_items, key=lambda i: i.cost)
                    if hasattr(cheapest, "rect"):
                        fake_pos = cheapest.rect.center
                        shop.handle_click(fake_pos, player)
                auto_buy_timer = 0

        # ---------- DIBUJADO ----------
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

    pygame.display.flip()

pygame.quit()
