import discord
from enum import Enum
import random
from views.views import KanaPracticeView
from bot_process_constants import hiragana, katakana

class Processes(Enum):
    NONE = "None"
    KANA_PRACTICE = "Kana"

class KanaPracticeProcess():
    def __init__(self, amount: str, kana_type: str):
        self.amount = amount
        self.isIndefiniteAmount = False
        self.amountCompleted = 0
        self.amountCorrect = 0
        self.usedHiragana = []
        self.usedKatakana = []
        self.currentAnswersForQuestion = []

        amount = amount.lower()

        if amount == "indef": # For Indefinite Amount
            self.isIndefiniteAmount = True
        elif self.string_is_int(amount):
            self.isIndefiniteAmount = False

            self.amount = int(amount)

            if self.amount <= 0:
                print("Kana Practice Process Was Less Than Or Equal To Zero. Setting To 16")

                self.amount = 16
        else:
            self.isIndefiniteAmount = True

        kana_type = kana_type.lower()

        if kana_type == "h": # h For Hiragana
            self.practicingKatakana = False
        elif kana_type == "k": # k For Katakana
            self.practicingHiragana = False
        else:
            self.practicingHiragana = True
            self.practicingKatakana = True

    async def create_question(self, interaction: discord.Interaction):
        if self.practicingHiragana == False and self.practicingKatakana == False:
            print("Says Practicing Both Hiragana And Katakana Is False. Setting Both To True")

            self.practicingHiragana = True
            self.practicingKatakana = True

        if self.currentAnswersForQuestion is None:
            self.currentAnswersForQuestion = []

        self.currentAnswersForQuestion.clear()

        for i in range(5): # Five Possible Answers
            is_answer = i == 0

            if random.random() < 0.5: # Hiragana
                hiragana_answer = self.get_hiragana_question(is_answer)

                self.currentAnswersForQuestion.append(hiragana_answer)

                self.usedHiragana.append(hiragana_answer[0])
            else: # Katakana
                katakana_answer = self.get_katakana_question(is_answer)

                self.currentAnswersForQuestion.append(katakana_answer)

                self.usedKatakana.append(katakana_answer[0])

        self.currentAnswersForQuestion = random.sample(self.currentAnswersForQuestion, len(self.currentAnswersForQuestion)) # Shuffle

        view = KanaPracticeView(self, interaction)

        await view.display_question(interaction)

    def get_hiragana_question(self, is_answer: bool):
        used_hiragana_set = set(self.usedHiragana)
        usable_hiragana = [kana for kana in hiragana.keys() if kana not in used_hiragana_set]

        if usable_hiragana == [] or len(usable_hiragana) <= 0:
            used_hiragana_set.clear()
            usable_hiragana = [kana for kana in hiragana.keys() if kana not in used_hiragana_set]

        hiragana_key = random.choice(usable_hiragana)

        return (hiragana_key, hiragana[hiragana_key], is_answer)

    def get_katakana_question(self, is_answer: bool):
        used_katakana_set = set(self.usedKatakana)
        usable_katakana = [kana for kana in katakana.keys() if kana not in used_katakana_set]

        if usable_katakana == [] or len(usable_katakana) <= 0:
            used_katakana_set.clear()
            usable_katakana = [kana for kana in katakana.keys() if kana not in used_katakana_set]

        katakana_key = random.choice(usable_katakana)

        return (katakana_key, katakana[katakana_key], is_answer)

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

        if self.isIndefiniteAmount == False:
            returnMessage += f"{self.amount - self.amountCompleted} Questions Left \n"

        ended = False

        if self.isIndefiniteAmount == False and self.amountCompleted >= self.amount:
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

    def string_is_int(self, s : str):
        if s[0] in ('-', '+'):
            return s[1:].isdigit()

        return s.isdigit()