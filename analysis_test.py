from candles import get_candles
from indicators import calculate_indicators


coin = "bitcoin"

# گرفتن قیمت‌های گذشته
prices = get_candles(coin)


# محاسبه اندیکاتورها
result = calculate_indicators(prices)


print("===== ANALYSIS =====")
print("Coin:", coin.upper())
print("Price:", result["price"])
print("RSI:", result["rsi"])
print("EMA20:", result["ema20"])
print("EMA50:", result["ema50"])


# تحلیل ساده روند

if result["ema20"] > result["ema50"]:
    print("Trend: UP 🟢")
else:
    print("Trend: DOWN 🔴")


if result["rsi"] < 30:
    print("Momentum: Oversold (Possible Opportunity) 🟢")

elif result["rsi"] > 70:
    print("Momentum: Overbought ⚠️")

else:
    print("Momentum: Neutral 🟡")