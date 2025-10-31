import pygame
import os
import math
import time

def play_intro(screen, background_image_name="inicio.png"):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # ---------- Cargar imágenes ----------
    base_path = os.path.dirname(__file__)
    bg_path = os.path.join(base_path, "assets", "imagenes", background_image_name)
    logo_path = os.path.join(base_path, "assets", "imagenes", "logo.png")

    try:
        bg_image = pygame.image.load(bg_path).convert_alpha()
    except:
        print(f"No se pudo cargar {background_image_name}, usando fondo negro.")
        bg_image = None

    try:
        logo_image = pygame.image.load(logo_path).convert_alpha()
        logo_image = pygame.transform.smoothscale(logo_image, (100, 100))  # tamaño reducido
    except:
        print("No se pudo cargar logo.png")
        logo_image = None

    # ---------- Fuente ----------
    font_path = os.path.join(base_path, "assets", "fonts", "PressStart2P.ttf")
    main_font_size = 64
    main_font = pygame.font.Font(font_path, main_font_size)
    text_color = (255, 255, 255)
    main_text = "CLICK AND HIDE"

    # ---------- Animación ----------
    move_duration = 3.0  # tiempo en deslizar
    load_duration = 5.0  # tiempo de carga tras deslizar
    start_ticks = pygame.time.get_ticks()
    running = True

    text_y_start = -main_font_size
    text_y_end = height // 2 - 100  # un poco arriba del centro

    logo_angle = 0

    while running:
        dt = clock.tick(60) / 1000.0
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # ---------- Fondo ----------
        if bg_image:
            bg_scaled = pygame.transform.smoothscale(bg_image, (width, height))
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # ---------- Movimiento del texto ----------
        if elapsed < move_duration:
            progress = elapsed / move_duration
            smooth = 1 - (1 - progress) ** 3  # ease-out cubic
            text_y = text_y_start + (text_y_end - text_y_start) * smooth
        else:
            text_y = text_y_end

        # Pulso leve
        pulse_scale = 1 + 0.02 * math.sin(elapsed * 6)
        font_size = max(1, int(main_font_size * pulse_scale))
        pulse_font = pygame.font.Font(font_path, font_size)
        text_surf = pulse_font.render(main_text, True, text_color)
        text_rect = text_surf.get_rect(center=(width // 2, int(text_y)))

        # Glow leve detrás del texto
        for offset in range(2, 0, -1):
            glow_surf = pulse_font.render(main_text, True, (150, 150, 150))
            glow_surf.set_alpha(80)
            screen.blit(glow_surf, (text_rect.x - offset, text_rect.y - offset))
            screen.blit(glow_surf, (text_rect.x + offset, text_rect.y + offset))

        # Texto principal
        screen.blit(text_surf, text_rect)

        # ---------- Logo girando + Cargando menú ----------
        if elapsed >= move_duration:
            # logo
            if logo_image:
                logo_angle += 90 * dt  # grados por segundo
                rotated_logo = pygame.transform.rotate(logo_image, logo_angle)
                logo_rect = rotated_logo.get_rect(center=(width//2, height - 120))
                screen.blit(rotated_logo, logo_rect)

            # texto cargando menú con puntos animados
            load_font = pygame.font.Font(font_path, 28)
            dots = int((elapsed - move_duration) * 2) % 4  # 0 a 3 puntos
            load_text = "Cargando menú" + "." * dots
            load_surf = load_font.render(load_text, True, (255, 255, 255))
            load_rect = load_surf.get_rect(center=(width//2, height - 40))
            screen.blit(load_surf, load_rect)

        pygame.display.flip()

        # ---------- Tiempo total ----------
        if elapsed >= move_duration + load_duration:
            running = False
