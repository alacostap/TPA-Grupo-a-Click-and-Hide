"""
intro.py — Animación de introducción de Click & Hide.

Muestra una breve secuencia animada antes del inicio del juego, incluyendo:
  - Fondo con imagen personalizada
  - Texto principal animado y pulsante
  - Logotipo girando
  - Texto de carga animado ("Cargando...")
  - Posibilidad de saltar la intro con clic o tecla
"""

import pygame
import os
import math


# --- REPRODUCIR INTRO ---
def play_intro(screen, background_image_name="inicio.png"):
    """
    Reproduce la animación de introducción del juego.

    Args:
        screen (pygame.Surface): Ventana principal de Pygame donde se dibuja la intro.
        background_image_name (str): Nombre de la imagen de fondo, por defecto "inicio.png".

    Comportamiento:
        - Aparece el texto "CLICK AND HIDE" descendiendo desde arriba.
        - El texto realiza un leve efecto de pulso (zoom suave).
        - Se muestra un logotipo girando en la parte inferior.
        - Aparece un texto de carga con puntos animados.
        - El jugador puede saltar la intro con cualquier tecla o clic.
        - Se cierra automáticamente tras unos segundos.
    """
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # --- Cargar imágenes y fuentes ---
    base_path = os.path.dirname(__file__)
    bg_image = pygame.image.load(
        os.path.join(base_path, "assets", "images", background_image_name)
    ).convert_alpha()
    logo_image = pygame.image.load(
        os.path.join(base_path, "assets", "images", "logo.png")
    ).convert_alpha()
    logo_image = pygame.transform.smoothscale(logo_image, (100, 100))
    font_path = os.path.join(base_path, "assets", "fonts", "PressStart2P.ttf")

    main_font_size = 64
    main_text = "CLICK AND HIDE"
    main_font = pygame.font.Font(font_path, main_font_size)

    # --- Variables de animación ---
    move_duration = 3.0  # Segundos que tarda el texto en caer
    load_duration = 5.0  # Duración total del texto de carga
    start_ticks = pygame.time.get_ticks()
    text_y_start = -main_font_size
    text_y_end = height // 2 - 100
    text_color = (255, 255, 255)
    logo_angle = 0
    running = True

    # --- Bucle principal ---
    while running:
        dt = clock.tick(60) / 1000.0
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False  # Saltar intro

        # --- Fondo ---
        screen.blit(pygame.transform.smoothscale(bg_image, (width, height)), (0, 0))

        # --- Texto principal animado ---
        progress = min(1, elapsed / move_duration)
        smooth = 1 - (1 - progress) ** 3  # Movimiento con suavizado cúbico
        text_y = text_y_start + (text_y_end - text_y_start) * smooth

        pulse_scale = 1 + 0.02 * math.sin(elapsed * 6)
        font_size = int(main_font_size * pulse_scale)
        pulse_font = pygame.font.Font(font_path, font_size)
        text_surf = pulse_font.render(main_text, True, text_color)
        text_rect = text_surf.get_rect(center=(width // 2, int(text_y)))

        # --- Efecto de brillo/sombra ---
        for offset in range(2, 0, -1):
            glow = pulse_font.render(main_text, True, (150, 150, 150))
            glow.set_alpha(80)
            screen.blit(glow, (text_rect.x - offset, text_rect.y - offset))
            screen.blit(glow, (text_rect.x + offset, text_rect.y + offset))

        screen.blit(text_surf, text_rect)

        # --- Logo girando + texto de carga ---
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

        # --- Fin automático ---
        if elapsed >= move_duration + load_duration:
            running = False
