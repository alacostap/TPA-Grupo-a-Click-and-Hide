# menu/achievements_menu.py

import pygame
import time

# ----- NOTIFICACIÓN DE LOGRO -----
class AchievementNotification:
    def __init__(self, achievement):
        self.achievement = achievement
        self.start_time = time.time()
        self.duration = 3
        self.slide_time = 0.4

    def update(self):
        """Devuelve False si la notificación ya expiró"""
        return time.time() - self.start_time < self.duration

    def draw(self, screen, font):
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

# ----- CLASE DE LOGROS -----
class Achievements:
    def __init__(self):
        self.achievements = [
            {"name": "PRIMER CLICK", "desc": "Haz tu primer click.", "check": lambda s: s.get("total_clicks", 0) >= 1, "completed": False},
            {"name": "AHORRADOR", "desc": "Alcanza $1000.", "check": lambda s: s.get("money", 0) >= 100, "completed": False},
            {"name": "MILLONARIO", "desc": "Alcanza $1000000.", "check": lambda s: s.get("money", 0) >= 1000, "completed": False},
            {"name": "PRIMERA MEJORA", "desc": "Compra al menos 1 mejora.", "check": lambda s: s.get("upgrades_bought", 0) > 0, "completed": False},
        ]
        self.active_notifications = []

    def update(self, state):
        """Actualizar logros y generar notificaciones"""
        for ach in self.achievements:
            if not ach["completed"] and ach["check"](state):
                ach["completed"] = True
                self.active_notifications.append(AchievementNotification(ach))

    def draw_notifications(self, screen, font):
        """Dibujar las notificaciones activas"""
        for notif in self.active_notifications[:]:
            notif.draw(screen, font)
            if not notif.update():
                self.active_notifications.remove(notif)

    def show_panel(self, screen, state):
        """Panel flotante estilo About Us mostrando logros"""
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 24)
        big_font = pygame.font.SysFont(None, 32)

        panel_width = screen.get_width() * 0.7
        panel_height = screen.get_height() * 0.7
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = (screen.get_height() - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        close_rect = pygame.Rect(panel_rect.right - 40, panel_rect.top + 10, 30, 30)

        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and close_rect.collidepoint(event.pos):
                    running = False

            # Fondo semitransparente
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Panel beige
            pygame.draw.rect(screen, (210, 180, 140), panel_rect, border_radius=12)
            pygame.draw.rect(screen, (50, 50, 50), panel_rect, 3, border_radius=12)

            # Titulo
            title = big_font.render("LOGROS", True, (0, 0, 0))
            screen.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 15))

            # Botón cerrar
            pygame.draw.rect(screen, (220, 80, 80), close_rect, border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), close_rect, 2, border_radius=6)
            x_txt = font.render("X", True, (255, 255, 255))
            screen.blit(x_txt, (close_rect.centerx - x_txt.get_width() // 2, close_rect.centery - x_txt.get_height() // 2))

            # Listado de logros
            y = panel_rect.y + 60
            for ach in self.achievements:
                rect = pygame.Rect(panel_rect.x + 20, y, panel_width - 40, 40)
                color = (100, 220, 100) if ach["completed"] else (220, 100, 100)
                pygame.draw.rect(screen, color, rect, border_radius=6)
                pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=6)

                status = "COMPLETADO" if ach["completed"] else "NO COMPLETADO"
                text_surf = font.render(f"{ach['name']} - {status}", True, (0,0,0))
                screen.blit(text_surf, (rect.x + 10, rect.y + 8))

                y += 50

            pygame.display.flip()
