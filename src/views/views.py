import discord
from typing import Optional
from botProcesses.bot_processes import KanaPracticeProcess

class KanaPracticeView(discord.ui.View):
    labelOne = "1"
    labelTwo = "2"
    labelThree = "3"
    labelFour = "4"
    labelFive = "5"

    kanaPracticeProcess: Optional[KanaPracticeProcess] = None

    def __init__(self, kana_practice_process: KanaPracticeProcess):
        super().__init__(timeout=None)

        self.kanaPracticeProcess = kana_practice_process

        if self.kanaPracticeProcess is None:
            print("KanaPracticeProcess is None. Cannot Create KanaPracticeView")

            return

        if not self.kanaPracticeProcess.currentAnswersForQuestion:
            print("KanaPracticeProcess.currentAnswersForQuestion is None. Creating Answers")

            self.kanaPracticeProcess.create_question()

        # Make Buttons

        self.create_answer_buttons()

        self.create_stop_button()

    # Buttons

    def create_answer_buttons(self):
        for i in range(5): # Five Possible Answers
            answer_label = self.kanaPracticeProcess.currentAnswersForQuestion[i][1]

            answer_button = discord.ui.Button(label=answer_label, style=discord.ButtonStyle.primary, custom_id=f"kana_answer_button_{i}")

            answer_button.callback = self.create_answer_button_callback(answer_label, self.kanaPracticeProcess.currentAnswersForQuestion[i][2])

            self.add_item(answer_button)

    def create_answer_button_callback(self, answer_label, is_answer: bool):
        async def answer_button_callback(interaction: discord.Interaction):
            message = self.kanaPracticeProcess.answer_question(is_answer)

            await interaction.response.send_message(message, ephemeral=True)

            await interaction.response.send_message(f"{answer_label}", ephemeral=True)

        return answer_button_callback

    def create_stop_button(self):
        stop_button = discord.ui.Button(label="Stop", style=discord.ButtonStyle.primary, custom_id=f"kana_stop_button")

        stop_button.callback = self.create_stop_button_callback()

        self.add_item(stop_button)

    def create_stop_button_callback(self):
        async def stop_button_callback(interaction: discord.Interaction):
            message = self.kanaPracticeProcess.stop_process()

            await interaction.response.send_message(message, ephemeral=True)

        return stop_button_callback