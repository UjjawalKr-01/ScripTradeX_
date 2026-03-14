from app.db import get_db

COMMISSION_RATE = 0.01

def calculate_commission(amount: float) -> float:
    return round(amount * COMMISSION_RATE, 2)