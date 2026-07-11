import ccxt


def test_binance():

    exchange = ccxt.binance()

    try:

        ticker = exchange.fetch_ticker("BTC/USDT")

        print("✅ Binance Connected")
        print("------------------")
        print("BTC Price:", ticker["last"])
        print("Volume:", ticker["baseVolume"])


    except Exception as e:

        print("❌ Connection Error:")
        print(e)



if __name__ == "__main__":

    test_binance()