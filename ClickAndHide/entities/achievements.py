"""
entities/achievements.py

Sistema de logros del juego Click & Hide.
Define las clases Achievements y AchievementNotification
para gestionar los logros desbloqueados y sus notificaciones visuales.
"""

import pygame
import time


# --- CLASE PRINCIPAL: GESTIÓN DE LOGROS ---
class Achievements:
    """
    Clase para gestionar los logros del jugador y sus notificaciones en pantalla.

    Atributos:
        achievements (list[dict]): Lista de logros disponibles con nombre, descripción, condición y estado.
        active_notifications (list[AchievementNotification]): Lista de notificaciones de logros activas.

    Métodos:
        update_achievements(state): Comprueba si se cumplen condiciones y desbloquea logros.
        manage_notifications(screen, font): Dibuja y gestiona las notificaciones activas.
    """

    def __init__(self):
        """Inicializa la lista de logros y la lista de notificaciones activas."""
        self.achievements = [
            {
                "name": "PRIMER CLICK",
                "desc": "Haz tu primer click.",
                "check": lambda s: s.get("total_clicks", 0) >= 1,
                "completed": False,
            },
            {
                "name": "AHORRADOR",
                "desc": "Alcanza $1,000.",
                "check": lambda s: s.get("money", 0) >= 1000,
                "completed": False,
            },
            {
                "name": "MILLONARIO",
                "desc": "Alcanza $1,000,000.",
                "check": lambda s: s.get("money", 0) >= 1_000_000,
                "completed": False,
            },
            {
                "name": "PRIMERA MEJORA",
                "desc": "Compra al menos una mejora.",
                "check": lambda s: s.get("upgrades_bought", 0) > 0,
                "completed": False,
            },
        ]
        self.active_notifications = []

    # --- ACTUALIZACIÓN DE LOGROS ---
    def update_achievements(self, state):
        """
        Comprueba el estado del juego y desbloquea logros nuevos.

        Args:
            state (dict): Estado actual del juego, con datos como dinero, clics y mejoras compradas.

        Si se cumple la condición de un logro aún no completado,
        lo marca como desbloqueado y genera una notificación visual.
        """
        for a in self.achievements:
            if not a["completed"] and a["check"](state):
                a["completed"] = True
                self.active_notifications.append(AchievementNotification(a))

    # --- GESTIÓN DE NOTIFICACIONES ---
    def manage_notifications(self, screen, font):
        """
        Actualiza y muestra todas las notificaciones activas en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibujan las notificaciones.
            font (pygame.font.Font): Fuente usada para renderizar el texto.

        Dibuja cada notificación, elimina las expiradas y mantiene las activas visibles.
        """
        for n in self.active_notifications[:]:
            n.draw_notification(screen, font)
            if not n.is_active_notification():
                self.active_notifications.remove(n)


# --- CLASE DE NOTIFICACIÓN DE LOGROS ---
class AchievementNotification:
    """
    Representa una notificación visual para un logro desbloqueado.

    Atributos:
        achievement (dict): Información del logro asociado.
        start_time (float): Tiempo en segundos en que se activó la notificación.
        duration (float): Duración total de la notificación en pantalla.
        slide_time (float): Duración de la animación de entrada/salida.

    Métodos:
        is_active_notification(): Indica si la notificación sigue activa.
        draw_notification(screen, font): Dibuja la notificación en pantalla.
    """

    def __init__(self, achievement):
        """
        Inicializa la notificación con tiempos de duración y animación.

        Args:
            achievement (dict): Diccionario con los datos del logro desbloqueado.
        """
        self.achievement = achievement
        self.start_time = time.time()
        self.duration = 3  # Duración total en segundos
        self.slide_time = 0.4  # Tiempo de animación de entrada/salida

    # --- ESTADO DE LA NOTIFICACIÓN ---
    def is_active_notification(self):
        """
        Indica si la notificación aún debe mostrarse en pantalla.

        Returns:
            bool: True si la notificación sigue activa; False si expiró.
        """
        return time.time() - self.start_time < self.duration

    # --- DIBUJO EN PANTALLA ---
    def draw_notification(self, screen, font):
        """
        Dibuja una notificación visual del logro en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se mostrará la notificación.
            font (pygame.font.Font): Fuente utilizada para renderizar el texto.

        Crea una animación deslizante desde la izquierda, con el nombre del logro
        y el texto "LOGRO DESBLOQUEADO!".
        """
        notif_width, notif_height = 300, 80
        elapsed = time.time() - self.start_time

        # --- Animación de entrada y salida ---
        if elapsed < self.slide_time:
            progress = elapsed / self.slide_time
            x = -notif_width + (progress * (notif_width + 30))
        elif elapsed < self.duration - self.slide_time:
            x = 20
        else:
            progress = (elapsed - (self.duration - self.slide_time)) / self.slide_time
            x = 20 - (progress * 50)

        y = screen.get_height() - notif_height - 20

        # --- Creación de superficie ---
        surf = pygame.Surface((notif_width, notif_height), pygame.SRCALPHA)
        pygame.draw.rect(
            surf, (40, 40, 40, 255), (0, 0, notif_width, notif_height), border_radius=10
        )
        pygame.draw.rect(
            surf,
            (255, 215, 0, 255),
            (0, 0, notif_width, notif_height),
            3,
            border_radius=10,
        )

        # --- Renderizado de texto ---
        title_surf = font.render("LOGRO DESBLOQUEADO!", True, (255, 255, 255))
        name_surf = font.render(self.achievement["name"], True, (200, 200, 200))
        surf.blit(title_surf, (10, 10))
        surf.blit(name_surf, (10, 40))

        # --- Mostrar en pantalla ---
        screen.blit(surf, (x, y))
