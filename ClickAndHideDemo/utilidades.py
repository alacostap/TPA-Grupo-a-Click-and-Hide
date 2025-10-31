# utilidades.py
import time
from config import *

def clamp_money(money):
    return max(0, money)

def can_earn(last_earn_time):
    now = time.time()
    if now - last_earn_time >= EARN_COOLDOWN:
        return True
    return False
