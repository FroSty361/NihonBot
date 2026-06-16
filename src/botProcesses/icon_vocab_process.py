import discord
from botProcesses.bot_process_definitions import Processes, BaseQuizProcess


class IconVocabProcess(BaseQuizProcess):
    def __init__(self, amount: str, use_furigana: bool):
        super().__init__(amount, Processes.ICON_VOCAB_QUIZ_PRACTICE)

        self.amount = amount
        self.isIndefiniteAmount = False
        self.amountCompleted = 0
        self.amountCorrect = 0

        self.useFurigana = use_furigana