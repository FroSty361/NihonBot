import discord
import random
from views.views import VCQuizPracticeView
from botProcesses.bot_process_constants import vc_vocab_furigana, vc_vocab_kanji, vc_vocab_english
from botProcesses.bot_process_definitions import Processes, BaseQuizProcess

class VCVocabPracticeProcess(BaseQuizProcess):
    def __init__(self, amount: str, text_type: str):
        super().__init__(amount, Processes.VC_VOCAB_QUIZ_PRACTICE)

        self.text_type = text_type

        self.usedFurigana = []
        self.usedKanji = []
        self.usedEnglish = []

    async def create_question(self, interaction: discord.Interaction, vc = None):
        if self.currentAnswersForQuestion is None:
            self.currentAnswersForQuestion = []

        self.currentAnswersForQuestion.clear()

        for i in range(5): # Five Possible Answers
            is_answer = i == 0

            if self.text_type == "english":
                english_answer = self.get_english_question(is_answer)

                self.currentAnswersForQuestion.append(english_answer)

                self.usedEnglish.append(english_answer[0])
            elif self.text_type == "kanji":
                kanji_answer = self.get_kanji_question(is_answer)

                self.currentAnswersForQuestion.append(kanji_answer)

                self.usedKanji.append(kanji_answer[0])
            else:
                furigana_answer = self.get_furigana_question(is_answer)

                self.currentAnswersForQuestion.append(furigana_answer)

                self.usedFurigana.append(furigana_answer[0])

        self.currentAnswersForQuestion = random.sample(self.currentAnswersForQuestion, len(self.currentAnswersForQuestion)) # Shuffle

        view = VCQuizPracticeView(self, interaction, vc)

        await view.display_question(interaction, self.processType)

    def get_furigana_question(self, is_answer: bool):
        used_furigana_set = set(self.usedFurigana)
        usable_furigana = [kana for kana in vc_vocab_furigana.keys() if kana not in used_furigana_set]

        if usable_furigana == [] or len(usable_furigana) <= 0:
            used_furigana_set.clear()
            usable_furigana = [kana for kana in vc_vocab_furigana.keys() if kana not in used_furigana_set]

        furigana_key = random.choice(usable_furigana)

        return (vc_vocab_furigana[furigana_key], furigana_key, is_answer)

    def get_kanji_question(self, is_answer: bool):
        used_kanji_set = set(self.usedKanji)
        usable_kanji = [kanji for kanji in vc_vocab_kanji.keys() if kanji not in used_kanji_set]

        if usable_kanji == [] or len(usable_kanji) <= 0:
            used_kanji_set.clear()
            usable_kanji = [kanji for kanji in vc_vocab_kanji.keys() if kanji not in used_kanji_set]

        kanji_key = random.choice(usable_kanji)

        return (vc_vocab_kanji[kanji_key], kanji_key, is_answer)

    def get_english_question(self, is_answer: bool):
        used_english_set = set(self.usedEnglish)
        usable_english = [word for word in vc_vocab_english.keys() if word not in used_english_set]

        if usable_english == [] or len(usable_english) <= 0:
            used_english_set.clear()
            usable_english = [word for word in vc_vocab_english.keys() if word not in used_english_set]

        english_key = random.choice(usable_english)

        return (vc_vocab_english[english_key], english_key, is_answer)