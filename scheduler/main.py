import redis
import time
import json
from helper import Ticker

r = redis.Redis(host='redis', port=6379)

def get_ticker_name_by_number(number: int) -> str: 
    return str(number) if number > 9 else '0' + str(number)

tickers = {f"ticker{get_ticker_name_by_number(el)}": Ticker(name=f"ticker{get_ticker_name_by_number(el)}") for el in range(100)}

def store_all_tickers():
    for ticker_name, ticker_inst in tickers.items():
        r.publish(ticker_name, json.dumps(ticker_inst.price_now))


def start_ticker():
    while True:
        store_all_tickers()
        time.sleep(10)

if __name__ == '__main__':
   start_ticker()
