# entities/shop_item.py
import pygame

class ShopItem:
    def __init__(self, name, cost, base_income, tipo, color=(230, 200, 150)):
        self.name = name
        self.base_cost = cost
        self.cost = cost
        self.base_income = base_income
        self.tipo = tipo  # "click" o "auto"
        self.amount = 0
        self.color = color
        self.rect = None

    def buy(self, player):
        """Intenta comprar el ítem usando el dinero del jugador."""
        if player.money >= self.cost:
            player.money -= self.cost
            self.amount += 1
            self.cost = int(self.cost * 1.15)  # Incremento del costo
            return True
        return False

    def render(self, screen, font, x, y, can_afford, mouse_pos):
        """Dibuja el botón de compra."""
        rect = pygame.Rect(x, y, 300, 60)
        self.rect = rect

        color = self.color if can_afford else (160, 160, 160)
        if rect.collidepoint(mouse_pos):
            color = tuple(min(255, c + 25) for c in color)

        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, (80, 60, 40), rect, 2, border_radius=10)

        name_txt = font.render(self.name, True, (50, 35, 20))
        cost_txt = font.render(f"${self.cost}", True, (60, 45, 30))
        qty_txt = font.render(f"x{self.amount}", True, (50, 35, 20))

        screen.blit(name_txt, (rect.x + 10, rect.y + 6))
        screen.blit(cost_txt, (rect.x + 10, rect.y + 30))
        screen.blit(qty_txt, (rect.right - 50, rect.y + 18))
