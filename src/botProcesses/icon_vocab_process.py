import random
import discord
from botProcesses.bot_process_constants import icons_furigana, icons_furigana_flags, icons_furigana_time, icons_kanji, icons_kanji_flags, icons_kanji_time
from botProcesses.bot_process_definitions import Processes, BaseQuizProcess
from views.views import QuizPracticeView


class IconVocabProcess(BaseQuizProcess):
    def __init__(self, amount: str, use_furigana: bool, add_flags: bool = False, add_time: bool = False):
        super().__init__(amount, Processes.ICON_VOCAB_QUIZ_PRACTICE)

        self.usedIcons = []

        self.icons_furigana = icons_furigana
        self.icons_kanji = icons_kanji

        self.useFurigana = use_furigana

        self.add_flags = add_flags
        self.add_time = add_time

        self.add_possible_icons()

    def add_possible_icons(self):
        if self.useFurigana:
            if self.add_flags:
                self.icons_furigana = self.icons_furigana | icons_furigana_flags

            if self.add_time:
                self.icons_furigana = self.icons_furigana | icons_furigana_time
        else:
            if self.add_flags:
                self.icons_kanji = self.icons_kanji | icons_kanji_flags

            if self.add_time:
                self.icons_kanji = self.icons_kanji | icons_kanji_time

    async def create_question(self, interaction: discord.Interaction):
        if self.currentAnswersForQuestion is None:
            self.currentAnswersForQuestion = []

        self.currentAnswersForQuestion.clear()

        guess_by_icon = random.random() < 0.5  # Or Vice Versa

        for i in range(5): # Five Possible Answers
            is_answer = i == 0

            answer = None

            if self.useFurigana:
                answer = self.get_furigana_question(is_answer, guess_by_icon)

                self.currentAnswersForQuestion.append(answer)
            else:
                answer = self.get_kanji_question(is_answer, guess_by_icon)

                self.currentAnswersForQuestion.append(answer)

            if answer is not None:
                if guess_by_icon == True:
                    self.usedIcons.append(answer[0])
                else:
                    self.usedIcons.append(answer[1])

        self.currentAnswersForQuestion = random.sample(self.currentAnswersForQuestion, len(self.currentAnswersForQuestion))  # Shuffle

        view = QuizPracticeView(self, interaction)

        await view.display_question(interaction, self.processType)

    def get_furigana_question(self, is_answer: bool, guess_by_icon: bool):
        used_icons_set = set(self.usedIcons)
        usable_icons = [icon for icon in self.icons_furigana.keys() if icon not in used_icons_set]

        if usable_icons == [] or len(usable_icons) <= 0:
            used_icons_set.clear()
            usable_icons = [icon for icon in self.icons_furigana.keys() if icon not in used_icons_set]

        icon_key = random.choice(usable_icons)

        if guess_by_icon:
            return (icon_key, self.icons_furigana[icon_key], is_answer)
        else:
            return (self.icons_furigana[icon_key], icon_key, is_answer)

    def get_kanji_question(self, is_answer: bool, guess_by_icon: bool):
        used_icons_set = set(self.usedIcons)
        usable_icons = [icon for icon in self.icons_kanji.keys() if icon not in used_icons_set]

        if usable_icons == [] or len(usable_icons) <= 0:
            used_icons_set.clear()
            usable_icons = [icon for icon in self.icons_kanji.keys() if icon not in used_icons_set]

        icon_key = random.choice(usable_icons)

        if guess_by_icon:
            return (icon_key, self.icons_kanji[icon_key], is_answer)
        else:
            return (self.icons_kanji[icon_key], icon_key, is_answer)