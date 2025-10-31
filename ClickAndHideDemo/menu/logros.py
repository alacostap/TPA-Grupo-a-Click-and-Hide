import pygame
import time

# ======================== CLASE LOGRO ==========================
class Logro:
    def __init__(self, nombre, descripcion, requisito_func):
        self.nombre = nombre
        self.descripcion = descripcion
        self.requisito_func = requisito_func
        self.completado = False

    def draw(self, surface, font, rect, estado):
        """
        Dibuja el logro en pantalla.
        estado: diccionario con valores actuales (money, upgrades, etc.)
        """
        # Color según completado (usa self.completado, no recalcules)
        bg_color = (160, 230, 160) if self.completado else (235, 235, 200)
        pygame.draw.rect(surface, bg_color, rect, border_radius=8)
        pygame.draw.rect(surface, (50, 50, 50), rect, 2, border_radius=8)

        # Nombre del logro
        txt = font.render(self.nombre, True, (0, 0, 0))
        surface.blit(txt, (rect.x + 10, rect.y + rect.height // 2 - txt.get_height() // 2))

        # Icono de completado
        icon_font = pygame.font.SysFont(None, 28)
        icon_text = "✔" if self.completado else "✖"
        icon_color = (0, 150, 0) if self.completado else (150, 0, 0)
        icon_surf = icon_font.render(icon_text, True, icon_color)
        surface.blit(icon_surf, (rect.right - 30, rect.y + rect.height // 2 - icon_surf.get_height() // 2))

        # Tooltip si el ratón pasa por encima
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            status_text = "¡COMPLETADO!" if self.completado else "SIN CONSEGUIR"
            mostrar_tooltip(surface, font, status_text + "\n" + self.descripcion,
                            mouse_pos, status_color=(0, 200, 0) if self.completado else (200, 0, 0))


# ======================== TOOLTIP ==========================
def mostrar_tooltip(surface, font, texto, pos, status_color=(255, 255, 255)):
    lines = texto.split("\n")
    rendered = [font.render(line, True, status_color if i==0 else (255, 255, 255)) for i, line in enumerate(lines)]
    max_w = max(r.get_width() for r in rendered)
    total_h = sum(r.get_height() for r in rendered) + (len(lines) - 1) * 4

    tooltip_rect = pygame.Rect(pos[0] + 10, pos[1] + 10, max_w + 20, total_h + 10)

    # Evitar que se salga de la pantalla
    tooltip_rect.right = min(tooltip_rect.right, surface.get_width() - 10)
    tooltip_rect.bottom = min(tooltip_rect.bottom, surface.get_height() - 10)

    pygame.draw.rect(surface, (0, 0, 0, 180), tooltip_rect)
    pygame.draw.rect(surface, (255, 255, 255), tooltip_rect, 2)

    y = tooltip_rect.y + 5
    for r in rendered:
        surface.blit(r, (tooltip_rect.x + 10, y))
        y += r.get_height() + 4


# ======================== LISTA DE LOGROS ==========================
logros = [
    Logro("Primer Click", "Haz tu primer click.", lambda estado: estado.get("money", 0) >= 1),
    Logro("Ahorros", "Alcanza $100.", lambda estado: estado.get("money", 0) >= 100),
    Logro("Millonario", "Alcanza $1000.", lambda estado: estado.get("money", 0) >= 1000),
    Logro("Mejoras Pro", "Compra al menos 1 mejora.", lambda estado: estado.get("upgrades_compra", 0) > 0),
]


# ======================== NOTIFICACIÓN DE LOGROS ==========================
class NotificacionLogro:
    def __init__(self, logro):
        self.logro = logro
        self.start_time = time.time()
        self.duration = 3  # segundos visibles
        self.slide_time = 0.4  # tiempo de animación entrada/salida

    def update(self, dt=None):
        elapsed = time.time() - self.start_time
        return elapsed < self.duration

    def draw(self, screen, font):
        big_font = pygame.font.SysFont(None, 32)
        notif_width = 300
        notif_height = 80

        target_x = screen.get_width() - notif_width - 20
        target_y = screen.get_height() - notif_height - 20
        elapsed = time.time() - self.start_time

        if elapsed < self.slide_time:
            progress = elapsed / self.slide_time
            x = screen.get_width() + 10 - (progress * (notif_width + 30))
            alpha = 255
        elif elapsed < self.duration - self.slide_time:
            x = target_x
            alpha = 255
        else:
            progress = (elapsed - (self.duration - self.slide_time)) / self.slide_time
            x = target_x - (progress * 50)
            alpha = int(255 * (1 - progress))

        y = target_y

        surf = pygame.Surface((notif_width, notif_height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (40, 40, 40, alpha), (0, 0, notif_width, notif_height), border_radius=10)
        pygame.draw.rect(surf, (255, 215, 0, alpha), (0, 0, notif_width, notif_height), 3, border_radius=10)

        title_surf = big_font.render("¡LOGRO CONSEGUIDO!", True, (255, 255, 255))
        name_surf = font.render(self.logro.nombre, True, (200, 200, 200))

        title_surf.set_alpha(alpha)
        name_surf.set_alpha(alpha)

        surf.blit(title_surf, (notif_width // 2 - title_surf.get_width() // 2, 10))
        surf.blit(name_surf, (notif_width // 2 - name_surf.get_width() // 2, 45))

        screen.blit(surf, (x, y))


# ======================== ACTUALIZACIÓN DE LOGROS ==========================
def actualizar_logros(estado):
    """
    Marca los logros completados y devuelve los nuevos logros conseguidos
    """
    if not isinstance(estado, dict):
        estado = {
            "money": getattr(estado, "money", 0),
            "upgrades_compra": getattr(estado, "upgrades_compra", 0),
        }

    nuevos = []
    for logro in logros:
        if not logro.completado and logro.requisito_func(estado):
            logro.completado = True
            nuevos.append(logro)
    return nuevos


# ======================== PANEL DE LOGROS FLOTANTE ==========================
def show_logros_panel(screen, estado):
    if not isinstance(estado, dict):
        estado = {
            "money": getattr(estado, "money", 0),
            "upgrades_compra": getattr(estado, "upgrades_compra", 0),
        }

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 36)

    scroll_offset = 0
    logro_height = 50
    spacing = 10
    content_height = len(logros) * (logro_height + spacing)

    panel_width = screen.get_width() * 0.7
    panel_height = screen.get_height() * 0.7
    panel_x = (screen.get_width() - panel_width) // 2
    panel_y = (screen.get_height() - panel_height) // 2
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    close_rect = pygame.Rect(panel_rect.right - 40, panel_rect.top + 10, 30, 30)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_offset = min(scroll_offset + 30, 0)
                elif event.button == 5:
                    max_scroll = min(0, panel_height - content_height - 60)
                    scroll_offset = max(scroll_offset - 30, max_scroll)
                elif close_rect.collidepoint(event.pos):
                    running = False

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (255, 240, 180), panel_rect, border_radius=12)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect, 3, border_radius=12)

        title = big_font.render("LOGROS", True, (0, 0, 0))
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 15))

        pygame.draw.rect(screen, (220, 80, 80), close_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), close_rect, 2, border_radius=6)
        x_txt = font.render("X", True, (255, 255, 255))
        screen.blit(x_txt, (close_rect.centerx - x_txt.get_width() // 2, close_rect.centery - x_txt.get_height() // 2))

        clip_rect = pygame.Rect(panel_x + 20, panel_y + 60, panel_width - 40, panel_height - 80)
        screen.set_clip(clip_rect)

        y = clip_rect.y + scroll_offset
        for logro in logros:
            logro_rect = pygame.Rect(clip_rect.x, y, clip_rect.width, logro_height)
            logro.draw(screen, font, logro_rect, estado)
            y += logro_height + spacing

        screen.set_clip(None)
        pygame.display.flip()
