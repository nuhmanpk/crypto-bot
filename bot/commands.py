from .admin import add_user
from .buttons import HELP_BUTTONS, START_BUTTONS, ABOUT_BUTTONS
from .constants import START_TEXT, HELP_TEXT, ABOUT_TEXT
from .stickers import WAITING
import random
from .crypto_utils import (
    get_crypto_price,
    get_crypto_historical,
    get_trending_cryptos,
    get_coin_details,
    get_exchanges,
    get_coin_market_data,
    get_exchange_rates,
    get_coin_exchanges,
    fetch_live_prices,
    format_prices_message,
)
from .database import db
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from datetime import datetime, timedelta
import pytz


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=START_TEXT,
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )
    # await message.reply_photo(
    #     photo='',
    #     caption=START_TEXT,
    #     reply_markup=START_BUTTONS,
    #     quote=True
    # )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=HELP_TEXT,
        reply_markup=HELP_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=ABOUT_TEXT,
        reply_markup=ABOUT_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.private & filters.command(["trending"]))
async def trending(bot, message: Message):
    sticker = random.choice(WAITING)
    sticker_message = await message.reply_sticker(sticker)
    txt = await message.reply("⏳ Fetching the latest trending cryptocurrencies...")
    response = await get_trending_cryptos()
    await txt.delete()
    await sticker_message.delete()
    await message.reply_text(response, quote=True)


@Client.on_message(filters.private & filters.command(["price"]))
async def price(bot, message):
    txt = await message.reply("⏳ Fetching Latest results for You !!")
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        user_id = message.from_user.id
        response = await get_crypto_price(symbol, user_id)
    else:
        response = "Please specify a cryptocurrency symbol. Usage: `/price BTC`"
    await message.reply_text(response, quote=True)
    await txt.delete()

@Client.on_message(filters.private & filters.command(["historical"]))
async def historical(bot, message):
    if len(message.command) < 3:
        await message.reply_text(
            "Usage: `/historical BTC day` `/historical BTC hour`", quote=True
        )
        return

    txt = await message.reply_text("⏳ Fetching historical data...")

    symbol = message.command[1].upper()
    timeframe = message.command[2].lower()
    user_id = message.from_user.id

    historical_data = await get_crypto_historical(symbol, user_id, timeframe)
    await txt.delete()
    await message.reply_text(historical_data)


@Client.on_message(filters.private & filters.command(["coin"]))
async def coin(bot, message):
    txt = await message.reply("⏳ Fetching Latest Coin details for You !!")
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        response = await get_coin_details(symbol)
    else:
        response = "Please specify a cryptocurrency symbol. Usage: `/coin DOGECOIN`"
    await message.reply_text(response, quote=True, disable_web_page_preview=True)
    await txt.delete()


@Client.on_message(filters.private & filters.command(["exchanges"]))
async def exchanges(bot, message):
    txt = await message.reply("⏳ Fetching supported exchanges...")
    response = await get_exchanges()
    await message.reply_text(response, quote=True)
    await txt.delete()


@Client.on_message(filters.private & filters.command(["market_data"]))
async def coin_market_data(bot, message):
    txt = await message.reply("⏳ Fetching market data...")
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        response = await get_coin_market_data(symbol)
        await txt.delete()
    else:
        response = (
            "Please specify a cryptocurrency symbol. Usage: /market_data <symbol>"
        )
        await txt.delete()
    await message.reply_text(response, quote=True)


@Client.on_message(filters.private & filters.command(["exchange_rates"]))
async def exchange_rates(bot, message):
    txt = await message.reply("⏳ Fetching Exchange Rates for You !!")
    response = await get_exchange_rates()
    await message.reply_text(response, quote=True)
    await txt.delete()


@Client.on_message(filters.private & filters.command(["exchange"]))
async def coin_market_data(bot, message):
    txt = await message.reply("⏳ Fetching market data...")
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        response = await get_coin_exchanges(symbol)
        if not response:
            response = (
                "Please specify a cryptocurrency symbol. Usage: /exchange DOGECOIN"
            )
        await txt.delete()
    else:
        response = "Please specify a cryptocurrency symbol. Usage: /exchange DOGECOIN"
        await txt.delete()
    await message.reply_text(response, quote=True)


@Client.on_message(filters.private & filters.command(["live_prices"]))
async def live_prices(bot, message):
    sticker = random.choice(WAITING)
    sticker_message = await message.reply_sticker(sticker)
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    currency = user.get("currency", "usd")
    symbols = [
        "bitcoin",
        "ethereum",
        "binancecoin",
        "ripple",
        "cardano",
        "solana",
        "polkadot",
        "dogecoin",
        "shiba-inu",
        "litecoin",
    ]

    live_message = await message.reply_text(
        "🔄 Fetching live prices for popular coins..."
    )

    try:
        prev_prices = {symbol: None for symbol in symbols}  # Initialize previous prices

        start_time = datetime.now(pytz.utc)
        end_time = start_time + timedelta(minutes=2)
        last_update = start_time

        while datetime.now(pytz.utc) < end_time:
            current_prices = await fetch_live_prices(symbols, currency)
            if not current_prices:
                await asyncio.sleep(10)  # Wait for 10 seconds before retrying
                continue

            formatted_message = format_prices_message(
                symbols, current_prices, prev_prices
            )

            # Update message only if the last update time has changed
            current_time = datetime.now(pytz.utc)
            if current_time > last_update:
                updated_message = f"{formatted_message}\n\n🕒 Updated on: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"

                try:
                    await live_message.edit_text(updated_message)
                    last_update = current_time
                except Exception as e:
                    print(f"❌ Error occurred while updating message: {e}")

            await asyncio.sleep(10)
            prev_prices = current_prices

    except asyncio.CancelledError:
        pass

    except Exception as e:
        print(f"❌ Error occurred: {e}")

    await live_message.edit_text(
        "⏹️ Live price updates stopped."
    )
    await sticker_message.delete()  
