"""
achievements.py

Sistema de logros del juego Click & Hide.
Clase Achievements para gestionar logros y notificaciones.
"""

import pygame
import time


class Achievements:
    """Gestión de logros y sus notificaciones."""

    def __init__(self):
        """Inicializa logros y lista de notificaciones activas."""
        self.achievements = [
            {"name": "PRIMER CLICK", "desc": "Haz tu primer click.",
             "check": lambda s: s.get("total_clicks", 0) >= 1, "completed": False},
            {"name": "AHORRADOR", "desc": "Alcanza $1,000.",
             "check": lambda s: s.get("money", 0) >= 1000, "completed": False},
            {"name": "MILLONARIO", "desc": "Alcanza $1,000,000.",
             "check": lambda s: s.get("money", 0) >= 1_000_000, "completed": False},
            {"name": "PRIMERA MEJORA", "desc": "Compra al menos una mejora.",
             "check": lambda s: s.get("upgrades_bought", 0) > 0, "completed": False},
        ]
        self.active_notifications = []

    def update(self, state):
        """Comprueba logros desbloqueados y lanza notificaciones."""
        for ach in self.achievements:
            if not ach["completed"] and ach["check"](state):
                ach["completed"] = True
                self.active_notifications.append(AchievementNotification(ach))

    def draw_notifications(self, screen, font):
        """Dibuja notificaciones activas en pantalla."""
        for notif in self.active_notifications[:]:
            notif.draw(screen, font)
            if not notif.update():
                self.active_notifications.remove(notif)


class AchievementNotification:
    """Notificación emergente de logro."""

    def __init__(self, achievement):
        """Inicializa notificación con duración y animación."""
        self.achievement = achievement
        self.start_time = time.time()
        self.duration = 3
        self.slide_time = 0.4

    def update(self):
        """Actualiza duración de la notificación. Devuelve False si expira."""
        return time.time() - self.start_time < self.duration

    def draw(self, screen, font):
        """Dibuja notificación con animación deslizante."""
        notif_width, notif_height = 300, 80
        elapsed = time.time() - self.start_time

        if elapsed < self.slide_time:
            progress = elapsed / self.slide_time
            x = -notif_width + (progress * (notif_width + 30))
        elif elapsed < self.duration - self.slide_time:
            x = 20
        else:
            progress = (elapsed - (self.duration - self.slide_time)) / self.slide_time
            x = 20 - (progress * 50)

        y = screen.get_height() - notif_height - 20

        surf = pygame.Surface((notif_width, notif_height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (40, 40, 40, 255), (0, 0, notif_width, notif_height), border_radius=10)
        pygame.draw.rect(surf, (255, 215, 0, 255), (0, 0, notif_width, notif_height), 3, border_radius=10)

        title_surf = font.render("LOGRO DESBLOQUEADO!", True, (255, 255, 255))
        name_surf = font.render(self.achievement["name"], True, (200, 200, 200))
        surf.blit(title_surf, (10, 10))
        surf.blit(name_surf, (10, 40))

        screen.blit(surf, (x, y))
