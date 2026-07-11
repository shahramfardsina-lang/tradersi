from scanner import (
    get_all_coins,
    get_market_coins,
    get_top_gainers,
    get_top_losers
)
from market_score import score_market
from candles import get_candles
from indicators import calculate_indicators
from analyzer import analyze_coin

import time
import json
import os
from datetime import datetime

# ===========================================
# CONFIG
# ===========================================

MAX_ANALYZE = 20

RETRY_COUNT = 3

RETRY_WAIT = [15, 30, 45]

REPORT_FILE = "analysis_report.json"

HISTORY_FILE = "history.json"

MAX_HISTORY = 100

SLEEP_BETWEEN_COINS = 4


# ===========================================
# HISTORY ENGINE
# ===========================================

def load_history():

    if not os.path.exists(HISTORY_FILE):

        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


def save_history(results):

    history = load_history()

    snapshot = {

        "time":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "top5": []

    }

    for coin in results[:5]:

        snapshot["top5"].append({

            "name":
            coin["name"],

            "score":
            coin["score"],

            "signal":
            coin["signal"]

        })

    history.append(snapshot)

    history = history[-MAX_HISTORY:]

    with open(

        HISTORY_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            history,

            f,

            indent=4,

            ensure_ascii=False

        )

    return history


def compare_history(results, history):

    if len(history) < 2:

        print("\n📁 First execution")

        return

    print("\n===== MARKET CHANGE =====")

    previous = {

        x["name"]: x["score"]

        for x in history[-2]["top5"]

    }

    for coin in results[:5]:

        name = coin["name"]

        score = coin["score"]

        if name not in previous:

            print(f"🆕 {name} entered Top5")

            continue

        diff = score - previous[name]

        if diff > 0:

            print(f"📈 {name}: +{diff}")

        elif diff < 0:

            print(f"📉 {name}: {diff}")

        else:

            print(f"➖ {name}: No change")


# ===========================================
# REPORT
# ===========================================

def save_report(report):

    with open(

        REPORT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            report,

            f,

            indent=4,

            ensure_ascii=False

        )


# ===========================================
# SINGLE COIN ANALYSIS
# ===========================================

def analyze_single_coin(coin):

    try:

        prices, error = get_candles(
            coin["id"]
        )

        if prices is None:

            return None, error

        indicators = calculate_indicators(
            prices
        )

        if indicators is None:

            return None, "Indicator error"

        analysis = analyze_coin(
            coin,
            indicators
        )

        result = {

            "name": coin["name"],

            "id": coin["id"],

            "score": analysis["score"],

            "signal": analysis["signal"],

            "rsi": round(
                indicators.get("rsi", 0),
                2
            ),

            "ema20": round(
                indicators.get("ema20", 0),
                4
            ),

            "ema50": round(
                indicators.get("ema50", 0),
                4
            ),

            "macd": round(
                indicators.get("macd", 0),
                4
            )

        }

        return result, None

    except Exception as e:

        return None, str(e)

# ===========================================
# RETRY SYSTEM
# ===========================================

def retry_coin(coin):

    for attempt in range(RETRY_COUNT):

        print(
            f"🔄 Retry {coin['name']} "
            f"{attempt+1}/{RETRY_COUNT}"
        )

        time.sleep(RETRY_WAIT[attempt])

        result, error = analyze_single_coin(coin)

        if result:

            print(
                f"✅ {coin['name']} recovered"
            )

            return result

        print(
            f"⚠️ {error}"
        )

    print(
        f"❌ {coin['name']} skipped"
    )

    return None


# ===========================================
# AI DECISION ENGINE
# ===========================================

def ai_market_review(results):

    if not results:

        return {

            "best_coin": None,

            "decision": "WAIT",

            "confidence": 0,

            "trend": "UNKNOWN",

            "risk": "UNKNOWN",

            "market_health": 0,

            "entry_zone": 0,

            "stop_loss": 0,

            "take_profit": 0,

            "reason": [],

            "watch_list": []

        }

    best = results[0]

    reasons = []

    bullish = 0

    # EMA

    if best["ema20"] > best["ema50"]:

        bullish += 1

        reasons.append(
            "EMA20 above EMA50"
        )

    else:

        reasons.append(
            "EMA20 below EMA50"
        )

    # MACD

    if best["macd"] > 0:

        bullish += 1

        reasons.append(
            "MACD positive"
        )

    else:

        reasons.append(
            "MACD negative"
        )

    # RSI

    if 45 <= best["rsi"] <= 65:

        bullish += 1

        reasons.append(
            "Healthy RSI"
        )

    elif best["rsi"] < 45:

        reasons.append(
            "Weak RSI"
        )

    else:

        reasons.append(
            "RSI overbought"
        )

    confidence = min(

        100,

        best["score"] + bullish * 10

    )

    market_health = int(

        (confidence + best["score"]) / 2

    )

    if confidence >= 90:

        decision = "BUY 🟢"

        risk = "LOW"

    elif confidence >= 75:

        decision = "WATCH 🟡"

        risk = "MEDIUM"

    else:

        decision = "WAIT 🔴"

        risk = "HIGH"

    trend = (

        "Bullish"

        if bullish >= 2

        else "Bearish"

    )

    entry = round(

        (best["ema20"] + best["ema50"]) / 2,

        4

    )

    stop = round(

        entry * 0.97,

        4

    )

    take = round(

        entry * 1.08,

        4

    )

    return {

        "best_coin": best["name"],

        "decision": decision,

        "confidence": confidence,

        "trend": trend,

        "risk": risk,

        "market_health": market_health,

        "entry_zone": entry,

        "stop_loss": stop,

        "take_profit": take,

        "reason": reasons,

        "watch_list": [

            coin["name"]

            for coin in results[:5]

        ]

    }

# ==========================
# MAIN BOT
# ==========================

def run_bot():

    print("\n🚀 Crypto AI Analyzer V2 Base")
    print("--------------------")

    market = get_market_coins(100)
    gainers = get_top_gainers(20)
    losers = get_top_losers(20)
    coins = get_all_coins()

    print("Market coins :", len(market))
    print("Top gainers  :", len(gainers))
    print("Top losers   :", len(losers))
    print("Total scan   :", len(coins))

    if not coins:
        print("No market data")
        return

    print("\n📊 Market scoring...")
    market_top = score_market(coins, limit=30)

    print("\n===== TOP 30 MARKET =====")
    for coin in market_top:
        print(coin["name"], "| Score:", coin["score"])

    results=[]
    retry_list=[]
    skipped=[]
    recovered=[]

    print("\n📈 Technical analysis...")
    for coin in market_top[:MAX_ANALYZE]:
        print(f"\n🔍 {coin['name']}")
        result,error=analyze_single_coin(coin)
        if result:
            results.append(result)
            print(f"✅ Score: {result['score']} | RSI: {result['rsi']} | MACD: {result['macd']}")
        else:
            retry_list.append(coin)
        time.sleep(SLEEP_BETWEEN_COINS)

    for coin in retry_list:
        r=retry_coin(coin)
        if r: recovered.append(coin["name"]); results.append(r)
        else: skipped.append({"name":coin["name"],"reason":"Retry failed"})

    results={c["id"]:c for c in results}
    results=sorted(results.values(),key=lambda x:x["score"],reverse=True)

    ai_result=ai_market_review(results)
    report={"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"market_health":ai_result["market_health"],"top5":results[:5],"all_results":results,"recovered":recovered,"skipped":skipped,"ai_review":ai_result}
    save_report(report)
    history=save_history(results)
    compare_history(results,history)
    print("\n💾 analysis_report.json updated")
    print("💾 history.json updated")

# ==========================
# START BOT
# ==========================

import traceback

if __name__ == "__main__":

    while True:

        try:

            run_bot()

        except Exception:

            print("\n❌ BOT ERROR")
            traceback.print_exc()

        print(
            "\n⏳ Waiting 5 minutes..."
        )

        time.sleep(300)