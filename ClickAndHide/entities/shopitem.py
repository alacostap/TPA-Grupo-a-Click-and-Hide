# entities/shop_item.py

import pygame

class ShopItem:
    """Ítem comprable en la tienda."""

    def __init__(self, name, cost, base_income, tipo):
        self.name = name
        self.cost = cost
        self.base_income = base_income
        self.tipo = tipo  # "click" o "auto"
        self.amount = 0

    def buy(self, player):
        """Intenta comprar el ítem. Retorna True si la compra fue exitosa."""
        if player.money >= self.cost:
            player.money -= self.cost
            self.amount += 1
            self.cost = int(self.cost * 1.15)
            return True
        return False

    def draw_item(self, screen, font, x, y, can_afford, mouse_pos, color=(230, 200, 150)):
        """Dibuja el botón del ítem en pantalla."""
        rect = pygame.Rect(x, y, 300, 60)
        draw_color = color if can_afford else (160, 160, 160)
        if rect.collidepoint(mouse_pos):
            draw_color = tuple(min(255, c + 25) for c in draw_color)

        pygame.draw.rect(screen, draw_color, rect, border_radius=10)
        pygame.draw.rect(screen, (80, 60, 40), rect, 2, border_radius=10)

        # Textos: nombre, costo y cantidad
        screen.blit(font.render(self.name, True, (50, 35, 20)), (rect.x + 10, rect.y + 6))
        screen.blit(font.render(f"${self.cost}", True, (60, 45, 30)), (rect.x + 10, rect.y + 30))
        screen.blit(font.render(f"x{self.amount}", True, (50, 35, 20)), (rect.right - 50, rect.y + 18))
