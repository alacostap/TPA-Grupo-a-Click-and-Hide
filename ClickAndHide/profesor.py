"""
profesor.py
"""

import pygame
import os
import random
import time


class Profesor:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        current = os.path.abspath(__file__)
        while True:
            current = os.path.dirname(current)
            if os.path.basename(current) == "ClickAndHide":
                break

        base_dir = current

        self.prof1_path = os.path.join(base_dir, "assets", "images", "Profesor1.png")
        self.prof2_path = os.path.join(base_dir, "assets", "images", "Profesor2.png")

        self.prof1_img = pygame.image.load(self.prof1_path).convert_alpha()
        self.prof2_img = pygame.image.load(self.prof2_path).convert_alpha()

        self.prof1_img = pygame.transform.scale(self.prof1_img, (width, height))
        self.prof2_img = pygame.transform.scale(self.prof2_img, (width, height))

        self.active = False
        self.in_event = False

        self.num1 = 0
        self.num2 = 0
        self.answer = ""
        self.correct_result = 0

        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 30)

        self.event_start_time = 0
        self.event_duration = 10

        self.beige = (239, 222, 205)
        self.brown = (120, 80, 50)

    # --- EVENT ---
    def trigger_event(self, player):
        self.in_event = True
        self.active = True
        player.locked = True

        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.correct_result = self.num1 + self.num2

        self.answer = ""
        self.event_start_time = time.time()

    # --- UPDATE ---
    def update(self, events, mouse_pos, click_happened, player):

        if click_happened and not self.in_event:
            if random.randint(1, 10) == 1:
                self.trigger_event(player)

        if self.in_event:
            for event in events:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:
                        self.answer = self.answer[:-1]

                    elif event.key == pygame.K_RETURN:
                        self.resolve(player)

                    else:
                        if event.unicode.isdigit():
                            self.answer += event.unicode

            # timeout
            if time.time() - self.event_start_time > self.event_duration:
                self.resolve(player, timeout=True)

    # --- RESOLVE (AQUÍ SE GESTIONA TODO) ---
    def resolve(self, player, timeout=False):

        if timeout:
            player.money -= 1000
        else:
            try:
                if int(self.answer) == self.correct_result:
                    player.money += 1000
                else:
                    player.money -= 1000
            except:
                player.money -= 1000

        player.locked = False
        self.in_event = False
        self.active = False
        self.answer = ""

    # --- PANEL ---
    def draw_panel(self, screen):
        panel_width = 420
        panel_height = 180

        x = (self.width - panel_width) // 2
        y = (self.height - panel_height) // 2

        rect = pygame.Rect(x, y, panel_width, panel_height)

        pygame.draw.rect(screen, self.beige, rect, border_radius=20)
        pygame.draw.rect(screen, self.brown, rect, 4, border_radius=20)

        return rect

    # --- TIMER ---
    def draw_timer(self, screen, panel):
        elapsed = time.time() - self.event_start_time
        progress = max(0, 1 - (elapsed / self.event_duration))

        bar_width = panel.width - 60
        x = panel.x + 30
        y = panel.y + panel.height - 25

        pygame.draw.rect(screen, (80, 80, 80), (x, y, bar_width, 12), border_radius=6)
        pygame.draw.rect(screen, (0, 200, 0), (x, y, int(bar_width * progress), 12), border_radius=6)

    # --- DRAW ---
    def draw(self, screen):

        if self.active:
            screen.blit(self.prof2_img, (0, 0))
        else:
            screen.blit(self.prof1_img, (0, 0))

        if self.in_event:
            panel = self.draw_panel(screen)

            q = f"{self.num1} + {self.num2} = ?"

            screen.blit(self.font.render(q, True, self.brown), (panel.x + 40, panel.y + 30))
            screen.blit(self.font.render(self.answer, True, (0, 0, 0)), (panel.x + 40, panel.y + 90))
            screen.blit(self.small_font.render("ENTER para responder", True, self.brown),
                        (panel.x + 40, panel.y + 120))

            self.draw_timer(screen, panel)