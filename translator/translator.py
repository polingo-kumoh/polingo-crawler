from googletrans import Translator



class ArticleTraslator:

    def __init__(self):
        self.translator = Translator()

    def translate(self, text, lang="en"):
        translated = self.translator.translate(text, dest="ko", src=lang)

        return translated.text