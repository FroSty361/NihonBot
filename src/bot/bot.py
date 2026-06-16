import discord
from discord.ext import commands
from dataManagement.runtime_data_management import users_runtime_data, UserRuntimeData
from botProcesses.bot_processes import Processes, KanaPracticeProcess

intents = discord.Intents.all()
intents.message_content = True
intents.messages = True

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
async def docs(interaction: discord.Interaction):
    user = await register_user(interaction)

    await interaction.response.send_message(f"@{user.username} Documentation At https://github.com/FroSty361/NihonBot")

@bot.tree.command(guild=TEST_GUILD, name="kana", description="Practice Kana")
async def kana(interaction: discord.Interaction, amount: str, kana_type: str = 'b'):
    user = await register_user(interaction)

    if user.process != Processes.NONE:
        await send_user_already_in_process_error(interaction, user.process)

        return

    user.process = Processes.KANA_PRACTICE

    await interaction.response.send_message("Ok Lets Start!")

    user.KanaPracticeProcess = KanaPracticeProcess(amount, kana_type)

    await user.KanaPracticeProcess.create_question(interaction)

# User Logic

async def register_user(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in users_runtime_data:
        users_runtime_data[user_id] = UserRuntimeData(username=interaction.user.name)

    return users_runtime_data[user_id]

# Comment

async def send_user_already_in_process_error(interaction: discord.Interaction, currentProcess):
    await interaction.response.send_message(f"User Already In Process {currentProcess.value}", ephemeral=True)