import pygame
import os
from menu.logros import show_logros_panel
from menu.aboutus import show_aboutus_panel
from menu.opciones import show_opciones_panel
from menu.salir import show_salir_panel

def show_menu(screen, font, big_font, game_started):
    clock = pygame.time.Clock()
    running = True
    choice = None

    WIDTH, HEIGHT = screen.get_size()

    # ----------------- PANEL IZQUIERDO -----------------
    panel_width = WIDTH // 3
    panel_color = (210, 180, 140, 180)  # beige con transparencia
    panel_surf = pygame.Surface((panel_width, HEIGHT), pygame.SRCALPHA)
    panel_surf.fill(panel_color)

    # ----------------- BOTONES -----------------
    button_texts = []

    # Mostrar botones según el estado del juego
    if not game_started:
        button_texts.append("JUGAR")
        button_texts.append("OPCIONES")
        button_texts.append("SOBRE NOSOTROS")
        button_texts.append("LOGROS")
        button_texts.append("SALIR")
    else:
        button_texts.append("CONTINUAR")
        button_texts.append("OPCIONES")
        button_texts.append("LOGROS")
        button_texts.append("SALIR")

    button_height = 80
    button_margin = 20
    buttons = []
    start_y = 150

    for i, text in enumerate(button_texts):
        rect = pygame.Rect(20, start_y + i * (button_height + button_margin), panel_width - 40, button_height)
        buttons.append((rect, text))

    # ----------------- IMAGEN DE FONDO -----------------
    bg_image = None
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))
        bg_path = os.path.join(base_path, "assets", "imagenes", "inicio.png")
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.smoothscale(bg_image, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"[MENU] No se pudo cargar la imagen de fondo: {e}")

    # ----------------- TÍTULO -----------------
    title_text = "CLICK & HIDE"
    title_color = (255, 255, 255)
    base_font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "PressStart2P.ttf")
    title_font = pygame.font.Font(base_font_path, 35)
    title_surf = title_font.render(title_text, True, title_color)
    title_rect = title_surf.get_rect(center=(panel_width // 2, 80))

    # ----------------- LOOP MENÚ -----------------
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

        # Fondo general
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 50, 50))

        # Panel izquierdo
        screen.blit(panel_surf, (0, 0))

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for rect, text in buttons:
            color = (180, 140, 80) if rect.collidepoint(mouse_pos) else (160, 120, 60)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # Título
        screen.blit(title_surf, title_rect)

        pygame.display.flip()
        clock.tick(60)

    # ----------------- ACCIONES DE BOTONES -----------------
    if choice == "LOGROS":
        show_logros_panel(screen, {"money": 0, "upgrades_compra": 0})
        return show_menu(screen, font, big_font, game_started)

    elif choice == "OPCIONES":
        show_opciones_panel(screen)
        return show_menu(screen, font, big_font, game_started)

    elif choice == "SOBRE NOSOTROS":
        # Solo aparece si game_started es False, de todas formas aquí lo dejamos
        show_aboutus_panel(screen)
        return show_menu(screen, font, big_font, game_started)

    elif choice == "SALIR":
        show_salir_panel(screen)
        return show_menu(screen, font, big_font, game_started)

    # Para JUGAR o CONTINUAR, devolvemos la opción
    return choice
