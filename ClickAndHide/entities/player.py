# entities/player.py
import time
import pygame
from config import MONEY_START, EARN_COOLDOWN
from utilities import clamp_money, can_earn

class Player:
    def __init__(self):
        self.money = MONEY_START
        self.total_clicks = 0
        self.click_income = 1
        self.auto_income = 0
        self.last_auto_time = time.time()
        self.last_click_time = time.time()

    def reset(self, money=MONEY_START):
        self.money = money
        self.total_clicks = 0
        self.click_income = 1
        self.auto_income = 0
        self.last_auto_time = time.time()
        self.last_click_time = time.time()

    def click(self):
        """Agregar dinero por click si el cooldown pasó."""
        if can_earn(self.last_click_time):
            self.money += self.click_income
            self.total_clicks += 1
            self.last_click_time = time.time()
            self.money = clamp_money(self.money)

    def apply_auto_income(self, now=None):
        """Agregar dinero automáticamente cada segundo."""
        now = now or time.time()
        if now - self.last_auto_time >= 1:
            self.money += self.auto_income
            self.last_auto_time = now
            self.money = clamp_money(self.money)

    def can_afford(self, amount):
        return self.money >= amount

    # ------------------ DIBUJO DEL BOTÓN CLICK ------------------
    def draw_click_button(self, screen, font, mouse_pos, WIDTH, HEIGHT):
        """Dibuja el botón central de click."""
        square_size = 180
        self.click_rect = pygame.Rect(WIDTH // 2 - square_size // 2 - 180,
                                      HEIGHT // 2 - square_size // 2,
                                      square_size, square_size)

        color_click = (235, 200, 120) if self.click_rect.collidepoint(mouse_pos) else (225, 190, 110)
        pygame.draw.rect(screen, color_click, self.click_rect, border_radius=25)
        pygame.draw.rect(screen, (90, 70, 40), self.click_rect, 3, border_radius=25)
        label_rect = font.render("CLICK", True, (60, 40, 20)).get_rect(center=self.click_rect.center)
        screen.blit(font.render("CLICK", True, (60, 40, 20)), label_rect)
