import discord
from enum import Enum

class Processes(Enum):
    NONE = "None",
    KANA_QUIZ_PRACTICE = "Kana Quiz Practice",
    ICON_VOCAB_QUIZ_PRACTICE = "Icon Vocab Quiz Practice"

class BaseQuizProcess:
    def __init__(self, amount: str, process_type: Processes):
        self.processType = process_type

        self.amount = amount
        self.isIndefiniteAmount = False
        self.amountCompleted = 0
        self.amountCorrect = 0

        self.currentAnswersForQuestion = []

    def __str__(self):
        return f"{self.processType.value}"

    async def create_question(self, interaction: discord.Interaction):
        print("Should Be Overridden")

    async def answer_question(self, is_answer: bool, interaction: discord.Interaction):
        self.amountCompleted += 1

        correct_answer = next((item for item in self.currentAnswersForQuestion if item[2] == True), None)

        returnMessage = ""

        if is_answer:
            self.amountCorrect += 1

            returnMessage = "Correct! \n"
        else:
            returnMessage = f"Incorrect! The Correct Answer Of {correct_answer[0]} Is {correct_answer[1]} \n"

        returnMessage += f"{self.amountCorrect} Correct Out Of {self.amountCompleted} \n"

        completed = self.isIndefiniteAmount == False and self.amountCompleted >= self.amount

        if self.isIndefiniteAmount == False and completed == False:
            returnMessage += f"{self.amount - self.amountCompleted} Question(s) Left \n"

        ended = False

        if completed:
            ended = True

            returnMessage += await self.stop_process(interaction)

        return (returnMessage, ended)

    async def stop_process(self, interaction: discord.Interaction):
        stop_process_message = ""

        user_id = interaction.user.id

        if self.isIndefiniteAmount:
            try:
                percent_correct = round((self.amountCorrect / self.amountCompleted) * 100, 3)

                stop_process_message = f"<@{user_id}> Completed! You Got {self.amountCorrect} Out Of {self.amountCompleted}! That Is {percent_correct} Percent Correct"
            except ZeroDivisionError:
                stop_process_message = f"<@{user_id}> Completed! You Got {self.amountCorrect} Out Of {self.amountCompleted}!"
        else:
            try:
                percent_correct = round((self.amountCorrect / self.amount) * 100, 3)

                stop_process_message = f"<@{user_id}> Completed! You Got {self.amountCorrect} Out Of {self.amount}! That Is {percent_correct} Percent Correct!"
            except ZeroDivisionError:
                stop_process_message = f"<@{user_id}> Completed! You Got {self.amountCorrect} Out Of {self.amount}!"

        from dataManagement.runtime_data_management import register_user
        user = await register_user(interaction)

        user.process = Processes.NONE

        return stop_process_message

    # Helpers

    def string_is_int(self, s: str):
        if s[0] in ('-', '+'):
            return s[1:].isdigit()

        return s.isdigit()