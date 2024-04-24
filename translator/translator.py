import deepl


class ArticleTraslator:

    def __init__(self, auth_key):
        self.translator = deepl.Translator(auth_key)

    def translate(self, text):
        translated = self.translator.translate_text(text, target_lang="KO")

        return translated.text