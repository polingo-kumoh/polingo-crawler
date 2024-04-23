import newspaper
import re






# https://www3.nhk.or.jp/news/ <- 인기 뉴스에서 받아옴
nhk_url = 'https://www3.nhk.or.jp/news/catnew.html'

class NhkCrawler:

    def __init__(self):
        self.paper = newspaper.build(nhk_url, memoize_articles=False, language='ja')


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

            # 마지막 sentence는 공백값이라서 제거
            parsed_article["sentences"] = split_sentences[:-1]
            parsed_article["image"] = article.top_image
            result.append(parsed_article)
    
        return result
