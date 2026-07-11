STABLE_WORDS = [

    "usd",
    "tether",
    "usdc",
    "dai",
    "stable"

]





def is_stable_coin(coin):


    name = coin.get(
        "name",
        ""
    ).lower()


    symbol = coin.get(
        "symbol",
        ""
    ).lower()



    for word in STABLE_WORDS:


        if word in name or word in symbol:

            return True



    return False






def score_market(coins, limit=30):


    results = []



    for coin in coins:



        if is_stable_coin(coin):

            continue




        score = 0



        market_cap = coin.get(
            "market_cap",
            0
        ) or 0



        volume = coin.get(
            "volume",
            0
        ) or 0



        change = coin.get(
            "change",
            0
        ) or 0




        # Market Cap Score

        if market_cap > 50_000_000_000:

            score += 30


        elif market_cap > 10_000_000_000:

            score += 25


        elif market_cap > 1_000_000_000:

            score += 15


        elif market_cap > 100_000_000:

            score += 10





        # Volume Score

        if volume > 5_000_000_000:

            score += 35


        elif volume > 1_000_000_000:

            score += 25


        elif volume > 100_000_000:

            score += 15


        elif volume > 10_000_000:

            score += 5






        # Daily momentum

        if change > 5:

            score += 20


        elif change > 0:

            score += 10


        elif change < -5:

            score -= 10






        # Volume / Market Cap

        if market_cap > 0:


            volume_ratio = volume / market_cap


            if volume_ratio > 0.1:

                score += 10






        results.append({

            "id": coin.get(
                "id",
                ""
            ),


            "name": coin.get(
                "name",
                ""
            ),


            "symbol": coin.get(
                "symbol",
                ""
            ),


            "score": max(
                0,
                score
            ),


            "market_cap": market_cap,


            "volume": volume,


            "price": coin.get(
                "price",
                0
            ),


            "change": change

        })






    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )



    return results[:limit]