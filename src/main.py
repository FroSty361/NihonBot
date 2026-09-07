import os
from dotenv import load_dotenv
from bot.bot import bot
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == "__main__":
    keep_alive()

    bot.run(TOKEN)