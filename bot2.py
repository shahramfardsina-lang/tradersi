import requests
import time

coins = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL"
}

while True:
    try:
        ids = ",".join(coins.keys())

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

        data = requests.get(url).json()

        print("\n--- Crypto Prices ---")

        for coin_id, symbol in coins.items():
            price = data[coin_id]["usd"]
            print(symbol, ":", price, "USD")

        print("---------------------")

    except Exception as e:
        print("Error:", e)

    # هر 5 دقیقه
    time.sleep(300)