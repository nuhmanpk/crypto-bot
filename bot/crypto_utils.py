import cryptocompare
from .database import db
from currency_symbols import CurrencySymbols
from datetime import datetime
import requests
from .vars import COINGECKO_API_URL


async def get_crypto_price(symbol, user_id):
    user = await db.get_user(user_id)
    currency = user.get("currency")
    currency_symbol = CurrencySymbols.get_symbol(currency)
    price = cryptocompare.get_price(symbol.upper(), currency=currency)
    if price and symbol.upper() in price and currency in price[symbol.upper()]:
        return f"💰 The current price of {symbol.upper()} is {currency_symbol}{price[symbol.upper()][currency]:.2f}"
    return f"❌ Could not fetch the price for {symbol.upper()} in {currency}."


async def get_trending_cryptos(user_id):
    response = requests.get(f"{COINGECKO_API_URL}/search/trending")
    if response.status_code == 200:
        trending = response.json().get("coins", [])
        if trending:
            trending_list = [
                f"{index+1}. {coin['item']['name']} (`/price {coin['item']['symbol'].upper()}`)" for index, coin in enumerate(trending)
            ]
            return "🚀 **Trending :**\n\n" + "\n".join(trending_list)
    return "❌ Could not fetch trending cryptocurrencies."


async def get_crypto_historical(symbol, user_id, timeframe='day'):
    user = await db.get_user(user_id)
    currency = user.get("currency", "USD")
    currency_symbol = CurrencySymbols.get_symbol(currency)

    if timeframe == 'day':
        historical_data = cryptocompare.get_historical_price_day(
            symbol.upper(), currency=currency)
    elif timeframe == 'hour':
        historical_data = cryptocompare.get_historical_price_hour(
            symbol.upper(), currency=currency)
    else:
        return "❌ Invalid timeframe specified. Use 'day' or 'hour'."

    if historical_data:
        # Trim the response to the last 5 entries to avoid the message being too long
        historical_data = historical_data[-5:]
        historical_list = [
            f"📅 : {datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')} - 💵 : {currency_symbol}{data['close']:.2f}"
            for data in historical_data
        ]
        return f"📈 Historical Data for {symbol.upper()} ({timeframe}):\n\n" + "\n".join(historical_list)
    return f"❌ Could not fetch historical data for {symbol.upper()}."


async def get_coin_details(symbol):
    response = requests.get(f"{COINGECKO_API_URL}/coins/{symbol.lower()}")
    if response.status_code == 200:
        coin_data = response.json()
        if coin_data:
            details = (
                f"**{coin_data['name']} ({coin_data['symbol'].upper()})**\n"
                f"Market Cap Rank: {coin_data.get('market_cap_rank', 'N/A')}\n"
                f"Current Price: ${coin_data['market_data']['current_price']['usd']:.2f}\n"
                f"Market Cap: ${coin_data['market_data']['market_cap']['usd']:,}\n"
                f"24h Volume: ${coin_data['market_data']['total_volume']['usd']:,}\n"
                f"Homepage: {coin_data['links']['homepage'][0]}\n"
                f"More Info: {coin_data['links']['blockchain_site'][0]}\n"
            )
            return details
    return f"❌ Could not fetch details for {symbol.upper()}."


async def get_exchanges():
    response = requests.get(f"{COINGECKO_API_URL}/exchanges")
    if response.status_code == 200:
        exchanges = response.json()
        if exchanges:
            exchange_list = [
                f"{index+1}. {exchange['name']}" for index, exchange in enumerate(exchanges[:10])]
            return "📊 **Top 10 Exchanges:**\n\n" + "\n".join(exchange_list)
    return "❌ Could not fetch supported exchanges."


async def get_coin_market_data(symbol):
    response = requests.get(
        f"{COINGECKO_API_URL}/coins/{symbol.lower()}/market_chart?vs_currency=usd&days=1")
    if response.status_code == 200:
        market_data = response.json()
        if market_data:
            market_list = [
                f"Timestamp: {data[0]} - Price: ${data[1]:.2f}" for data in market_data.get("prices", [])[:10]
            ]
            return f"📊 **Market Data for {symbol.upper()}:**\n\n" + "\n".join(market_list)
    return f"❌ Could not fetch market data for {symbol.upper()}."
