import newspaper
import re
from janome.tokenizer import Tokenizer





# https://www3.nhk.or.jp/news/ <- 인기 뉴스에서 받아옴
nhk_url = 'https://www3.nhk.or.jp/news/catnew.html'

class NhkCrawler:

    def __init__(self):
        self.paper = newspaper.build(nhk_url, memoize_articles=False, language='ja')
        self.tokenizer = Tokenizer()

    def crawl(self, size):
        filtered_articles = [article for article in self.paper.articles if article.url.startswith("https://www3.nhk.or.jp/news/html")]
        result = []

        # 필터링된 기사에 대해 반복
        for i, article in enumerate(filtered_articles[:size], 1):
            parsed_article = {}
            article.download()
            article.parse()

            parsed_article["url"] = article.url
            parsed_article["publish_date"] = article.publish_date
            parsed_article["title"] = article.title

            cleaned_text = re.sub(r'\s{2,}', ' ', article.text)
            split_sentences = re.split(r'(?<=。)', cleaned_text)

            restructured_sentences = []

            for sentence in split_sentences:
                if sentence.strip():
                    tokens = list(self.tokenizer.tokenize(sentence.strip()))

                    new_sentence = ""

                    for token in tokens:
                        if token.part_of_speech.startswith("記号"):  # 구두점인 경우
                            new_sentence += token.surface
                        else:  # 단어인 경우
                            if new_sentence:
                                new_sentence += " "
                            new_sentence += token.surface

                    restructured_sentences.append(new_sentence)

            parsed_article["sentences"] = restructured_sentences
            parsed_article["image"] = article.top_image
            result.append(parsed_article)
    
        return result
