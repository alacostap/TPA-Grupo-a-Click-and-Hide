import time
import pygame
from config import MONEY_START
from auxiliary import clamp_money, can_earn


class Player:

    def __init__(self):
        self.money = MONEY_START
        self.total_clicks = 0
        self.click_income = 1
        self.auto_income = 0
        self.last_auto_time = time.time()
        self.last_click_time = time.time()

        # BLOQUEO PROFESOR
        self.locked = False

    def reset(self, money=MONEY_START):
        self.money = money
        self.total_clicks = 0
        self.click_income = 1
        self.auto_income = 0
        self.last_auto_time = time.time()
        self.last_click_time = time.time()
        self.locked = False

    def click(self):
        if self.locked:
            return

        if can_earn(self.last_click_time):
            self.money += self.click_income
            self.total_clicks += 1
            self.last_click_time = time.time()
            self.money = clamp_money(self.money)

    def apply_auto_income(self, now=None):
        if self.locked:
            return

        now = now or time.time()
        if now - self.last_auto_time >= 1:
            self.money += self.auto_income
            self.last_auto_time = now
            self.money = clamp_money(self.money)

    def can_afford(self, amount):
        return self.money >= amount

    # --- CLICK LOGO ---
    def is_click_on_logo(self, mouse_pos):
        if not hasattr(self, "logo_rect"):
            return False

        if not self.logo_rect.collidepoint(mouse_pos):
            return False

        rel_x = mouse_pos[0] - self.logo_rect.x
        rel_y = mouse_pos[1] - self.logo_rect.y

        try:
            pixel = self.logo_scaled.get_at((rel_x, rel_y))
            return pixel.a > 10
        except:
            return False

    # --- DRAW ---
    def draw_click_button(self, screen, font, mouse_pos, WIDTH, HEIGHT):

        scale = 1.5
        base_width = int(300 * scale)
        base_height = int(225 * scale)

        offset_y = 170

        x = WIDTH // 2 - base_width // 2 - 180
        y = HEIGHT // 2 - base_height // 2 + offset_y

        self.click_rect = pygame.Rect(x, y, base_width, base_height)

        if not hasattr(self, "logo_img"):
            import os
            base_dir = os.path.dirname(os.path.dirname(__file__))
            logo_path = os.path.join(base_dir, "assets", "images", "logo.png")
            self.logo_img = pygame.image.load(logo_path).convert_alpha()

        self.logo_scaled = pygame.transform.smoothscale(
            self.logo_img,
            (base_width, base_height)
        )

        self.logo_rect = self.logo_scaled.get_rect(center=self.click_rect.center)

        screen.blit(self.logo_scaled, self.logo_rect.topleft)