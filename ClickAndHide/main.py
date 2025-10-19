import pygame
import time
import os
from config import *
from entidades import Player
from utilidades import clamp_money
from upgrades import Upgrade
from intro import play_intro

# Menú y logros
from menu.menu import show_menu
from menu.logros import show_logros_panel, actualizar_logros, NotificacionLogro

pygame.init()

# ----------------- CONFIG -----------------
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CLICK AND HIDE")
clock = pygame.time.Clock()
FPS = 60

# Fuente
base_font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf")
font = pygame.font.Font(base_font_path, 24)
big_font = pygame.font.Font(base_font_path, 36)

# ----------------- GAME STATE -----------------
player = Player()
running = True
state = "menu"
game_started = False
auto_income = 0.0
last_auto_time = time.time()
notificaciones = []

# ----------------- UPGRADES -----------------
upgrade1 = Upgrade("Mejora 1", 10, 0.1, 0, 0)
upgrade2 = Upgrade("Mejora 2", 100, 0.5, 0, 0)
upgrade3 = Upgrade("Mejora 3", 1000, 1, 0, 0)
upgrades_list = [upgrade1, upgrade2, upgrade3]

# ----------------- INTRO -----------------
play_intro(screen, "inicio.png")

# ----------------- MAIN LOOP -----------------
while running:
    dt = clock.tick(FPS) / 1000.0
    now = time.time()
    mouse_pos = pygame.mouse.get_pos()

    # ----------------- MENÚ -----------------
    if state == "menu":
        choice = show_menu(screen, font, big_font, game_started)

        if choice == "SALIR":
            running = False
            continue
        elif choice in ["JUGAR", "CONTINUAR"]:
            state = "playing"
            if not game_started:
                player.money = MONEY_START
                player.total_clicks = 0
                auto_income = 0
                for upg in upgrades_list:
                    upg.level = 0
                    upg.cost = upg.base_cost
                last_auto_time = time.time()
                game_started = True
        continue

    # ----------------- EVENTOS -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state = "menu"
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        if state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Click cuadrado principal
            if click_rect.collidepoint(mouse_pos):
                player.money += 1
                player.total_clicks += 1
            # Upgrades
            for upg in upgrades_list:
                if upg.rect.collidepoint(mouse_pos):
                    gained = upg.buy(player)
                    if gained > 0:
                        player.upgrades_compra += 1
                        auto_income += gained

    # ----------------- INTERFAZ DE JUEGO -----------------
    if state == "playing":
        # Fondo
        screen.fill((230, 230, 230))

        # HEADER
        header_height = 80
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, header_height))
        money_text = font.render(f"${int(player.money)}", True, (255, 255, 255))
        screen.blit(money_text, (20, 20))

        clicks_text = font.render(f"Clicks: {player.total_clicks}", True, (200, 200, 200))
        screen.blit(clicks_text, (250, 20))

        menu_text = font.render("[ESC] Volver al Menú", True, (180, 180, 180))
        menu_rect = menu_text.get_rect(topright=(WIDTH - 20, 20))
        screen.blit(menu_text, menu_rect)

        # CENTRO: Cuadrado principal
        square_size = 200
        click_rect = pygame.Rect(WIDTH//2 - square_size//2, HEIGHT//2 - square_size//2, square_size, square_size)
        pygame.draw.rect(screen, (70, 130, 180), click_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), click_rect, 4, border_radius=15)
        click_label = font.render("CLICK", True, (255, 255, 255))
        label_rect = click_label.get_rect(center=click_rect.center)
        screen.blit(click_label, label_rect)

        # PANEL DERECHA: Upgrades
        panel_width = 300
        panel_x = WIDTH - panel_width
        pygame.draw.rect(screen, (240, 240, 240, 180), (panel_x, header_height, panel_width, HEIGHT - header_height))

        upg_y = header_height + 30
        for upg in upgrades_list:
            upg.rect.topleft = (panel_x + 30, upg_y)
            upg.draw(screen, font)
            upg_y += 110

        # AUTO INCOME
        if now - last_auto_time >= 1:
            player.money += auto_income
            last_auto_time = now
        player.money = clamp_money(player.money)

        # LOGROS
        nuevos_logros = actualizar_logros(player)
        for l in nuevos_logros:
            notificaciones.append(NotificacionLogro(l))

    # ----------------- NOTIFICACIONES -----------------
    for notif in notificaciones[:]:
        if not notif.update(dt):
            notificaciones.remove(notif)
        else:
            notif.draw(screen, font)

    pygame.display.flip()

pygame.quit()
