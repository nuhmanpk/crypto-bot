from .admin import add_user
from .buttons import HELP_BUTTONS, START_BUTTONS, ABOUT_BUTTONS
from .constants import START_TEXT, HELP_TEXT, ABOUT_TEXT
from .crypto_utils import (get_crypto_price, get_crypto_historical,
                           get_trending_cryptos, get_coin_details, get_exchanges, get_coin_market_data)
from .database import db
from pyrogram import Client, filters


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=START_TEXT,
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True
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
        quote=True
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
        quote=True
    )


@Client.on_message(filters.private & filters.command(["price"]))
async def price(bot, message):
    txt = await message.reply('⏳ Fetching Latest results for You !!')
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        user_id = message.from_user.id
        response = await get_crypto_price(symbol, user_id)
    else:
        response = "Please specify a cryptocurrency symbol. Usage: /price <symbol>"
    await message.reply_text(response, quote=True)
    await txt.delete()


@Client.on_message(filters.private & filters.command(["trending"]))
async def trending(bot, message):
    txt = await message.reply('⏳ Fetching the latest trending cryptocurrencies...')
    user_id = message.from_user.id
    response = await get_trending_cryptos(user_id)
    await txt.delete()
    await message.reply_text(response, quote=True)


@Client.on_message(filters.private & filters.command(["historical"]))
async def historical(bot, message):
    if len(message.command) < 3:
        await message.reply_text("Usage: /historical <symbol> [day/hour]")
        return

    txt = await message.reply_text('⏳ Fetching historical data...')

    symbol = message.command[1].upper()
    timeframe = message.command[2].lower()
    user_id = message.from_user.id

    historical_data = await get_crypto_historical(symbol, user_id, timeframe)
    await txt.delete()
    await message.reply_text(historical_data)


@Client.on_message(filters.private & filters.command(["coin"]))
async def price(bot, message):
    txt = await message.reply('⏳ Fetching Latest Coin details for You !!')
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        response = await get_coin_details(symbol)
    else:
        response = "Please specify a cryptocurrency symbol. Usage: /price <symbol>"
    await message.reply_text(response, quote=True, disable_web_page_preview=True)
    await txt.delete()


@Client.on_message(filters.private & filters.command(["exchanges"]))
async def exchanges(bot, message):
    txt = await message.reply('⏳ Fetching supported exchanges...')
    response = await get_exchanges()
    await message.reply_text(response, quote=True)
    await txt.delete()


@Client.on_message(filters.private & filters.command(["market_data"]))
async def coin_market_data(bot, message):
    txt = await message.reply('⏳ Fetching market data...')
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        user_id = message.from_user.id
        response = await get_coin_market_data(symbol)
        await txt.delete()
    else:
        response = "Please specify a cryptocurrency symbol. Usage: /market_data <symbol>"
        await txt.delete()
    await message.reply_text(response, quote=True)
