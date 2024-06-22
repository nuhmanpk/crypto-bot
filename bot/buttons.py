from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .currency import CURRENCY_FLAGS, TRENDING_CURRENCIES


def generate_currency_buttons():
    buttons = []
    for currency in TRENDING_CURRENCIES:
        flag = CURRENCY_FLAGS.get(currency, "")
        buttons.append(InlineKeyboardButton(
            f"{flag} {currency}", callback_data=f"currency:{currency}"))

    button_rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

    button_rows.append([InlineKeyboardButton(
        "Back", callback_data="settings:back")])

    return InlineKeyboardMarkup(button_rows)


START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help 🆘', callback_data='help'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Settings ⚙️', callback_data='settings'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Settings ⚙️', callback_data='settings'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('Help 🆘', callback_data='help'),
            InlineKeyboardButton('Settings ⚙️', callback_data='settings'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

SETTINGS_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "Change Currency", callback_data="settings:change_currency")
    ],
    [
        InlineKeyboardButton("Close", callback_data="settings:close")
    ]
])

CURRENCY_BUTTONS = generate_currency_buttons()

CLOSE_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Close', callback_data='close')]])
