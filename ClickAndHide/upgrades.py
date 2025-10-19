import pygame

class Upgrade:
    def __init__(self, name, cost, increment, x, y):
        self.name = name
        self.cost = cost
        self.base_cost = cost          # 👈 guardamos el costo original
        self.increment = increment
        self.level = 0
        self.rect = pygame.Rect(x, y, 160, 80)

    def buy(self, player):
        # Redondear dinero antes de comparar
        if round(player.money, 1) >= self.cost:
            player.money = round(player.money - self.cost, 1)
            self.level += 1
            self.cost = round(self.cost * 1.5, 1)
            return self.increment
        return 0

    def draw(self, screen, font):
        # Fondo de la mejora
        pygame.draw.rect(screen, (200, 160, 50), self.rect, border_radius=8)
        # Borde exterior
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3, border_radius=8)

        # Texto
        txt_name = font.render(self.name, True, (0, 0, 0))
        txt_level = font.render(f"Nivel {self.level}", True, (0, 0, 0))
        txt_cost = font.render(f"Costo: ${self.cost}", True, (0, 0, 0))

        # Centrar textos horizontalmente
        screen.blit(txt_name, (self.rect.centerx - txt_name.get_width()//2, self.rect.y + 10))
        screen.blit(txt_level, (self.rect.centerx - txt_level.get_width()//2, self.rect.y + 35))
        screen.blit(txt_cost, (self.rect.centerx - txt_cost.get_width()//2, self.rect.y + 60))
