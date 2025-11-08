"""
menu/aboutus_menu.py

Panel emergente "About Us" del juego Click & Hide.
Muestra información sobre los desarrolladores, el motor del juego y el año.
"""

import pygame


# --- FUNCIÓN PRINCIPAL ---
def show_about_us_panel(screen):
    """
    Muestra un panel emergente con información sobre los desarrolladores.

    Args:
        screen (pygame.Surface): Superficie principal del juego donde se dibuja el panel.

    Descripción:
        Este panel aparece centrado en la pantalla, con un diseño limpio y un botón de cierre.
        Incluye texto sobre los autores, el motor de desarrollo (Python + Pygame) y derechos reservados.

    Controles:
        - **ESC**: Cierra el panel.
        - **Click en X**: Cierra el panel.
    """
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 36)

    # --- PANEL CENTRADO ---
    panel_width = screen.get_width() * 0.7
    panel_height = screen.get_height() * 0.7
    panel_x = (screen.get_width() - panel_width) // 2
    panel_y = (screen.get_height() - panel_height) // 2
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    # --- BOTÓN DE CIERRE (X) ---
    close_rect = pygame.Rect(panel_rect.right - 40, panel_rect.top + 10, 30, 30)

    # --- TEXTO DEL PANEL ---
    text_lines = [
        "ClickAndHide is a game developed by Group A.",
        "Classic clicker game with events.",
        "",
        "Developed with Python + Pygame.",
        "© 2025 All rights reserved.",
    ]

    # --- BUCLE PRINCIPAL DEL PANEL ---
    running = True
    while running:
        clock.tick(60)

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and close_rect.collidepoint(
                event.pos
            ):
                running = False

        # --- FONDO SEMITRANSPARENTE ---
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        screen.blit(overlay, (0, 0))

        # --- PANEL PRINCIPAL ---
        pygame.draw.rect(screen, (255, 240, 180), panel_rect, border_radius=12)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect, 3, border_radius=12)

        # --- TÍTULO ---
        title = big_font.render("ABOUT US", True, (0, 0, 0))
        screen.blit(
            title, (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 15)
        )

        # --- BOTÓN DE CIERRE ---
        pygame.draw.rect(screen, (220, 80, 80), close_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), close_rect, 2, border_radius=6)
        x_txt = font.render("X", True, (255, 255, 255))
        screen.blit(
            x_txt,
            (
                close_rect.centerx - x_txt.get_width() // 2,
                close_rect.centery - x_txt.get_height() // 2,
            ),
        )

        # --- TEXTO INFORMATIVO ---
        y = panel_rect.y + 80
        for line in text_lines:
            txt_surf = font.render(line, True, (0, 0, 0))
            screen.blit(txt_surf, (panel_rect.centerx - txt_surf.get_width() // 2, y))
            y += txt_surf.get_height() + 10

        # --- ACTUALIZACIÓN DE PANTALLA ---
        pygame.display.flip()
