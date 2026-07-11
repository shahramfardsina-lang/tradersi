import requests



def get_coincap_data():

    url = (
        "https://api.coincap.io/v2/assets"
        "?limit=100"
    )


    try:

        response = requests.get(
            url,
            timeout=20
        )


        data = response.json()


        assets = data["data"]


        result = {}



        for coin in assets:


            symbol = coin["symbol"]


            result[symbol] = {

                "price": float(
                    coin["priceUsd"]
                ),

                "volume": float(
                    coin["volumeUsd24Hr"]
                ),

                "change": float(
                    coin["changePercent24Hr"]
                )

            }



        return result



    except Exception as e:

        print(
            "CoinCap error:",
            e
        )

        return {}




if __name__ == "__main__":


    data = get_coincap_data()


    print(
        "Coins:",
        len(data)
    )


    print(
        data.get("BTC")
    )