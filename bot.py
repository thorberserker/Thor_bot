from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I AM THOR! THE GOD OF MEMES AND MOONSHOT COINS!")

app = ApplicationBuilder().token("7783798993:AAGYBOm89p_AEeTCfqjRtjgx38oM4BayxX8").build()
app.add_handler(CommandHandler("hello", hello))

app.run_polling()

from telegram.ext import MessageHandler, filters

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I heard you, mortal!")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# bot.py
import secrets
import random
import openai
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set the OpenAI API key
openai.api_key = secrets.OPENAI_API_KEY

# Helper function to get price data for a coin (using CoinGecko API)
def get_coin_price(coin_name):
    url = f"{secrets.COINGECKO_API_URL}/simple/price?ids={coin_name}&vs_currencies=usd"
    response = requests.get(url).json()
    if coin_name in response:
        return f"Thor says: '{coin_name.upper()} is mighty today! Current price: ${response[coin_name]['usd']}.'"
    return "Thor sees no coin in the digital sea, try again with a valid coin!"

# Helper function to get token data from DexScreener (for Solana network)
def get_dextools_info(token_address):
    url = f"{secrets.DEXSCREENER_API_URL}/solana/{token_address}"
    response = requests.get(url).json()
    if 'pairs' in response and len(response['pairs']) > 0:
        pair = response['pairs'][0]
        return f"Thor says: '{pair['baseToken']['name']} ({pair['baseToken']['symbol']}) is looking mighty! Price: ${pair['priceUsd']}, Liquidity: ${pair['liquidity']['usd']}'"
    return "Thor sees no coin in the digital sea, try again with a token address!"

# Helper function to generate Thor's drunken prophecy (ChatGPT)
def get_thor_prophecy():
    prompt = "Thor, the drunk Viking god of thunder, wakes up from a nap and rants about the future of cryptocurrency. He speaks in a loud, incoherent manner with a lot of dramatic flair."
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can adjust the engine for better results
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Helper function for drunken rants
def get_drunk_rant():
    rants = [
        "By Odin's beard, I can't tell if the market is going up or down, but I’ll grab my mead anyway!",
        "Ragnarok has come for the market... wait, what market was I talking about again?",
        "Satoshi, you trickster! You made this coin explode! Now I see a Doge moon… or was it just a hallucination?",
        "Valhalla's out there, just past Mars… or was it just a space pizza delivery? I forget."
    ]
    return random.choice(rants)

# Commands for the bot to respond to
async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin_name = context.args[0] if context.args else "dogecoin"  # Default to Dogecoin if no coin is mentioned
    price = get_coin_price(coin_name)
    await update.message.reply_text(price)

async def dextools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Thor says: 'Give me a token address and I’ll see if it’s worth the voyage!'")
        return
    token_address = context.args[0]
    info = get_dextools_info(token_address)
    await update.message.reply_text(info)

async def prophecy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prophecy = get_thor_prophecy()
    await update.message.reply_text(f"Thor’s Prophecy: {prophecy}")

async def drunk_rant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rant = get_drunk_rant()
    await update.message.reply_text(f"Thor’s Rant: {rant}")

# Telegram bot setup
async def main():
    app = ApplicationBuilder().token("your-telegram-bot-token-here").build()

    # Add handlers for commands
    app.add_handler(CommandHandler("coin", coin))
    app.add_handler(CommandHandler("dextools", dextools))
    app.add_handler(CommandHandler("prophecy", prophecy))
    app.add_handler(CommandHandler("rant", drunk_rant))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



