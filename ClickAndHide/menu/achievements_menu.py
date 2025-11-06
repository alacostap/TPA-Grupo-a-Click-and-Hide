# menu/achievements_panel.py

import pygame

def show_achievements_panel(screen, achievements, state):
    """
    Muestra el panel de logros del jugador.

    Args:
        screen (pygame.Surface): Ventana donde se dibuja el panel.
        achievements (Achievements): Instancia del gestor de logros.
        state (dict): Estado actual del jugador para actualizar logros.
    """
    # Actualiza logros antes de mostrar
    achievements.update_achievements(state)
    
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
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and close_rect.collidepoint(event.pos):
                running = False

        # Panel base
        pygame.draw.rect(screen, (210, 180, 140), panel_rect, border_radius=12)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect, 3, border_radius=12)

        # Título
        title = big_font.render("LOGROS", True, (0, 0, 0))
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 15))

        # Botón cerrar
        pygame.draw.rect(screen, (220, 80, 80), close_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), close_rect, 2, border_radius=6)
        x_txt = font.render("X", True, (255, 255, 255))
        screen.blit(x_txt, (
            close_rect.centerx - x_txt.get_width() // 2,
            close_rect.centery - x_txt.get_height() // 2
        ))

        # Lista de logros
        y = panel_rect.y + 60
        for ach in achievements.achievements:
            rect = pygame.Rect(panel_rect.x + 20, y, panel_width - 40, 50)
            color = (100, 220, 100) if ach["completed"] else (220, 100, 100)
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=6)

            # Tooltip
            if rect.collidepoint(mouse_pos):
                info_surf = font.render(ach["desc"], True, (0, 0, 0))
                info_bg = pygame.Surface((info_surf.get_width() + 20, info_surf.get_height() + 10))
                info_bg.fill((255, 255, 200))
                screen.blit(info_bg, (mouse_pos[0] + 10, mouse_pos[1] - 30))
                screen.blit(info_surf, (mouse_pos[0] + 20, mouse_pos[1] - 25))

            status = "COMPLETADO" if ach["completed"] else "NO COMPLETADO"
            text_surf = font.render(f"{ach['name']} - {status}", True, (0, 0, 0))
            screen.blit(text_surf, (rect.x + 10, rect.y + 12))
            y += 60

        pygame.display.flip()
