from symbol_map import get_symbol
from coincap_data import get_coincap_data




def combine_market_data(coins):


    cap_data = get_coincap_data()


    results = []



    for coin in coins:


        symbol = get_symbol(
            coin["id"]
        )


        if symbol is None:

            continue



        if symbol not in cap_data:

            continue



        market = cap_data[symbol]



        results.append({

            "id": coin["id"],

            "name": coin["name"],

            "market_cap": coin["market_cap"],

            "rank": coin["rank"],

            "volume": market["volume"],

            "price": market["price"],

            "change": market["change"]

        })


    return results