import requests


def load_my_coins():
    try:
        with open("my_coins.txt", "r") as file:
            return file.read().splitlines()
    except:
        return []


def get_market_coins(limit=100):

    url = (
        "https://api.coingecko.com/api/v3/coins/markets"
        "?vs_currency=usd"
        "&order=market_cap_desc"
        f"&per_page={limit}"
        "&page=1"
        "&sparkline=false"
    )

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

    except Exception as e:
        print("CoinGecko error:", e)
        return []

    coins = []

    for coin in data:

        coins.append({

            "id": coin["id"],
            "name": coin["name"],
            "symbol": coin.get("symbol", ""),

            "market_cap": coin.get("market_cap", 0),
            "volume": coin.get("total_volume", 0),
            "price": coin.get("current_price", 0),

            "change": coin.get(
                "price_change_percentage_24h"
            ) or 0,

            "rank": coin.get(
                "market_cap_rank",
                999
            )

        })

    return coins


def get_top_gainers(limit=20):

    coins = get_market_coins(250)

    coins.sort(
        key=lambda x: x["change"],
        reverse=True
    )

    return coins[:limit]


def get_top_losers(limit=20):

    coins = get_market_coins(250)

    coins.sort(
        key=lambda x: x["change"]
    )

    return coins[:limit]


def get_scan_list():

    market = get_market_coins(100)

    gainers = get_top_gainers(20)

    losers = get_top_losers(20)

    scan = {}

    for coin in market:
        coin["source"] = ["market"]
        scan[coin["id"]] = coin

    for coin in gainers:

        if coin["id"] in scan:

            scan[coin["id"]]["source"].append(
                "gainer"
            )

        else:

            coin["source"] = ["gainer"]
            scan[coin["id"]] = coin

    for coin in losers:

        if coin["id"] in scan:

            scan[coin["id"]]["source"].append(
                "loser"
            )

        else:

            coin["source"] = ["loser"]
            scan[coin["id"]] = coin

    custom = load_my_coins()

    for cid in custom:

        if cid not in scan:

            scan[cid] = {

                "id": cid,
                "name": cid,
                "symbol": "",
                "market_cap": 0,
                "volume": 0,
                "price": 0,
                "change": 0,
                "rank": 999,
                "source": ["custom"]

            }

    return list(scan.values())


def get_all_coins():
    return get_scan_list()