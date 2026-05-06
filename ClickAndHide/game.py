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

        # --- MENU ---
        if state == "menu":
            choice = show_main_menu(
                screen, font_small, font_big,
                game_started, player, achievements_manager
            )

            if choice in ["EXIT", "SALIR"]:
                running = False
                continue
            elif choice in ["PLAY", "JUGAR"]:
                state = "playing"
                continue
            elif choice in ["CONTINUE", "CONTINUAR"]:
                state = "playing"
                continue

        # --- EVENTS ---
        for event in events:

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_happened = True

                if hasattr(player, "click_rect") and player.click_rect.collidepoint(mouse_pos):
                    player.click()
                    save_game(player, shop)

                shop.handle_click(mouse_pos, player, achievements_manager)
                save_game(player, shop)

        # --- LOGIC ---
        profesor.update(events, mouse_pos, click_happened, player)

        # SOLO RESUELVE UNA VEZ
        if profesor.just_finished:
            if profesor.correct:
                player.money += 1000
            else:
                player.money -= 1000
            profesor.just_finished = False

        player.apply_auto_income()

        # ---------------- RENDER ----------------
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

    # --- SYSTEMS ---
    player = Player()
    shop = Shop()
    profesor = Profesor(WIDTH, HEIGHT)

    player.reset(MONEY_START)
    shop.init_items()

    # --- CONTROL ---
    state = "idle"
    timer = 0.0

    EVENT_COOLDOWN = 3
    last_event = 0.0

    ai_number = ""
    reward_given = False

    running = True
    start_time = time.time()

    # --- LOOP ---
    while running:

        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        if time.time() - start_time > 30:
            running = False

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # --- ECONOMÍA ---
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

        # --- PROFESOR UPDATE ---
        profesor.update(events, mouse_pos, False, player)

        timer += dt

        # --- SPAWN EVENTO ---
        if state == "idle":
            if time.time() - last_event > EVENT_COOLDOWN:
                if random.randint(1, 180) == 1:
                    profesor.trigger_event(player)
                    state = "question"
                    timer = 0
                    reward_given = False

        # --- PREGUNTA ---
        elif state == "question":
            if timer >= 2.0:
                ai_number = str(profesor.correct_result)
                state = "answer"
                timer = 0

        # --- RESPUESTA ---
        elif state == "answer":
            if timer >= 2.0:
                state = "reward"
                timer = 0

        # --- RECOMPENSA ---
        elif state == "reward":

            if not reward_given:
                player.money += 1000
                reward_given = True

            if timer >= 0.5:
                profesor.resolve(player)
                last_event = time.time()
                state = "idle"
                timer = 0

        # --- DRAW ---
        screen.blit(fondo_img, (0, 0))

        profesor.draw(screen)

        draw_header(screen, font_medium, font_small, player)

        player.draw_click_button(screen, font_medium, mouse_pos, WIDTH, HEIGHT)
        shop.draw(screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT)

        # --- RESPUESTA IA LUGAR ---
        if state in ["answer", "reward"] and profesor.in_event:

            # posición EXACTA del input del profesor (sin redibujar panel)
            panel_x = (profesor.width - 420) // 2
            panel_y = (profesor.height - 180) // 2

            txt = profesor.font.render(ai_number, True, (0, 0, 0))

            screen.blit(txt, (panel_x + 40, panel_y + 90))

        # --- PASIVO ---
        player.apply_auto_income()

        pygame.display.flip()