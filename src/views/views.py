import discord
from typing import Optional
from botProcesses.bot_process_definitions import BaseQuizProcess, Processes
from emoji import emojize, analyze


class QuizPracticeView(discord.ui.View):
    # Constants

    ANSWER_BUTTON_ID_STRING = "kana_answer_button_"
    STOP_BUTTON_ID_STRING = "kana_stop_button_"

    # Labels

    labelOne = "1"
    labelTwo = "2"
    labelThree = "3"
    labelFour = "4"
    labelFive = "5"

    botProcess = None

    def __init__(self, bot_process: BaseQuizProcess, interaction: discord.Interaction):
        super().__init__(timeout=None)

        self.botProcess = bot_process

        if self.botProcess is None:
            print(f"{self.botProcess} is None. Stopping Process")

            return

        if not self.botProcess.currentAnswersForQuestion:
            print(f"Current Answers For Question In {self.botProcess} Is None. Stopping Process")

            return

        # Make Buttons

        self.create_answer_buttons()

        self.create_stop_button()

    async def display_question(self, interaction: discord.Interaction, process_type: Processes):
        correct_answer = next((item for item in self.botProcess.currentAnswersForQuestion if item[2] == True), None)

        match process_type:
            case Processes.KANA_QUIZ_PRACTICE:
                await interaction.followup.send(f"What Is Romaji For {correct_answer[0]}?", view=self)
            case Processes.ICON_VOCAB_QUIZ_PRACTICE:
                await interaction.followup.send(f"What Is Vocabulary From {correct_answer[0]}?", view=self)
            case _:
                print(f"Process Type For Displaying Question In Quiz Practice View Is Not Supported, {process_type.value}")

    # Buttons

    def create_answer_buttons(self):
        for i in range(5): # Five Possible Answers
            answer_label_str = self.botProcess.currentAnswersForQuestion[i][1]

            answer_label = emojize(f"{answer_label_str}", language='alias')

            answer_button = discord.ui.Button(label=answer_label, style=discord.ButtonStyle.primary, custom_id=f"{self.ANSWER_BUTTON_ID_STRING}{i}")

            answer_button.callback = self.create_answer_button_callback(answer_label, self.botProcess.currentAnswersForQuestion[i][2])

            self.add_item(answer_button)

    def create_answer_button_callback(self, answer_label, is_answer: bool):
        async def answer_button_callback(interaction: discord.Interaction):
            buttons = self.get_buttons()

            for button in buttons:
                button.disabled = True

            await interaction.response.edit_message(view=self)

            response = await self.botProcess.answer_question(is_answer, interaction) # Returns Message And If Practice Questions Have Ended
            await interaction.followup.send(response[0], ephemeral=(not response[1]))

            if response[1] == False:
                await self.botProcess.create_question(interaction)

        return answer_button_callback

    def create_stop_button(self):
        stop_button = discord.ui.Button(label="Stop", style=discord.ButtonStyle.primary, custom_id=self.STOP_BUTTON_ID_STRING)

        stop_button.callback = self.create_stop_button_callback()

        self.add_item(stop_button)

    def create_stop_button_callback(self):
        async def stop_button_callback(interaction: discord.Interaction):
            buttons = self.get_buttons()

            for button in buttons:
                button.disabled = True

            message = await self.botProcess.stop_process(interaction)

            await interaction.response.send_message(message, ephemeral=False)

        return stop_button_callback

    # Helper

    def get_buttons(self, answer_buttons: bool = True, stop_button: bool = True):
        buttons: list[discord.ui.Button] = []

        for child in self.children:
            if not isinstance(child, discord.ui.Button):
                continue

            _id = str(child.custom_id)

            if stop_button and _id == self.STOP_BUTTON_ID_STRING:
                buttons.append(child)

                continue

            if answer_buttons and _id.startswith(self.ANSWER_BUTTON_ID_STRING):
                buttons.append(child)

        return buttons