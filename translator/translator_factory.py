from translator import ArticleTranslator


class TranslatorFactory :

    def __init__(self, token_list : list):
        self.translator_list = [ArticleTranslator(token) for token in token_list]
        self.current_index = 0

    def translate(self, text):
        # 라운드 로빈 방식으로 번역기 선택
        translator = self.translator_list[self.current_index]
        # 요청된 텍스트 번역
        result = translator.translate(text)
        # 다음 번역기로 인덱스 업데이트
        self.current_index = (self.current_index + 1) % len(self.translator_list)
        return result