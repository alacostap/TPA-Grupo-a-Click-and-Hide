import pygame
import os
from menu.achievements_menu import AchievementsMenu
from menu.aboutus_menu import show_about_us_panel
from menu.options_menu import show_options_panel
from menu.exit_menu import show_exit_panel


def show_main_menu(screen, font, big_font, game_started, player, achievements_manager):
    clock = pygame.time.Clock()
    running = True
    choice = None

    WIDTH, HEIGHT = screen.get_size()

    # ----- PANEL IZQUIERDO -----
    panel_width = WIDTH // 3
    panel_color = (210, 180, 140, 180)
    panel_surf = pygame.Surface((panel_width, HEIGHT), pygame.SRCALPHA)
    panel_surf.fill(panel_color)

    # ----- BOTONES -----
    if not game_started:
        button_texts = ["JUGAR", "OPCIONES", "ABOUT US", "LOGROS", "SALIR"]
    else:
        button_texts = ["CONTINUAR", "OPCIONES", "LOGROS", "SALIR"]

    button_height = 80
    button_margin = 20
    buttons = []
    start_y = 150
    for i, text in enumerate(button_texts):
        rect = pygame.Rect(20, start_y + i * (button_height + button_margin), panel_width - 40, button_height)
        buttons.append((rect, text))

    # ----- FONDO -----
    bg_image = None
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))
        bg_path = os.path.join(base_path, "assets", "images", "clase.png")
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.smoothscale(bg_image, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"[MENU] No se pudo cargar fondo: {e}")

    # ----- TÍTULO -----
    title_text = "CLICK & HIDE"
    title_color = (255, 255, 255)
    base_font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "PressStart2P.ttf")
    title_font = pygame.font.Font(base_font_path, 35)
    title_surf = title_font.render(title_text, True, title_color)
    title_rect = title_surf.get_rect(center=(panel_width // 2, 80))

    # ----- LOOP DEL MENÚ -----
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

        # ----- DIBUJAR FONDO -----
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 50, 50))

        # ----- DIBUJAR PANEL IZQUIERDO -----
        screen.blit(panel_surf, (0, 0))

        # ----- DIBUJAR BOTONES -----
        mouse_pos = pygame.mouse.get_pos()
        for rect, text in buttons:
            color = (180, 140, 80) if rect.collidepoint(mouse_pos) else (160, 120, 60)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # ----- DIBUJAR TÍTULO -----
        screen.blit(title_surf, title_rect)

        pygame.display.flip()
        clock.tick(60)

    # ----- ACCIONES SEGÚN BOTÓN -----
    if choice == "LOGROS":
        game_state = {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "upgrades_bought": getattr(player, "upgrades_bought", 0)
        }
        achievements_manager.show_panel(screen, game_state)
        # volver al menú después de cerrar el panel
        return show_main_menu(screen, font, big_font, game_started, player, achievements_manager)

    elif choice == "OPCIONES":
        show_options_panel(screen)
        return show_main_menu(screen, font, big_font, game_started, player, achievements_manager)

    elif choice == "ABOUT US":
        show_about_us_panel(screen)
        return show_main_menu(screen, font, big_font, game_started, player, achievements_manager)

    elif choice == "SALIR":
        show_exit_panel(screen)
        # Si el usuario cancela salida, regresa al menú
        return show_main_menu(screen, font, big_font, game_started, player, achievements_manager)

    return choice
