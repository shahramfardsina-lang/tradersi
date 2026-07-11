import json
from datetime import datetime



def load_report():

    try:

        with open(
            "analysis_report.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception as e:

        print(
            "Report load error:",
            e
        )

        return None





def create_ai_report(data):


    print("\n🤖 AI MARKET REVIEW")
    print("--------------------")


    top5 = data.get(
        "top5",
        []
    )


    if not top5:

        print(
            "No data"
        )

        return




    for i, coin in enumerate(top5,1):


        print("\n#" , i)

        print(
            coin["name"]
        )


        print(
            "Score:",
            coin["score"]
        )


        print(
            "Signal:",
            coin["signal"]
        )


        print(
            "RSI:",
            round(
                coin["rsi"],
                2
            )
        )


        print(
            "MACD:",
            round(
                coin["macd"],
                3
            )
        )



        # تحلیل ساده


        if coin["rsi"] > 70:


            print(
                "Risk: RSI high - possible overbought"
            )


        elif coin["rsi"] < 40:


            print(
                "Risk: Weak momentum"
            )


        else:


            print(
                "RSI: Healthy zone"
            )




        if coin["ema20"] > coin["ema50"]:


            print(
                "Trend: EMA bullish ✅"
            )


        else:


            print(
                "Trend: EMA weak 🔴"
            )



        if coin["macd"] > 0:


            print(
                "Momentum: Positive ✅"
            )


        else:


            print(
                "Momentum: Negative 🔴"
            )






    print("\n====================")

    print(
        "Generated:",
        datetime.now()
    )







if __name__ == "__main__":


    report = load_report()


    if report:

        create_ai_report(report)