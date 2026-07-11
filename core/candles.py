import requests

def get_candles(coin_id):
    try:
        url=(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
             "?vs_currency=usd&days=30&interval=daily")
        r=requests.get(url,timeout=10)
        if r.status_code!=200:
            return None, f"HTTP {r.status_code}"
        data=r.json()
        prices=[p[1] for p in data.get("prices",[])]
        return prices, None
    except Exception as e:
        return None, str(e)
