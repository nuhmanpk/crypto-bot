from .database import db
from .admin import add_user
from pyrogram import Client, filters
from .buttons import HELP_BUTTONS, START_BUTTONS, ABOUT_BUTTONS
from .constants import START_TEXT, HELP_TEXT, ABOUT_TEXT
from .crypto_utils import get_crypto_price, get_crypto_historical, get_trending_cryptos


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
    txt = await message.reply('Fetching Latest results for You !!')
    symbol = message.command[1] if len(message.command) > 1 else None
    if symbol:
        user_id = message.from_user.id
        response = await get_crypto_price(symbol, user_id)
        await txt.delete()
    else:
        response = "Please specify a cryptocurrency symbol. Usage: /price <symbol>"
        await txt.delete()
    await message.reply_text(response, quote=True)


@Client.on_message(filters.private & filters.command(["trending"]))
async def trending(bot, message):
    txt = await message.reply_text('Fetching Latest results for you...')
    user_id = message.from_user.id
    response = await get_trending_cryptos(user_id)
    await txt.edit_text(response)


@Client.on_message(filters.private & filters.command(["historical"]))
async def historical(bot, message):
    symbol = message.command[1] if len(message.command) > 1 else None
    timeframe = message.command[2] if len(message.command) > 2 else 'day'
    if symbol:
        user_id = message.from_user.id
        response = await get_crypto_historical(symbol, user_id, timeframe)
    else:
        response = "Please specify a cryptocurrency symbol and optional timeframe. Usage: /historical <symbol> [day/hour]"
    await message.reply_text(response, quote=True)
