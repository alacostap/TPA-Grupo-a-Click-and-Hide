import pygame
import time
import os
from config import *
from entidades import Player
from utilidades import clamp_money
from upgrades import ShopItem
from intro import play_intro

# Menú y logros
from menu.menu import show_menu
from menu.logros import show_logros_panel, actualizar_logros, NotificacionLogro

pygame.init()

# ----------------- CONFIG -----------------
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CLICK AND HIDE - DEMO AUTOMÁTICA")
clock = pygame.time.Clock()
FPS = 60

# Fuentes
base_font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P.ttf")
font_small = pygame.font.Font(base_font_path, 14)
font_medium = pygame.font.Font(base_font_path, 18)
font_big = pygame.font.Font(base_font_path, 28)

# ----------------- GAME STATE -----------------
player = Player()
running = True
state = "menu"
game_started = False
auto_income = 0.0
click_income = 1.0
last_auto_time = time.time()
notificaciones = []

# ----------------- SHOP ITEMS -----------------
shop_data = [
    ("Cursor", 15, 1, "click", (245, 222, 100)),
    ("Abuela", 100, 1, "auto", (230, 200, 150)),
    ("Granja", 1100, 8, "auto", (215, 190, 140)),
    ("Fábrica", 12000, 47, "auto", (200, 180, 130)),
    ("Banco", 140000, 260, "auto", (220, 190, 140)),
    ("Templo", 2000000, 1400, "auto", (240, 200, 150)),
    ("Mina", 10000, 25, "auto", (230, 210, 160)),
    ("Ordenador", 50000, 80, "click", (250, 220, 160)),
    ("Portal", 1000000, 800, "auto", (245, 200, 150)),
]
shop_items = []
for name, cost, inc, tipo, color in shop_data:
    item = ShopItem(name, cost, inc, tipo)
    item.color = color
    shop_items.append(item)

# ----------------- INTRO -----------------
play_intro(screen, "inicio.png")

# ----------------- DEMO AUTOMÁTICA -----------------
demo_mode = True           # <--- Activar modo automático
demo_click_timer = 0
demo_buy_timer = 0
demo_start_time = time.time()
demo_duration = 60         # Duración total de la demo (segundos)

# ----------------- MAIN LOOP -----------------
hover_click = False

while running:
    dt = clock.tick(FPS) / 1000.0
    now = time.time()
    mouse_pos = pygame.mouse.get_pos()

    # ----------------- MENÚ -----------------
    if state == "menu":
        # En modo demo, saltar directamente al juego
        if demo_mode:
            state = "playing"
            player.money = MONEY_START
            player.total_clicks = 0
            auto_income = 0
            click_income = 1
            for item in shop_items:
                item.amount = 0
                item.cost = item.base_cost
            last_auto_time = time.time()
            game_started = True
        else:
            choice = show_menu(screen, font_small, font_big, game_started)
            if choice == "SALIR":
                running = False
                continue
            elif choice in ["JUGAR", "CONTINUAR"]:
                state = "playing"
                if not game_started:
                    player.money = MONEY_START
                    player.total_clicks = 0
                    auto_income = 0
                    click_income = 1
                    for item in shop_items:
                        item.amount = 0
                        item.cost = item.base_cost
                    last_auto_time = time.time()
                    game_started = True
        continue

    # ----------------- EVENTOS -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state = "menu"
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

        if not demo_mode and state == "playing" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if click_rect.collidepoint(mouse_pos):
                player.money += click_income
                player.total_clicks += 1

            for item in shop_items:
                if item.rect.collidepoint(mouse_pos):
                    if item.buy(player):
                        if item.tipo == "click":
                            click_income += item.base_income
                        else:
                            auto_income += item.base_income

    # ----------------- INTERFAZ DE JUEGO -----------------
    if state == "playing":
        # Fondo beige degradado
        for y in range(HEIGHT):
            color = (250 - y // 15, 240 - y // 20, 210 - y // 30)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        # Cabecera marrón clara con degradado
        header_height = 60
        for y in range(header_height):
            c = (180 + y // 3, 150 + y // 2, 100 + y // 3)
            pygame.draw.line(screen, c, (0, y), (WIDTH, y))

        # Textos cabecera
        money_text = font_medium.render(f"${int(player.money)}", True, (255, 255, 255))
        clicks_text = font_small.render(f"Clicks: {player.total_clicks}", True, (240, 240, 220))
        income_text = font_small.render(f"+{click_income}/click", True, (240, 255, 200))
        auto_text = font_small.render(f"+{auto_income:.1f}/s", True, (255, 240, 200))
        screen.blit(money_text, (20, 15))
        screen.blit(clicks_text, (300, 20))
        screen.blit(income_text, (600, 20))
        screen.blit(auto_text, (850, 20))

        # ----------------- BOTÓN CLICK -----------------
        square_size = 180
        click_rect = pygame.Rect(WIDTH // 2 - square_size // 2 - 180,
                                 HEIGHT // 2 - square_size // 2,
                                 square_size, square_size)

        if click_rect.collidepoint(mouse_pos):
            hover_click = True
            color_click = (235, 200, 120)  # hover dorado
        else:
            hover_click = False
            color_click = (225, 190, 110)  # beige suave

        pygame.draw.rect(screen, color_click, click_rect, border_radius=25)
        pygame.draw.rect(screen, (90, 70, 40), click_rect, 3, border_radius=25)
        click_label = font_medium.render("CLICK", True, (60, 40, 20))
        label_rect = click_label.get_rect(center=click_rect.center)
        screen.blit(click_label, label_rect)

        # ----------------- PANEL DERECHA (TIENDA) -----------------
        panel_width = 380
        panel_x = WIDTH - panel_width
        panel_y = header_height
        panel_h = HEIGHT - header_height

        shadow_rect = pygame.Rect(panel_x - 5, panel_y + 5, panel_width, panel_h)
        pygame.draw.rect(screen, (150, 130, 100, 50), shadow_rect, border_radius=15)
        pygame.draw.rect(screen, (245, 240, 220), (panel_x, panel_y, panel_width, panel_h), border_radius=15)

        # Título
        title = font_big.render("TIENDA", True, (80, 60, 40))
        screen.blit(title, (panel_x + 100, header_height + 8))
        pygame.draw.line(screen, (90, 70, 40),
                         (panel_x + 30, header_height + 50),
                         (panel_x + panel_width - 30, header_height + 50), 2)

        # Dibujar mejoras
        y_offset = header_height + 60
        item_height = 60
        for item in shop_items:
            can_afford = player.money >= item.cost
            rect = pygame.Rect(panel_x + 30, y_offset, panel_width - 60, item_height)

            base_color = item.color
            if not can_afford:
                base_color = tuple(max(130, c - 70) for c in base_color)
            elif rect.collidepoint(mouse_pos):
                base_color = tuple(min(255, c + 25) for c in base_color)

            pygame.draw.rect(screen, base_color, rect, border_radius=10)
            pygame.draw.rect(screen, (90, 70, 40), rect, 2, border_radius=10)

            name_text = font_small.render(item.name, True, (50, 35, 20))
            cost_text = font_small.render(f"${item.cost}", True, (60, 45, 30))
            qty_text = font_small.render(f"x{item.amount}", True, (50, 35, 20))

            screen.blit(name_text, (rect.x + 10, rect.y + 6))
            screen.blit(cost_text, (rect.x + 10, rect.y + 30))
            screen.blit(qty_text, (rect.right - 50, rect.y + 18))

            item.rect = rect
            y_offset += item_height + 8

        # ----------------- AUTO INCOME -----------------
        if now - last_auto_time >= 1:
            player.money += auto_income
            last_auto_time = now
        player.money = clamp_money(player.money)

        # ----------------- DEMO AUTOMÁTICA -----------------
        if demo_mode:
            demo_click_timer += dt
            if demo_click_timer >= 0.2:  # clic cada 0.2s
                demo_click_timer = 0
                player.money += click_income
                player.total_clicks += 1

            demo_buy_timer += dt
            if demo_buy_timer >= 1.5:  # intentar comprar cada 1.5s
                demo_buy_timer = 0
                affordable = [item for item in shop_items if player.money >= item.cost]
                if affordable:
                    item = min(affordable, key=lambda i: i.cost)
                    if item.buy(player):
                        if item.tipo == "click":
                            click_income += item.base_income
                        else:
                            auto_income += item.base_income

            # Finalizar demo tras duración
            if time.time() - demo_start_time > demo_duration:
                print("Demo finalizada automáticamente.")
                running = False

    pygame.display.flip()

pygame.quit()
