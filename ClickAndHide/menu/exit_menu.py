#exit_menu.py

import pygame
import sys

# ----- SHOW EXIT PANEL -----
def show_exit_panel(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 36)

    panel_width, panel_height = 400, 200
    panel_x = (screen.get_width() - panel_width) // 2
    panel_y = (screen.get_height() - panel_height) // 2
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    yes_rect = pygame.Rect(panel_rect.x + 60, panel_rect.bottom - 60, 100, 40)
    no_rect = pygame.Rect(panel_rect.right - 160, panel_rect.bottom - 60, 100, 40)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(event.pos):
                    running = False

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (255, 240, 180), panel_rect, border_radius=12)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect, 3, border_radius=12)

        title = big_font.render("Exit game?", True, (0, 0, 0))
        screen.blit(title, (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 40))

        pygame.draw.rect(screen, (100, 200, 100), yes_rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), yes_rect, 2, border_radius=8)
        txt_yes = font.render("Yes", True, (0, 0, 0))
        screen.blit(txt_yes, (yes_rect.centerx - txt_yes.get_width() // 2, yes_rect.centery - txt_yes.get_height() // 2))

        pygame.draw.rect(screen, (200, 100, 100), no_rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), no_rect, 2, border_radius=8)
        txt_no = font.render("No", True, (0, 0, 0))
        screen.blit(txt_no, (no_rect.centerx - txt_no.get_width() // 2, no_rect.centery - txt_no.get_height() // 2))

        pygame.display.flip()
