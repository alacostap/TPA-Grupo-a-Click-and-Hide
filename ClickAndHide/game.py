"""
game.py — Lógica principal del juego Click & Hide
"""

import pygame
import os
import time
import random

from config import WIDTH, HEIGHT, FPS, MONEY_START
from auxiliary import draw_header
from entities.player import Player
from entities.shop import Shop
from entities.achievements import Achievements
from profesor import Profesor
from intro import play_intro
from menu.main_menu import show_main_menu
from save import save_game, load_game

# --- GAME NORMAL ---
def run_game():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLICK AND HIDE")
    clock = pygame.time.Clock()

    base_font_path = os.path.join(
        os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf"
    )

    font_small = pygame.font.Font(base_font_path, 14)
    font_medium = pygame.font.Font(base_font_path, 18)
    font_big = pygame.font.Font(base_font_path, 28)

    base_dir = os.path.dirname(__file__)
    fondo_img = pygame.image.load(
        os.path.join(base_dir, "assets", "images", "clase.png")
    ).convert()

    fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

    player = Player()
    shop = Shop()
    achievements_manager = Achievements()
    profesor = Profesor(WIDTH, HEIGHT)

    load_game(player, shop)

    state = "menu"
    running = True
    game_started = player.total_clicks > 0 or player.money != MONEY_START

    play_intro(screen, "clase.png")

    while running:

        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        click_happened = False
        events = pygame.event.get()

        # MENU
        if state == "menu":
            choice = show_main_menu(
                screen, font_small, font_big,
                game_started, player, achievements_manager
            )

            if choice in ["EXIT", "SALIR"]:
                running = False
                continue
            elif choice in ["PLAY", "JUGAR", "CONTINUE", "CONTINUAR"]:
                state = "playing"
                continue

        # EVENTS
        for event in events:

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                    continue

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_happened = True

                if hasattr(player, "click_rect") and player.click_rect.collidepoint(mouse_pos):
                    player.click()
                    save_game(player, shop)

                shop.handle_click(mouse_pos, player, achievements_manager)
                save_game(player, shop)

        # PROFESOR
        profesor.update(events, mouse_pos, click_happened, player)

        # PASIVO
        if not getattr(player, "locked", False):
            player.apply_auto_income()

        # RENDER
        screen.blit(fondo_img, (0, 0))

        profesor.draw(screen)

        draw_header(screen, font_medium, font_small, player)

        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        achievements_manager.update_achievements({
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": sum(i.amount for i in shop.items)
        })

        pygame.display.flip()


# --- DEMO ---
def run_game_demo():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLICK AND HIDE — DEMO")
    clock = pygame.time.Clock()

    base_font_path = os.path.join(
        os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf"
    )

    font_small = pygame.font.Font(base_font_path, 14)
    font_medium = pygame.font.Font(base_font_path, 18)
    font_big = pygame.font.Font(base_font_path, 28)

    base_dir = os.path.dirname(__file__)

    fondo_img = pygame.image.load(
        os.path.join(base_dir, "assets", "images", "clase.png")
    ).convert()

    fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

    player = Player()
    shop = Shop()
    profesor = Profesor(WIDTH, HEIGHT)

    player.reset(MONEY_START)
    shop.init_items()

    state = "idle"
    timer = 0.0
    last_event = 0.0

    ai_number = ""
    reward_given = False

    running = True
    start_time = time.time()

    while running:

        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        if time.time() - start_time > 30:
            running = False

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # DINERO DEMO
        if not getattr(player, "locked", False):
            player.click()
            player.apply_auto_income()

        profesor.update(events, mouse_pos, False, player)

        timer += dt

        if state == "idle":
            if time.time() - last_event > 3:
                if random.randint(1, 180) == 1:
                    profesor.trigger_event(player)
                    state = "question"
                    timer = 0
                    reward_given = False

        elif state == "question":
            if timer >= 2:
                ai_number = str(profesor.correct_result)
                profesor.answer = ai_number
                state = "answer"
                timer = 0

        elif state == "answer":
            if timer >= 2:
                state = "reward"
                timer = 0

        elif state == "reward":
            if not reward_given:
                player.money += 1000
                reward_given = True

            if timer >= 0.5:
                profesor.resolve(player)
                last_event = time.time()
                state = "idle"
                timer = 0

        # DRAW
        screen.blit(fondo_img, (0, 0))
        profesor.draw(screen)
        draw_header(screen, font_medium, font_small, player)
        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        pygame.display.flip()
