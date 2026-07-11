import requests



def get_all_binance_data():

    url = (
        "https://api.binance.com/api/v3/ticker/24hr"
    )


    try:

        response = requests.get(
            url,
            timeout=30
        )


        data = response.json()


        result = {}


        for item in data:

            symbol = item.get(
                "symbol",
                ""
            )


            if symbol.endswith("USDT"):


                coin = symbol.replace(
                    "USDT",
                    ""
                )


                result[coin] = {

                    "volume": float(
                        item["quoteVolume"]
                    ),

                    "price": float(
                        item["lastPrice"]
                    ),

                    "change": float(
                        item["priceChangePercent"]
                    )

                }


        return result



    except Exception as e:

        print(
            "Binance error:",
            e
        )

        return {}





if __name__ == "__main__":


    data = get_all_binance_data()


    print(
        "Binance coins:",
        len(data)
    )


    print(
        data.get(
            "BTC"
        )
    )