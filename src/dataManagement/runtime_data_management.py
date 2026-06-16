import discord
from dataclasses import dataclass, field
from typing import Optional
from botProcesses.bot_processes import Processes, KanaPracticeProcess

users_runtime_data: dict[int, UserRuntimeData] = {}

async def register_user(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in users_runtime_data:
        users_runtime_data[user_id] = UserRuntimeData(username=interaction.user.name)

    return users_runtime_data[user_id]

# Models

@dataclass
class UserRuntimeData:
    username: str

    process: Processes = Processes.NONE

    KanaPracticeProcess: Optional[KanaPracticeProcess] = None