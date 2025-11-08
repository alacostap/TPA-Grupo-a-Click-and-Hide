"""
entities/player.py

Define la clase Player del juego Click & Hide.
Gestiona el dinero, los ingresos por clic y automáticos,
así como el dibujo del botón de clic principal.
"""

import time
import pygame
from config import MONEY_START, EARN_COOLDOWN
from auxiliary import clamp_money, can_earn


# --- CLASE PRINCIPAL: PLAYER ---
class Player:
    """
    Representa al jugador y su progreso dentro del juego.

    Atributos:
        money (int): Dinero actual del jugador.
        total_clicks (int): Número total de clics realizados.
        click_income (int): Dinero ganado por cada clic manual.
        auto_income (int): Dinero ganado automáticamente por segundo.
        last_auto_time (float): Marca de tiempo del último ingreso automático.
        last_click_time (float): Marca de tiempo del último clic.

    Métodos:
        reset(money): Reinicia los valores del jugador.
        click(): Agrega dinero al jugador por clic, si no hay cooldown activo.
        apply_auto_income(now): Aplica ingresos automáticos cada segundo.
        can_afford(amount): Devuelve True si el jugador tiene dinero suficiente.
        draw_click_button(screen, font, mouse_pos, WIDTH, HEIGHT): Dibuja el botón de clic.
    """

    def __init__(self):
        """Inicializa al jugador con valores por defecto."""
        self.money = MONEY_START
        self.total_clicks = 0
        self.click_income = 1
        self.auto_income = 0
        self.last_auto_time = time.time()
        self.last_click_time = time.time()

    # --- REINICIO DEL JUGADOR ---
    def reset(self, money=MONEY_START):
        """
        Reinicia el jugador a su estado inicial.

        Args:
            money (int): Cantidad de dinero inicial (por defecto, MONEY_START).
        """
        self.money = money
        self.total_clicks = 0
        self.click_income = 1
        self.auto_income = 0
        self.last_auto_time = time.time()
        self.last_click_time = time.time()

    # --- CLIC MANUAL ---
    def click(self):
        """
        Ejecuta un clic del jugador y agrega dinero si pasó el cooldown.

        Usa la función auxiliar 'can_earn' para verificar si puede ganar dinero
        según el tiempo transcurrido desde el último clic.
        """
        if can_earn(self.last_click_time):
            self.money += self.click_income
            self.total_clicks += 1
            self.last_click_time = time.time()
            self.money = clamp_money(self.money)

    # --- INGRESO AUTOMÁTICO ---
    def apply_auto_income(self, now=None):
        """
        Aplica el ingreso automático cada segundo.

        Args:
            now (float, opcional): Tiempo actual. Si no se pasa, se usa time.time().
        """
        now = now or time.time()
        if now - self.last_auto_time >= 1:
            self.money += self.auto_income
            self.last_auto_time = now
            self.money = clamp_money(self.money)

    # --- VERIFICACIÓN DE COMPRA ---
    def can_afford(self, amount):
        """
        Comprueba si el jugador tiene suficiente dinero para una compra.

        Args:
            amount (int): Precio o cantidad a comprobar.

        Returns:
            bool: True si el jugador tiene al menos esa cantidad de dinero.
        """
        return self.money >= amount

    # --- DIBUJO DEL BOTÓN DE CLIC ---
    def draw_click_button(self, screen, font, mouse_pos, WIDTH, HEIGHT):
        """
        Dibuja el botón central del clic en la pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja el botón.
            font (pygame.font.Font): Fuente utilizada para el texto del botón.
            mouse_pos (tuple[int, int]): Posición actual del ratón.
            WIDTH (int): Ancho de la ventana del juego.
            HEIGHT (int): Alto de la ventana del juego.

        El botón cambia de color al pasar el cursor sobre él,
        y su área se guarda en 'self.click_rect' para detectar clics.
        """
        square_size = 180
        self.click_rect = pygame.Rect(
            WIDTH // 2 - square_size // 2 - 180,
            HEIGHT // 2 - square_size // 2,
            square_size,
            square_size,
        )

        color_click = (
            (235, 200, 120)
            if self.click_rect.collidepoint(mouse_pos)
            else (225, 190, 110)
        )

        pygame.draw.rect(screen, color_click, self.click_rect, border_radius=25)
        pygame.draw.rect(screen, (90, 70, 40), self.click_rect, 3, border_radius=25)

        label_surface = font.render("CLICK", True, (60, 40, 20))
        label_rect = label_surface.get_rect(center=self.click_rect.center)
        screen.blit(label_surface, label_rect)
