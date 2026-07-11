import requests


class MarketData:

    URL = (
        "https://api.coingecko.com/api/v3/coins/markets"
    )

    @staticmethod
    def get_top_coins(limit=100):

        params = {

            "vs_currency": "usd",

            "order": "market_cap_desc",

            "per_page": limit,

            "page": 1,

            "sparkline": "false",

            "price_change_percentage": "24h",

        }

        try:

            response = requests.get(
                MarketData.URL,
                params=params,
                timeout=15,
            )

            if response.status_code == 429:
                print("⚠️ CoinGecko rate limit")
                return []
            response.raise_for_status()

            data = response.json()

            coins = []

            for coin in data:

                coins.append({

                    "id":
                        coin["id"],

                    "symbol":
                        coin["symbol"].upper(),

                    "name":
                        coin["name"],

                    "price":
                        coin["current_price"],

                    "change":
                        coin.get(
                            "price_change_percentage_24h",
                            0,
                        ),

                    "volume":
                        coin.get(
                            "total_volume",
                            0,
                        ),

                    "marketcap":
                        coin.get(
                            "market_cap",
                            0,
                        ),

                })

            return coins

        except Exception as e:
            import traceback
            traceback.print_exc()
            return []