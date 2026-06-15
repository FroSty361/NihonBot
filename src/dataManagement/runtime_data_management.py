from dataclasses import dataclass, field
from typing import Optional
from botProcesses.bot_processes import Processes, KanaPracticeProcess

users_runtime_data: dict[int, UserRuntimeData] = {}

# Models

@dataclass
class UserRuntimeData:
    username: str

    process: Processes = Processes.NONE

    KanaPracticeProcess: Optional[KanaPracticeProcess] = None