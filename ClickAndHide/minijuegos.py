# minijuegos.py
import random
import time

class QuestionMinigame:
    def __init__(self):
        self.active = False
        self.question = ""
        self.answer = 0
        self.start_time = 0
        self.time_limit = 7
        self.input_text = ""
        self.result = None
        self.reward = 50
        self.penalty = 20

    def start(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*'])
        if op == '+':
            self.answer = a + b
        elif op == '-':
            self.answer = a - b
        else:
            self.answer = a * b
        self.question = f"{a} {op} {b} = ?"
        self.input_text = ""
        self.start_time = time.time()
        self.active = True
        self.result = None

    def update(self):
        if not self.active:
            return
        if time.time() - self.start_time > self.time_limit:
            self.active = False
            self.result = "timeout"

    def submit(self):
        try:
            val = int(self.input_text.strip())
        except:
            val = None
        if val == self.answer:
            self.result = "correct"
        else:
            self.result = "wrong"
        self.active = False
