from random import random
import datetime
import time

class Ticker:
    def __init__(self, name: str, price: int =0):
        self.price = price
        self.name = name
    
    @staticmethod
    def generate_movement():
        movement = -1 if random() < 0.5 else 1
        return movement

    @property
    def price_now(self) -> dict:
        self.price += self.generate_movement()
        dt = datetime.datetime.now()
        return {"price": self.price, "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S")}