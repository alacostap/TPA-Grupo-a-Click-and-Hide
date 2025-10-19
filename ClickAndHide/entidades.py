#entidades.py

class Player:
    def __init__(self):
        self.money = 0
        self.last_earn_time = -999.0

        # ---- Atributos para logros ----
        self.clicks_realizados = 0     # Número total de clicks hechos
        self.upgrades_compra = 0       # Número total de mejoras compradas


class Teacher:
    def __init__(self):
        self.next_question_time = 0
