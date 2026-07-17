import discord
import random
from views.views import VCQuizPracticeView
from botProcesses.bot_process_constants import vc_vocab_furigana, vc_vocab_kanji
from botProcesses.bot_process_definitions import Processes, BaseQuizProcess

class VCVocabPracticeProcess(BaseQuizProcess):
    def __init__(self, amount: str, use_furigana: bool):
        super().__init__(amount, Processes.VC_VOCAB_QUIZ_PRACTICE)

        self.use_furigana = use_furigana

        self.usedFurigana = []
        self.usedKanji = []

    async def create_question(self, interaction: discord.Interaction, vc = None):
        if self.currentAnswersForQuestion is None:
            self.currentAnswersForQuestion = []

        self.currentAnswersForQuestion.clear()

        for i in range(5): # Five Possible Answers
            is_answer = i == 0

            if self.use_furigana:
                furigana_answer = self.get_furigana_question(is_answer)

                self.currentAnswersForQuestion.append(furigana_answer)

                self.usedFurigana.append(furigana_answer[0])
            else:
                kanji_answer = self.get_kanji_question(is_answer)

                self.currentAnswersForQuestion.append(kanji_answer)

                self.usedKanji.append(kanji_answer[0])

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
        usable_kanji = [kana for kana in vc_vocab_kanji.keys() if kana not in used_kanji_set]

        if usable_kanji == [] or len(usable_kanji) <= 0:
            used_kanji_set.clear()
            usable_kanji = [kanji for kanji in vc_vocab_kanji.keys() if kanji not in used_kanji_set]

        kanji_key = random.choice(usable_kanji)

        return (vc_vocab_kanji[kanji_key], kanji_key, is_answer)