"""
menu/main_menu.py

Menú principal de Click & Hide.
Muestra opciones como JUGAR, OPCIONES, ABOUT US, LOGROS y SALIR,
y permite navegar entre submenús o iniciar/continuar la partida.
"""

import pygame
import os
from entities.achievements import Achievements
from menu.achievements_menu import show_achievements_panel
from menu.aboutus_menu import show_about_us_panel
from menu.options_menu import show_options_panel
from menu.exit_menu import show_exit_panel


# --- FUNCIÓN PRINCIPAL ---
def show_main_menu(screen, font, big_font, game_started, player, achievements_manager):
    """
    Muestra el menú principal y gestiona la interacción del usuario.

    Args:
        screen (pygame.Surface): Superficie principal donde se dibuja el menú.
        font (pygame.font.Font): Fuente base para los botones.
        big_font (pygame.font.Font): Fuente grande para el título.
        game_started (bool): Indica si la partida ya ha comenzado.
        player (Player): Instancia actual del jugador.
        achievements_manager (Achievements): Gestor de logros global.

    Returns:
        str | None: Opción seleccionada por el jugador (por ejemplo "JUGAR", "CONTINUAR" o "SALIR").

    Descripción:
        Este menú es la puerta de entrada principal del juego. Muestra las opciones disponibles
        dependiendo de si el jugador ya tiene una partida activa o no, y permite navegar hacia
        paneles secundarios como "Logros", "Opciones", "About Us" o el panel de salida.
    """

    # --- CONFIGURACIÓN INICIAL ---
    clock = pygame.time.Clock()
    running = True
    choice = None
    WIDTH, HEIGHT = screen.get_size()

    # --- PANEL IZQUIERDO ---
    panel_width = WIDTH // 3
    panel_color = (210, 180, 140, 180)
    panel_surf = pygame.Surface((panel_width, HEIGHT), pygame.SRCALPHA)
    panel_surf.fill(panel_color)

    # --- BOTONES DEL MENÚ ---
    if not game_started:
        button_texts = ["JUGAR", "OPCIONES", "ABOUT US", "LOGROS", "SALIR"]
    else:
        button_texts = ["CONTINUAR", "OPCIONES", "LOGROS", "SALIR"]

    button_height = 80
    button_margin = 20
    buttons = []
    start_y = 150
    for i, text in enumerate(button_texts):
        rect = pygame.Rect(
            20,
            start_y + i * (button_height + button_margin),
            panel_width - 40,
            button_height,
        )
        buttons.append((rect, text))

    # --- FONDO DEL MENÚ ---
    bg_image = None
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))
        bg_path = os.path.join(base_path, "assets", "images", "clase.png")
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.smoothscale(bg_image, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"[MENU] No se pudo cargar fondo: {e}")

    # --- TÍTULO DEL MENÚ ---
    title_text = "CLICK & HIDE"
    title_color = (255, 255, 255)
    base_font_path = os.path.join(
        os.path.dirname(__file__), "..", "assets", "fonts", "PressStart2P.ttf"
    )
    title_font = pygame.font.Font(base_font_path, 35)
    title_surf = title_font.render(title_text, True, title_color)
    title_rect = title_surf.get_rect(center=(panel_width // 2, 80))

    # --- BUCLE PRINCIPAL ---
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = "SALIR"
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for rect, text in buttons:
                    if rect.collidepoint(mx, my):
                        choice = text
                        running = False

        # --- DIBUJO DEL FONDO ---
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 50, 50))

        # --- DIBUJO DEL PANEL IZQUIERDO ---
        screen.blit(panel_surf, (0, 0))

        # --- DIBUJO DE LOS BOTONES ---
        mouse_pos = pygame.mouse.get_pos()
        for rect, text in buttons:
            color = (180, 140, 80) if rect.collidepoint(mouse_pos) else (160, 120, 60)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # --- DIBUJO DEL TÍTULO ---
        screen.blit(title_surf, title_rect)

        # --- ACTUALIZACIÓN DE PANTALLA ---
        pygame.display.flip()
        clock.tick(60)

    # --- ACCIONES SEGÚN BOTÓN ---
    if choice == "LOGROS":
        game_state = {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": getattr(player, "upgrades_bought", 0),
        }
        show_achievements_panel(screen, achievements_manager, game_state)
        return show_main_menu(
            screen, font, big_font, game_started, player, achievements_manager
        )

    elif choice == "OPCIONES":
        show_options_panel(screen)
        return show_main_menu(
            screen, font, big_font, game_started, player, achievements_manager
        )

    elif choice == "ABOUT US":
        show_about_us_panel(screen)
        return show_main_menu(
            screen, font, big_font, game_started, player, achievements_manager
        )

    elif choice == "SALIR":
        show_exit_panel(screen)
        return show_main_menu(
            screen, font, big_font, game_started, player, achievements_manager
        )

    return choice
