import os
from dotenv import load_dotenv
from .bot.bot import bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise RuntimeError("No DISCORD_TOKEN Set")

bot.run(TOKEN)