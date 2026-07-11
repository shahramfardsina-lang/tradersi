SYMBOLS = {

    "bitcoin": "BTC",
    "ethereum": "ETH",
    "tether": "USDT",
    "binancecoin": "BNB",
    "solana": "SOL",
    "ripple": "XRP",
    "usd-coin": "USDC",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "avalanche-2": "AVAX",
    "tron": "TRX",
    "chainlink": "LINK",
    "polkadot": "DOT",
    "polygon": "POL",
    "litecoin": "LTC",
    "bitcoin-cash": "BCH",
    "stellar": "XLM",
    "uniswap": "UNI",
    "cosmos": "ATOM",
    "ethereum-classic": "ETC"

}


def get_symbol(coin_id):

    return SYMBOLS.get(
        coin_id,
        None
    )