import requests
import asyncio
import time
import numpy as np

SYMBOL = "MATICUSDT"
BUY_PRICE = 34160
SELL_PRICE = 34501

API_URL = "https://testnet.binance.vision"  # https://api.binance.com

is_opened = False


def calc_sma(data):
    closes = [float(candle[4]) for candle in data]
    return np.mean(closes)


async def start():
    global is_opened
    response = requests.get(
        API_URL + "/api/v3/klines?limit=21&interval=15m&symbol=" + SYMBOL)
    data = response.json()
    candle = data[-1]
    price = float(candle[4])

    print("\033c", end="")
    print("Price: " + str(price))

    sma21 = calc_sma(data)
    sma13 = calc_sma(data[8:])
    print("SMA (13): " + str(sma13))
    print("SMA (21): " + str(sma21))
    print("Is Opened? " + str(is_opened))

    if sma13 > sma21 and not is_opened:
        print("comprar")
        is_opened = True
    elif sma13 < sma21 and is_opened:
        print("vender")
        is_opened = False
    else:
        print("aguardar")


while True:
    asyncio.run(start())
    time.sleep(3)
