import nltk
from crawler import Crawler
from article_insertor import ArticleInsertor
import pytz


def main():
    # 최초 실행시 punkt 1번만 다운 필요
    nltk.download('punkt')

    cnn_url = 'https://edition.cnn.com'
    nhk_url = 'https://www3.nhk.or.jp/news/'

    cnn_crawler = Crawler(cnn_url, "en")
    nhk_crawler = Crawler(nhk_url, "ja")
    article_insertor = ArticleInsertor("localhost", "root", "1111", "polingo")


    cnn_articles = filter_and_sort_articles(cnn_crawler.crawl(0, 20))
    nhk_articles = filter_and_sort_articles(nhk_crawler.crawl(0, 20))

    for article in cnn_articles:
        article["language"] = "ENGLISH"
        article_insertor.insert(article)
    for article in nhk_articles:
        article["language"] = "JAPANESE"
        article_insertor.insert(article)

def filter_and_sort_articles(articles):
    # publish_date가 None이 아닌 articles만 필터링
    filtered_articles = [article for article in articles if article['publish_date'] is not None]

    # 모든 datetime을 UTC로 변환
    for article in filtered_articles:
        if article['publish_date'].tzinfo is None or article['publish_date'].tzinfo.utcoffset(article['publish_date']) is None:
            article['publish_date'] = pytz.utc.localize(article['publish_date'])
        else:
            article['publish_date'] = article['publish_date'].astimezone(pytz.utc)

    # publish_date에 따라 내림차순으로 정렬
    sorted_articles = sorted(filtered_articles, key=lambda x: x['publish_date'], reverse=True)

    # 상위 5개 article 반환
    return sorted_articles[:5]


if __name__ == '__main__':
    main()
