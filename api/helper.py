from random import random
import datetime
import time

class Ticker:
    def __init__(self, price=0):
        self.price = price
        self.prices_history = []
    
    @staticmethod
    def generate_movement():
        movement = -1 if random() < 0.5 else 1
        return movement
    
    @property
    def new_price(self):
        self.price += self.generate_movement()
        dt = datetime.datetime.now()
        self.prices_history.append({"pv": self.price, "uv": dt.strftime("%Y-%m-%d %H:%M:%S")})
        return {"pv": self.price, "uv": dt.strftime("%Y-%m-%d %H:%M:%S")}