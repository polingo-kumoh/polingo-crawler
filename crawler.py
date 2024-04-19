import newspaper
import nltk

cnn_url = 'https://edition.cnn.com'


class Crawler:
    def __init__(self, url, language):
        self.paper = newspaper.build(url, memoize_articles=False, language= language)
        self.language = language
    def crawl(self, start=0, end=10):
        result = []

        # 맨앞 5개는 이상한 값이 들어가 있어서 5번 이상의 뉴스를 가져옴
        for i, article in enumerate(self.paper.articles[start:end], 1):
            parsed_article = {}
            article.download()
            article.parse()

            parsed_article["url"] = article.url
            parsed_article["publish_date"] = article.publish_date
            parsed_article["title"] = article.title
            parsed_article["sentences"] = nltk.sent_tokenize(article.text)
            parsed_article["image"] = article.top_image
            parsed_article["language"] = self.language
            result.append(parsed_article)
        return result