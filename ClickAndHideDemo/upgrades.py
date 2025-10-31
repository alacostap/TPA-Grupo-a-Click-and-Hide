import pygame

class ShopItem:
    def __init__(self, name, base_cost, base_income, tipo="auto", cost_growth=1.15):
        """
        name: nombre del objeto
        base_cost: costo inicial
        base_income: ingreso base (por click o por segundo)
        tipo: 'click' o 'auto'
        cost_growth: multiplicador de coste por compra
        """
        self.name = name
        self.base_cost = base_cost
        self.cost = base_cost
        self.base_income = base_income
        self.amount = 0
        self.tipo = tipo
        self.cost_growth = cost_growth
        self.rect = pygame.Rect(0, 0, 260, 80)

    def buy(self, player):
        """Compra una unidad si hay suficiente dinero."""
        if player.money >= self.cost:
            player.money -= self.cost
            self.amount += 1
            self.cost = int(self.cost * self.cost_growth)
            return True
        return False

    def get_total_income(self):
        """Devuelve la producción total de este ítem."""
        return self.base_income * self.amount

    def draw(self, screen, font, x, y, can_afford):
        """Dibuja la línea de la tienda."""
        self.rect.topleft = (x, y)
        color = (240, 220, 140) if can_afford else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=8)

        txt_name = font.render(self.name, True, (0, 0, 0))
        txt_cost = font.render(f"${self.cost}", True, (50, 50, 50))
        txt_amount = font.render(f"x{self.amount}", True, (0, 0, 0))

        screen.blit(txt_name, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(txt_cost, (self.rect.x + 10, self.rect.y + 45))
        screen.blit(txt_amount, (self.rect.right - 60, self.rect.y + 25))
