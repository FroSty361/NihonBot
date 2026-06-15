import os
from dotenv import load_dotenv
from bot.bot import bot

load_dotenv()
TOKEN = os.getenv('TOKEN')

if __name__ == "__main__":
    bot.run(TOKEN)