# Crypto-Bot

Crypto-Bot is a Ope source Telegram bot built using Pyrogram that allows users to fetch the latest cryptocurrency prices, trending cryptocurrencies, and historical data. The bot also supports user-specific settings such as preferred currency for price display.

<img src='./assets//demo.gif' width=310px height=600px>

## Features

- **Fetch Current Prices:** Get the latest price of any cryptocurrency in your preferred currency.
- **Trending Cryptocurrencies:** View the top 10 trending cryptocurrencies.
- **Historical Data:** Fetch historical price data for cryptocurrencies by day or hour.
- **User Settings:** Set and update your preferred currency for price displays.
- **Live Price Fetching** : Get live datas instantly.
- **Inline Keyboard Support:** Use inline keyboards for easy navigation and settings adjustments.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/nuhmanpk/crypto-bot.git
    cd crypto-bot
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment variables:**

    Create a `.env` file in the root directory of the project and add your bot token, API ID, and API hash:

    ```env
    BOT_TOKEN=your-bot-token
    API_ID=your-api-id
    API_HASH=your-api-hash
    DATABASE_URL=your-database-url
    DATABASE_NAME=your-database-name
    SESSION_STRING=your-session-string
    ADMINS = 1234556
    ```
    - Generate `SESSION_STRING` from [here](https://gist.github.com/nuhmanpk/5b2b29fcecd479754c599c36c0961363)
    - Get `DATABASE_URL` url from [here](https://mongodb.com)
    - Get `API_ID` and `API_HASH` from [here](https://api.telegram.org)
    - Give a `DATABASE_NAME` as you wish
    - Get `BOT_TOKEN` from [here](https://t.me/botfather)
    - Add user id of admins as `ADMINS` serperated by whitespaces.

## Usage

1. **Run the bot:**

    ```bash
    python main.py
    ```

<img src='./assets/logo.jpeg' max-width=25px max-height=25px/>

2. **Interact with the bot:**

    - **/start**: Start the bot and see the welcome message.
    - **/help**: Get help information about the bot's commands.
    - **/price [symbol]**: Get the current price of the specified cryptocurrency.
    - **/trending**: View the top 10 trending cryptocurrencies.
    - **/historical [symbol] [timeframe]**: Get historical data for the specified cryptocurrency and timeframe (day or hour).
    - **/live_prices** - Fetch Live Price
    - **/exchange [symbol]** - Get exchange details.
    - **/exchange_rates** -  Get all exchange dates.
    - **/exchanges** -  Get all exchanges.
    - **/coin** -  Get all coin details.
    - **/setcurrency [currency_code]**: Set your preferred currency for price displays.
    - **Settings ⚙️**: Use the settings button to change preferences like your preferred currency.
    - And [more](https://t.me/bughunterbots) ...

- If you find this bot useful mark your star and fell free to contribute

Happy Coding! 🚀

Built with ❤️ by Nuhman Pk © 2024
