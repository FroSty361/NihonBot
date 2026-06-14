import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

TEST_GUILD = discord.Object(id=1515433987105886298)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=TEST_GUILD)

        print(f"Synced {len(synced)} Command(s)")
    except Exception as e:
        print(f"Failed To Sync: {e}")

    print(f"Logged In As A Bot {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandNotFound):
        pass

@bot.tree.command(guild=TEST_GUILD, name="docs", description="Provides A Link To The Documentation")
@commands.guild_only()
async def docs(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.id} Documentation At https://github.com/FroSty361/NihonBot")

bot.run(TOKEN)