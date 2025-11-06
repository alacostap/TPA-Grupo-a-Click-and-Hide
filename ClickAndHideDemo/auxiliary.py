"""
auxiliary.py — Funciones auxiliares para Click & Hide.

Incluye:
  - Lógica simple (dinero, tiempos de clic)
  - Dibujos comunes (fondo, cabecera, paneles)
"""

import pygame
import time
from config import *

# ---------- LÓGICA SIMPLE ----------

def clamp_money(money):
    """Limita el dinero a 0 o más."""
    return max(0, money)

def can_earn(last_earn_time):
    """Devuelve True si pasó el cooldown desde el último clic."""
    now = time.time()
    return now - last_earn_time >= EARN_COOLDOWN

# ---------- DIBUJO ----------

def draw_gradient_background(screen, width, height):
    """Dibuja un fondo degradado vertical beige."""
    for y in range(height):
        color = (250 - y // 15, 240 - y // 20, 210 - y // 30)
        pygame.draw.line(screen, color, (0, y), (width, y))

def draw_header(screen, font_medium, font_small, player):
    """Dibuja la cabecera con dinero, clics y ganancias."""
    header_height = 60
    width, _ = screen.get_size()

    for y in range(header_height):
        c = (180 + y // 3, 150 + y // 2, 100 + y // 3)
        pygame.draw.line(screen, c, (0, y), (width, y))

    money_text = font_medium.render(f"${int(player.money)}", True, (255, 255, 255))
    clicks_text = font_small.render(f"Clicks: {player.total_clicks}", True, (240, 240, 220))
    income_text = font_small.render(f"+{player.click_income}/click", True, (240, 255, 200))
    auto_text = font_small.render(f"+{player.auto_income:.1f}/s", True, (255, 240, 200))

    screen.blit(money_text, (20, 15))
    screen.blit(clicks_text, (300, 20))
    screen.blit(income_text, (600, 20))
    screen.blit(auto_text, (850, 20))

def draw_shop_panel(screen, panel_x, panel_y, panel_width, panel_h):
    """Dibuja el panel principal de la tienda con sombra y fondo beige."""
    pygame.draw.rect(screen, (150, 130, 100, 50),
                     (panel_x - 5, panel_y + 5, panel_width, panel_h), border_radius=15)
    pygame.draw.rect(screen, (245, 240, 220),
                     (panel_x, panel_y, panel_width, panel_h), border_radius=15)
