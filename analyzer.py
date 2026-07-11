# V2 Base
def analyze_coin(coin, indicators):

    score = 0


    # Market

    market_score = coin.get("score", 0)


    if market_score >= 70:
        score += 30

    elif market_score >= 50:
        score += 25

    elif market_score >= 30:
        score += 15



    # RSI

    rsi = indicators.get("rsi", 50)


    if 45 <= rsi <= 60:
        score += 25

    elif 35 <= rsi < 45:
        score += 20

    elif rsi < 35:
        score += 10

    elif 60 < rsi <= 70:
        score += 5

    elif 70 < rsi <= 80:
        score -= 15

    elif rsi > 80:
        score -= 30



    # EMA

    ema20 = indicators.get("ema20",0)

    ema50 = indicators.get("ema50",0)


    if ema20 > 0 and ema50 > 0:


        if ema20 > ema50:

            score += 25

        else:

            score -= 5




    # MACD

    macd = indicators.get("macd",0)


    if macd > 0:

        score += 20

    else:

        score -= 5



    # Limit

    score = max(
        0,
        min(score,100)
    )



    if score >= 75:

        signal = "STRONG WATCH 🟢"


    elif score >= 55:

        signal = "WATCH 🟡"


    else:

        signal = "WEAK 🔴"



    return {

        "score": score,

        "signal": signal

    }