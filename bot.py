import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

    print(f"Logged In As A Bot {bot.user}")

@bot.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi!")

bot.run(TOKEN)