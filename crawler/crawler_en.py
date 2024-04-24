import newspaper
import nltk
import pytz


cnn_url = 'https://edition.cnn.com'


class CnnCrawler:
    def __init__(self):
        self.paper = newspaper.build(cnn_url, memoize_articles=False, language= "en")

    def crawl(self, size):
        result = []

        # 맨앞 5개는 이상한 값이 들어가 있어서 5번 이상의 뉴스를 가져옴
        for i, article in enumerate(self.paper.articles[:size * 2], 1):
            parsed_article = {}
            article.download()
            article.parse()

            parsed_article["url"] = article.url
            parsed_article["publish_date"] = article.publish_date
            parsed_article["title"] = article.title
            parsed_article["sentences"] = nltk.sent_tokenize(article.text)
            parsed_article["image"] = article.top_image
            result.append(parsed_article)

        return self.filter_and_sort_articles(result, size)

    def filter_and_sort_articles(self, articles, size):
        # publish_date가 None이 아닌 articles만 필터링
        filtered_articles = [article for article in articles if article['publish_date'] is not None]

        # 모든 datetime을 UTC로 변환
        for article in filtered_articles:
            if article['publish_date'].tzinfo is None or article['publish_date'].tzinfo.utcoffset(
                    article['publish_date']) is None:
                article['publish_date'] = pytz.utc.localize(article['publish_date'])
            else:
                article['publish_date'] = article['publish_date'].astimezone(pytz.utc)

        # publish_date에 따라 내림차순으로 정렬
        sorted_articles = sorted(filtered_articles, key=lambda x: x['publish_date'], reverse=True)

        # 상위 N개 article 반환
        return sorted_articles[:size]