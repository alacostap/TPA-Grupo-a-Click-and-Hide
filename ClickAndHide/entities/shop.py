import pygame
from entities.shopitem import ShopItem
from utilities import draw_shop_panel  # <-- tu función para dibujar el panel

class Shop:
    def __init__(self):
        # Datos base de los items: nombre, costo, ingreso, tipo, color
        self.shop_data = [
            ("Ratón", 15, 1, "click", (230, 200, 150)),
            ("Apuntes (+1/s)", 50, 1, "auto", (245, 222, 100)),
            ("Libro (+5/s)", 100, 5, "auto", (230, 200, 150)),
            ("Pizarra (+10/s)", 200, 10, "auto", (230, 200, 150)),
            ("Móbil (+25/s)", 500, 25, "auto", (215, 190, 140)),
            ("Tablet (+50/s)", 1000, 50, "auto", (200, 180, 130)),
            ("Ordenador (+100/s)", 2500, 100, "auto", (220, 190, 140)),
            ("Fibra Óptica (+200/s)", 7500, 200, "auto", (240, 200, 150)),
            ("Servidor (+500/s)", 10000, 500, "auto", (230, 210, 160)),
        ]
        self.items = []
        self.scroll_offset = 0
        self.scroll_speed = 20
        self.max_scroll = 0
        self.dragging_slider = False
        self.slider_rect = None
        self.reset_items()

    # ---------- RESET ITEMS ----------
    def reset_items(self):
        """Inicializa o reinicia todos los ShopItem a sus valores base."""
        self.items = []
        for name, cost, inc, tipo, color in self.shop_data:
            item = ShopItem(name, cost, inc, tipo)
            item.color = color
            self.items.append(item)

    # ---------- HANDLE CLICK ----------
    def handle_click(self, mouse_pos, player):
        """Revisar si el usuario clicó un item y comprarlo si puede."""
        for item in self.items:
            if hasattr(item, 'rect') and item.rect.collidepoint(mouse_pos):
                if item.buy(player):
                    if item.tipo == "click":
                        player.click_income += item.base_income
                    else:
                        player.auto_income += item.base_income

    # ---------- HANDLE SCROLL ----------
    def handle_scroll(self, event):
        """Manejo del scroll con rueda del ratón."""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # ---------- HANDLE SLIDER DRAG ----------
    def handle_mouse_events(self, event, mouse_pos, panel_y, panel_h):
        """Maneja clic y arrastre del slider lateral."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect and self.slider_rect.collidepoint(mouse_pos):
                self.dragging_slider = True
                self.drag_start_y = mouse_pos[1]
                self.scroll_start_offset = self.scroll_offset

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_slider = False

        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            if self.max_scroll > 0:
                # Calcular cuánto se mueve en relación al panel visible
                slider_area_height = panel_h - 60
                slider_height = self.slider_rect.height
                delta_y = mouse_pos[1] - self.drag_start_y
                scroll_range = self.max_scroll
                slider_range = slider_area_height - slider_height
                self.scroll_offset = self.scroll_start_offset + (delta_y / slider_range) * scroll_range
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # ---------- DRAW SHOP ----------
    def draw(self, screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT):
        """Dibuja la tienda completa con slider lateral."""
        header_height = 60
        panel_width = 380
        panel_x, panel_y = WIDTH - panel_width, header_height
        panel_h = HEIGHT - header_height

        # Panel de fondo
        draw_shop_panel(screen, panel_x, panel_y, panel_width, panel_h)

        # Título
        title = font_big.render("TIENDA", True, (80, 60, 40))
        screen.blit(title, (panel_x + 100, header_height + 8))
        pygame.draw.line(screen, (90, 70, 40),
                         (panel_x + 30, header_height + 50),
                         (panel_x + panel_width - 30, header_height + 50), 2)

        # Altura total de todos los items
        item_height = 60
        spacing = 8
        total_height = len(self.items) * (item_height + spacing)
        self.max_scroll = max(0, total_height - (panel_h - 60))

        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

        # Dibujar items
        y_offset = header_height + 60 - self.scroll_offset
        for item in self.items:
            can_afford = player.can_afford(item.cost)
            rect = pygame.Rect(panel_x + 30, y_offset, panel_width - 60, item_height)
            color = item.color
            if not can_afford:
                color = tuple(max(130, c - 70) for c in color)
            elif rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 25) for c in color)

            # Dibujar solo si está visible
            if rect.bottom >= panel_y and rect.y <= panel_y + panel_h:
                pygame.draw.rect(screen, color, rect, border_radius=10)
                pygame.draw.rect(screen, (90, 70, 40), rect, 2, border_radius=10)
                screen.blit(font_small.render(item.name, True, (50, 35, 20)), (rect.x + 10, rect.y + 6))
                screen.blit(font_small.render(f"${item.cost}", True, (60, 45, 30)), (rect.x + 10, rect.y + 30))
                screen.blit(font_small.render(f"x{item.amount}", True, (50, 35, 20)), (rect.right - 50, rect.y + 18))

            item.rect = rect
            y_offset += item_height + spacing

        # Slider lateral (guarda su rect para detección)
        self.slider_rect = None
        if total_height > panel_h - 60:
            slider_height = max(40, (panel_h - 60) * (panel_h - 60) / total_height)
            slider_y = panel_y + 60 + (panel_h - 60 - slider_height) * self.scroll_offset / self.max_scroll
            self.slider_rect = pygame.Rect(panel_x + panel_width - 15, slider_y, 10, slider_height)
            pygame.draw.rect(screen, (150, 150, 150), self.slider_rect, border_radius=5)
            pygame.draw.rect(screen, (80, 80, 80), self.slider_rect, 2, border_radius=5)
