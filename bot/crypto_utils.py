import cryptocompare
from .database import db
from currency_symbols import CurrencySymbols


# Fetch the current price of a cryptocurrency
async def get_crypto_price(symbol,user_id):
    user = await db.get_user(user_id)
    currency=user.get("currency")
    currency_symbol = CurrencySymbols.get_symbol(currency)
    price = cryptocompare.get_price(symbol.upper(), currency=currency)
    if price and symbol.upper() in price and currency in price[symbol.upper()]:
        return f"The current price of {symbol.upper()} is {currency_symbol}{price[symbol.upper()][currency]:.2f}"
    return f"Could not fetch the price for {symbol.upper()} in {currency}."

# Fetch trending cryptocurrencies
async def get_trending_cryptos(user_id):
    trending = cryptocompare.get_exchanges()
    print("📱 ~ crypto_utils.py:15 -> trending: ",  trending)
    if trending:
        trending_list = [f"{coin['FullName']} ({coin['Name']})" for coin in trending]
        return "Trending Cryptocurrencies:\n" + "\n".join(trending_list)
    return "Could not fetch trending cryptocurrencies."

# Fetch historical data for a cryptocurrency
async def get_crypto_historical(symbol, user_id,timeframe='day'):
    user = await db.get_user(user_id)
    if timeframe == 'day':
        historical_data = cryptocompare.get_historical_price_day(symbol.upper(), currency=user.get("currency"))
    elif timeframe == 'hour':
        historical_data = cryptocompare.get_historical_price_hour(symbol.upper(), currency=user.get("currency"))
    else:
        return "Invalid timeframe specified. Use 'day' or 'hour'."

    if historical_data:
        historical_list = [f"Date: {data['time']} - Price: ${data['close']}" for data in historical_data]
        return f"Historical Data for {symbol.upper()} ({timeframe}):\n" + "\n".join(historical_list)
    return f"Could not fetch historical data for {symbol.upper()}."
