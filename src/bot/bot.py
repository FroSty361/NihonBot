import discord
from discord.ext import commands
from discord import app_commands
from dataManagement.runtime_data_management import register_user
from botProcesses.bot_process_definitions import Processes
from botProcesses.kana_practice_process import KanaPracticeProcess
from botProcesses.icon_vocab_process import IconVocabProcess

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
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def docs(interaction: discord.Interaction):
    await interaction.response.send_message("Documentation At https://github.com/FroSty361/NihonBot")

@bot.tree.command(guild=TEST_GUILD, name="kana", description="Practice Kana")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def kana(interaction: discord.Interaction, amount: str, kana_type: str = 'b'):
    user = await register_user(interaction) # Or Just Get User If Already Registered In Dictionary

    if user.process != Processes.NONE:
        await send_user_already_in_process_error(interaction, user.process)

        return

    user.process = Processes.KANA_QUIZ_PRACTICE

    await interaction.response.send_message("Ok Lets Start!")

    user.CurrentProcess = KanaPracticeProcess(amount, kana_type)

    await user.CurrentProcess.create_question(interaction)

@bot.tree.command(guild=TEST_GUILD, name="icon_vocab", description="Practice Vocabulary With Icons")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def icon_vocab(interaction: discord.Interaction, amount: str, use_furigana: bool):
    user = await register_user(interaction) # Or Just Get User If Already Registered In Dictionary

    if user.process != Processes.NONE:
        await send_user_already_in_process_error(interaction, user.process)

        return

    user.process = Processes.ICON_VOCAB_QUIZ_PRACTICE

    await interaction.response.send_message("Ok Lets Start!")

    user.CurrentProcess = IconVocabProcess(amount, use_furigana)

    await user.CurrentProcess.create_question(interaction)

# Comment

async def send_user_already_in_process_error(interaction: discord.Interaction, currentProcess):
    await interaction.response.send_message(f"User Already In Process {currentProcess.value}", ephemeral=True)