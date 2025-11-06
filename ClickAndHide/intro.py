"""
intro.py — Animación de introducción de Click & Hide.

Muestra:
  - Fondo personalizado
  - Texto animado "CLICK AND HIDE"
  - Logotipo girando
  - Texto de carga con puntos

Se puede saltar con cualquier tecla o clic.
"""

import pygame
import os
import math


def play_intro(screen, background_image_name="inicio.png"):
    """
    Reproduce la intro del juego.

    Args:
        screen (pygame.Surface): Ventana principal.
        background_image_name (str): Archivo de fondo (default: "inicio.png").

    Comportamiento:
        - Texto principal animado
        - Logo girando
        - Texto de carga animado
        - Salto con clic o tecla
        - Termina automáticamente tras unos segundos
    """
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # Cargar imágenes y fuente
    base_path = os.path.dirname(__file__)
    bg_image = pygame.image.load(os.path.join(base_path, "assets", "images", background_image_name)).convert_alpha()
    logo_image = pygame.image.load(os.path.join(base_path, "assets", "images", "logo.png")).convert_alpha()
    logo_image = pygame.transform.smoothscale(logo_image, (100, 100))
    font_path = os.path.join(base_path, "assets", "fonts", "PressStart2P.ttf")
    main_font_size = 64
    main_text = "CLICK AND HIDE"
    main_font = pygame.font.Font(font_path, main_font_size)

    # Variables de animación
    move_duration = 3.0
    load_duration = 5.0
    start_ticks = pygame.time.get_ticks()
    text_y_start = -main_font_size
    text_y_end = height // 2 - 100
    text_color = (255, 255, 255)
    logo_angle = 0
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        # Fondo
        screen.blit(pygame.transform.smoothscale(bg_image, (width, height)), (0, 0))

        # Texto animado
        progress = min(1, elapsed / move_duration)
        smooth = 1 - (1 - progress) ** 3
        text_y = text_y_start + (text_y_end - text_y_start) * smooth
        pulse_scale = 1 + 0.02 * math.sin(elapsed * 6)
        font_size = int(main_font_size * pulse_scale)
        pulse_font = pygame.font.Font(font_path, font_size)
        text_surf = pulse_font.render(main_text, True, text_color)
        text_rect = text_surf.get_rect(center=(width // 2, int(text_y)))

        for offset in range(2, 0, -1):
            glow = pulse_font.render(main_text, True, (150, 150, 150))
            glow.set_alpha(80)
            screen.blit(glow, (text_rect.x - offset, text_rect.y - offset))
            screen.blit(glow, (text_rect.x + offset, text_rect.y + offset))

        screen.blit(text_surf, text_rect)

        # Logo girando y texto de carga
        if elapsed >= move_duration:
            logo_angle += 90 * dt
            rotated_logo = pygame.transform.rotate(logo_image, logo_angle)
            logo_rect = rotated_logo.get_rect(center=(width // 2, height - 120))
            screen.blit(rotated_logo, logo_rect)

            load_font = pygame.font.Font(font_path, 28)
            dots = int((elapsed - move_duration) * 2) % 4
            load_text = "Cargando" + "." * dots
            load_surf = load_font.render(load_text, True, (255, 255, 255))
            screen.blit(load_surf, load_surf.get_rect(center=(width // 2, height - 40)))

        pygame.display.flip()

        if elapsed >= move_duration + load_duration:
            running = False
