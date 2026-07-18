import discord
import random
from views.views import QuizPracticeView
from botProcesses.bot_process_constants import hiragana, katakana
from botProcesses.bot_process_definitions import Processes, BaseQuizProcess

class KanaPracticeProcess(BaseQuizProcess):
    def __init__(self, amount: str, kana_type: str):
        super().__init__(amount, Processes.KANA_QUIZ_PRACTICE)

        self.usedHiragana = []
        self.usedKatakana = []

        amount = amount.lower()

        kana_type = kana_type.lower()

        if kana_type == "h": # h For Hiragana
            self.practicingHiragana = True
            self.practicingKatakana = False
        elif kana_type == "k": # k For Katakana
            self.practicingHiragana = False
            self.practicingKatakana = True
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

        view = QuizPracticeView(self, interaction)

        await view.display_question(interaction, self.processType)

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