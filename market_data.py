from api_manager import api_get


class MarketData:

    URL = "https://api.coingecko.com/api/v3/coins/markets"

    @staticmethod
    def get_top_coins(limit=100):

        all_coins = []

        pages = max(1, (limit + 19) // 20)

        for page in range(1, pages + 1):

            url = (
                f"{MarketData.URL}?vs_currency=usd"
                f"&order=market_cap_desc"
                f"&per_page=20"
                f"&page={page}"
                f"&sparkline=false"
                f"&price_change_percentage=24h"
            )

            data = api_get(url)

            if not data:
                continue

            for coin in data:

                all_coins.append({
                    "name": coin.get("id", ""),
                    "symbol": coin.get("symbol", "").upper(),
                    "price": coin.get("current_price", 0),
                    "change": coin.get("price_change_percentage_24h", 0) or 0,
                    "volume": coin.get("total_volume", 0),
                })

                if len(all_coins) >= limit:
                    return all_coins

        return all_coins


def get_market_data(coin):

    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin}"
        "?localization=false"
        "&tickers=false"
        "&market_data=true"
        "&community_data=false"
        "&developer_data=false"
    )

    data = api_get(url)

    if not data or "market_data" not in data:
        return None

    market = data["market_data"]

    return {
        "name": data.get("name", coin),
        "price": market["current_price"].get("usd", 0),
        "volume": market["total_volume"].get("usd", 0),
        "market_cap": market["market_cap"].get("usd", 0),
        "change_24h": market.get("price_change_percentage_24h", 0),
    }
