"""
entities/shop.py

Clases relacionadas con la tienda para Click & Hide.
Gestiona la tienda, los ítems, las compras, el scroll y el deslizador lateral.
"""

import pygame
from auxiliary import draw_shop_panel


# --- CLASE BASE: SHOPITEM ---
class ShopItem:
    """
    Representa un ítem individual dentro de la tienda.

    Atributos:
        name (str): Nombre del ítem.
        cost (int): Costo actual del ítem.
        base_income (int): Incremento base de ingresos que aporta el ítem.
        tipo (str): Tipo de ítem ('click' o 'auto').
        amount (int): Cantidad de unidades compradas.
        color (tuple): Color RGB asociado al ítem.
        rect (pygame.Rect): Rectángulo de interacción en pantalla.
    """

    def __init__(self, name, cost, income, tipo, color):
        """Inicializa un ítem con sus atributos básicos."""
        self.name = name
        self.cost = cost
        self.base_income = income
        self.tipo = tipo
        self.amount = 0
        self.color = color
        self.rect = None


# --- FÁBRICA DE ÍTEMS ---
class ShopItemFactory:
    """
    Crea instancias de ítems de la tienda mediante un método de fábrica.
    Actualmente todos los ítems son de tipo ShopItem, pero este patrón permite
    ampliar el sistema con otros tipos en el futuro (por ejemplo, ítems especiales).
    """

    @staticmethod
    def create_item(name, cost, income, tipo, color):
        """
        Crea un nuevo ítem de la tienda.

        Args:
            name (str): Nombre del ítem.
            cost (int): Precio inicial del ítem.
            income (int): Ingreso que genera el ítem.
            tipo (str): Tipo ('click' o 'auto').
            color (tuple): Color RGB.

        Returns:
            ShopItem: Nueva instancia de ítem creada.
        """
        return ShopItem(name, cost, income, tipo, color)


# --- CLASE PRINCIPAL: SHOP ---
class Shop:
    """
    Representa la tienda del juego y gestiona la lógica de interacción.

    Atributos:
        shop_data (list): Datos base de los ítems disponibles.
        items (list[ShopItem]): Lista de ítems creados.
        scroll_offset (int): Desplazamiento actual del scroll.
        scroll_speed (int): Velocidad de desplazamiento.
        max_scroll (int): Máximo desplazamiento posible.
        dragging_slider (bool): Indica si el deslizador está siendo arrastrado.
        slider_rect (pygame.Rect): Área del deslizador lateral.
    """

    def __init__(self):
        """Inicializa la tienda con ítems base y parámetros de scroll."""
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
        self.init_items()

        self.scroll_offset = 0
        self.scroll_speed = 20
        self.max_scroll = 0
        self.dragging_slider = False
        self.slider_rect = None

    # --- INICIALIZACIÓN ---
    def init_items(self):
        """Crea o reinicia todos los ítems usando la clase fábrica."""
        self.items = []
        for name, cost, income, tipo, color in self.shop_data:
            item = ShopItemFactory.create_item(name, cost, income, tipo, color)
            self.items.append(item)

    # --- GESTIÓN DE CLICS / COMPRAS ---
    def handle_click(self, mouse_pos, player, achievements_manager=None):
        """
        Gestiona las compras cuando el jugador hace clic sobre un ítem.

        Args:
            mouse_pos (tuple[int, int]): Posición actual del ratón.
            player (Player): Instancia del jugador.
            achievements_manager (Achievements, opcional): Sistema de logros.

        Efectos:
            - Resta dinero al jugador al comprar.
            - Aumenta la cantidad del ítem.
            - Incrementa el ingreso del jugador.
            - Actualiza los logros si aplica.
        """
        for item in self.items:
            if item.rect and item.rect.collidepoint(mouse_pos):
                if player.money >= item.cost:
                    player.money -= item.cost
                    item.amount += 1
                    item.cost = int(item.cost * 1.15)

                    if item.tipo == "click":
                        player.click_income += item.base_income
                    else:
                        player.auto_income += item.base_income

                    if not hasattr(player, "upgrades_bought"):
                        player.upgrades_bought = 0
                    player.upgrades_bought += 1

                    if achievements_manager:
                        game_state = {
                            "money": player.money,
                            "total_clicks": player.total_clicks,
                            "upgrades_bought": player.upgrades_bought,
                        }
                        achievements_manager.update_achievements(game_state)

    # --- CONTROL DE SCROLL ---
    def handle_scroll(self, event):
        """
        Maneja el desplazamiento vertical con la rueda del ratón.

        Args:
            event (pygame.event.Event): Evento de Pygame del tipo MOUSEWHEEL.
        """
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # --- CONTROL DEL DESLIZADOR ---
    def handle_mouse_events(self, event, mouse_pos, panel_y, panel_h):
        """
        Controla el comportamiento del deslizador lateral para hacer scroll manual.

        Args:
            event (pygame.event.Event): Evento de Pygame.
            mouse_pos (tuple[int, int]): Posición actual del ratón.
            panel_y (int): Posición vertical del panel.
            panel_h (int): Altura del panel de la tienda.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect and self.slider_rect.collidepoint(mouse_pos):
                self.dragging_slider = True
                self.drag_start_y = mouse_pos[1]
                self.scroll_start_offset = self.scroll_offset
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_slider = False
        elif (
            event.type == pygame.MOUSEMOTION
            and self.dragging_slider
            and self.max_scroll > 0
        ):
            slider_area_height = panel_h - 60
            slider_height = self.slider_rect.height
            delta_y = mouse_pos[1] - self.drag_start_y
            scroll_range = self.max_scroll
            slider_range = slider_area_height - slider_height
            self.scroll_offset = (
                self.scroll_start_offset + (delta_y / slider_range) * scroll_range
            )
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # --- DIBUJO DE LA TIENDA ---
    def draw(self, screen, font_small, font_big, player, mouse_pos, WIDTH, HEIGHT):
        """
        Dibuja la tienda completa con su panel, ítems y deslizador lateral.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja.
            font_small (pygame.font.Font): Fuente pequeña para texto.
            font_big (pygame.font.Font): Fuente grande para el título.
            player (Player): Instancia del jugador para comprobar dinero.
            mouse_pos (tuple[int, int]): Posición del ratón.
            WIDTH (int): Ancho de la ventana.
            HEIGHT (int): Alto de la ventana.
        """
        header_height = 60
        panel_width = 380
        panel_x, panel_y = WIDTH - panel_width, header_height
        panel_h = HEIGHT - header_height

        draw_shop_panel(screen, panel_x, panel_y, panel_width, panel_h)

        title = font_big.render("TIENDA", True, (80, 60, 40))
        screen.blit(title, (panel_x + 100, header_height + 8))
        pygame.draw.line(
            screen,
            (90, 70, 40),
            (panel_x + 30, header_height + 50),
            (panel_x + panel_width - 30, header_height + 50),
            2,
        )

        item_height, spacing = 60, 8
        total_height = len(self.items) * (item_height + spacing)
        self.max_scroll = max(0, total_height - (panel_h - 60))
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

        y_offset = header_height + 60 - self.scroll_offset
        for item in self.items:
            can_afford = player.can_afford(item.cost)
            rect = pygame.Rect(panel_x + 30, y_offset, panel_width - 60, item_height)
            color = item.color
            if not can_afford:
                color = tuple(max(130, c - 70) for c in color)
            elif rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 25) for c in color)

            if rect.bottom >= panel_y and rect.y <= panel_y + panel_h:
                pygame.draw.rect(screen, color, rect, border_radius=10)
                pygame.draw.rect(screen, (90, 70, 40), rect, 2, border_radius=10)
                screen.blit(
                    font_small.render(item.name, True, (50, 35, 20)),
                    (rect.x + 10, rect.y + 6),
                )
                screen.blit(
                    font_small.render(f"${item.cost}", True, (60, 45, 30)),
                    (rect.x + 10, rect.y + 30),
                )
                screen.blit(
                    font_small.render(f"x{item.amount}", True, (50, 35, 20)),
                    (rect.right - 50, rect.y + 18),
                )

            item.rect = rect
            y_offset += item_height + spacing

        # --- DESLIZADOR LATERAL ---
        self.slider_rect = None
        if total_height > panel_h - 60:
            slider_height = max(40, (panel_h - 60) * (panel_h - 60) / total_height)
            slider_y = (
                panel_y
                + 60
                + (panel_h - 60 - slider_height) * self.scroll_offset / self.max_scroll
            )
            self.slider_rect = pygame.Rect(
                panel_x + panel_width - 15, slider_y, 10, slider_height
            )
            pygame.draw.rect(screen, (150, 150, 150), self.slider_rect, border_radius=5)
            pygame.draw.rect(screen, (80, 80, 80), self.slider_rect, 2, border_radius=5)
