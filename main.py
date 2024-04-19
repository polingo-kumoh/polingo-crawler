import nltk
from crawler import Crawler




def main():
    # 최초 실행시 punkt 1번만 다운 필요
    nltk.download('punkt')

    cnn_url = 'https://edition.cnn.com'
    nhk_url = 'https://www3.nhk.or.jp/news/'

    cnn_crawler = Crawler(cnn_url, "en")
    nhk_crawler = Crawler(nhk_url, "ja")

    cnn_articles = cnn_crawler.crawl(5, 10)
    nhk_articles = nhk_crawler.crawl(0, 5)
    print()

if __name__ == '__main__':
    main()
