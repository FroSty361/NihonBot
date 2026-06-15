from enum import Enum
import random
from dataclasses import field

# Lists

hiragana = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo',
    'ん': 'n',

    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',

    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo'
}

katakana = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',

    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa','ヲ': 'wo',
    'ン': 'n',

    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',

    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',

    'ヴ': 'vu',
    'ファ': 'fa', 'フィ': 'fi', 'フェ': 'fe', 'フォ': 'fo',
    'ティ': 'ti', 'ディ': 'di', 'デュ': 'dyu',
    'ウィ': 'wi', 'ウェ': 'we', 'ウォ': 'wo',
    'ヴァ': 'va', 'ヴィ': 'vi', 'ヴェ': 've', 'ヴォ': 'vo',
    'ー': 'lengthen vowel'
}

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

    def create_question(self):
        if self.practicingHiragana == False and self.practicingKatakana == False:
            print("Says Practicing Both Hiragana And Katakana Is False. Setting Both To True")

            self.practicingHiragana = True
            self.practicingKatakana = True

        if self.currentAnswersForQuestion == None:
            self.currentAnswersForQuestion = []

        self.currentAnswersForQuestion.clear()

        for i in range(5): # Five Possible Answers
            if i == 0:
                self.currentAnswersForQuestion.append(self.get_hiragana_question(True))
            else:
                self.currentAnswersForQuestion.append(self.get_hiragana_question(False))

        self.currentAnswersForQuestion = random.sample(self.currentAnswersForQuestion, len(self.currentAnswersForQuestion)) # Shuffle


    def get_hiragana_question(self, is_answer: bool):
        used_hiragana_set = set(self.usedHiragana)
        usable_hiragana = [kana for kana in hiragana.keys() if kana not in used_hiragana_set]

        if usable_hiragana == [] or len(usable_hiragana) <= 0:
            used_hiragana_set.clear()
            usable_hiragana = [kana for kana in hiragana.keys() if kana not in used_hiragana_set]

        hiragana_key = random.choice(usable_hiragana)

        return (hiragana_key, hiragana[hiragana_key], is_answer)

    def answer_question(self, is_answer: bool):
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

        if self.isIndefiniteAmount == False and self.amountCompleted >= self.amount:
            returnMessage += self.stop_process()

        return returnMessage

    def stop_process(self):
        stop_process_message = ""

        if self.isIndefiniteAmount:
            try:
                percentCorrect = round((self.amountCorrect / self.amountCompleted) * 100, 3)

                stop_process_message = f"Completed! You Got {self.amountCorrect} Out Of {self.amountCompleted}! That Is {percentCorrect} Percent Correct"
            except ZeroDivisionError:
                stop_process_message = f"Completed! You Got {self.amountCorrect} Out Of {self.amountCompleted}!"
        else:
            try:
                percentCorrect = round((self.amountCorrect / self.amount) * 100, 3)

                stop_process_message = f"Completed! You Got {self.amountCorrect} Out Of {self.amount}! That Is {percentCorrect} Percent Correct!"
            except ZeroDivisionError:
                stop_process_message = f"Completed! You Got {self.amountCorrect} Out Of {self.amount}!"

        return stop_process_message

    # Helpers

    def string_is_int(self, s : str):
        if s[0] in ('-', '+'):
            return s[1:].isdigit()

        return s.isdigit()