from bot.buttons import SETTINGS_BUTTONS
from .admin import add_user
from pyrogram import Client, filters
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, message):
    await message.message.delete()
    await add_user(message.from_user.id)
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    elif message.data == "settings":
        await message.message.reply('TODO: Settings')
    elif message.data == "close":
        await message.message.delete()


@Client.on_message(filters.private & filters.command(["settings"]))
async def settings(bot, message):
    await message.reply_text(
        "Settings:",
        reply_markup=SETTINGS_BUTTONS
    )
