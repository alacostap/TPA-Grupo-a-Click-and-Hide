"""
auxiliary.py — Funciones auxiliares para Click & Hide.

Incluye utilidades generales:
- Lógica simple (control de dinero, cooldowns)
- Funciones de dibujo (fondo, cabecera, paneles)
"""

import pygame
import time
from config import *


# --- LÓGICA SIMPLE ---
def clamp_money(money):
    """
    Limita el dinero del jugador a un valor mínimo de 0.

    Args:
        money (float): Cantidad de dinero actual.

    Returns:
        float: Dinero corregido (0 si es negativo).
    """
    return max(0, money)


def can_earn(last_earn_time):
    """
    Indica si el jugador puede volver a ganar dinero tras el cooldown.

    Args:
        last_earn_time (float): Tiempo del último clic o ganancia.

    Returns:
        bool: True si ya pasó el tiempo de espera.
    """
    now = time.time()
    return now - last_earn_time >= EARN_COOLDOWN


# --- DIBUJO DE INTERFAZ ---
def draw_gradient_background(screen, width, height):
    """
    Dibuja un fondo degradado vertical con tonos beige.

    Args:
        screen (pygame.Surface): Superficie donde se dibuja.
        width (int): Ancho total del área de dibujo.
        height (int): Alto total del área de dibujo.
    """
    for y in range(height):
        color = (250 - y // 15, 240 - y // 20, 210 - y // 30)
        pygame.draw.line(screen, color, (0, y), (width, y))


def draw_header(screen, font_medium, font_small, player):
    """
    Dibuja la cabecera del juego con información del jugador.

    Muestra:
      - Dinero actual
      - Número total de clics
      - Ganancia por clic
      - Ganancia automática por segundo

    Args:
        screen (pygame.Surface): Superficie donde se dibuja.
        font_medium (pygame.font.Font): Fuente principal para el dinero.
        font_small (pygame.font.Font): Fuente para los textos secundarios.
        player (Player): Instancia del jugador con estadísticas actuales.
    """
    header_height = 60
    width, _ = screen.get_size()

    # --- Fondo degradado del encabezado ---
    for y in range(header_height):
        c = (180 + y // 3, 150 + y // 2, 100 + y // 3)
        pygame.draw.line(screen, c, (0, y), (width, y))

    # --- Textos ---
    money_text = font_medium.render(f"${int(player.money)}", True, (255, 255, 255))
    clicks_text = font_small.render(
        f"Clicks: {player.total_clicks}", True, (240, 240, 220)
    )
    income_text = font_small.render(
        f"+{player.click_income}/click", True, (240, 255, 200)
    )
    auto_text = font_small.render(f"+{player.auto_income:.1f}/s", True, (255, 240, 200))

    # --- Posiciones ---
    screen.blit(money_text, (20, 15))
    screen.blit(clicks_text, (300, 20))
    screen.blit(income_text, (600, 20))
    screen.blit(auto_text, (850, 20))


def draw_shop_panel(screen, panel_x, panel_y, panel_width, panel_h):
    """
    Dibuja el panel principal de la tienda con sombra y fondo beige.

    Args:
        screen (pygame.Surface): Superficie donde se dibuja.
        panel_x (int): Posición X del panel.
        panel_y (int): Posición Y del panel.
        panel_width (int): Ancho del panel.
        panel_h (int): Altura del panel.
    """
    # --- Sombra ---
    pygame.draw.rect(
        screen,
        (150, 130, 100, 50),
        (panel_x - 5, panel_y + 5, panel_width, panel_h),
        border_radius=15,
    )

    # --- Panel principal ---
    pygame.draw.rect(
        screen,
        (245, 240, 220),
        (panel_x, panel_y, panel_width, panel_h),
        border_radius=15,
    )
