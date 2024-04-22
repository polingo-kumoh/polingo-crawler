import newspaper
import nltk
import re
from newspaper import Article

# 최초 실행시 punkt 1번만 다운 필요
#nltk.download('punkt')

# https://www3.nhk.or.jp/news/ <- 인기 뉴스에서 받아옴
nhk_url = 'https://www3.nhk.or.jp/news/catnew.html'
nhk_paper = newspaper.build(nhk_url, memoize_articles=False, language='ja')

filtered_articles = [article for article in nhk_paper.articles if article.url.startswith("https://www3.nhk.or.jp/news/html")]

# 필터링된 기사에 대해 반복
for i, article in enumerate(filtered_articles[:7], 1):
    # 기사 다운로드 및 파싱
    article.download()
    article.parse()
    
    print("URL:", article.url)

    # 발행날짜 출력
    date = Article(article.url, memoize_articles=False)
    date.download()
    date.parse()
    print("발행날짜:", date.publish_date)

    # 기사 제목 출력
    print("제목:", article.title)
    
    # 기사 본문 출력
    print("------------본문------------")
    cleaned_text = re.sub(r'\s{2,}', ' ', article.text)
    split_sentences = re.split(r'(?<=。)', cleaned_text)

    # 각 문장을 출력
    for idx, sentence in enumerate(split_sentences, 1):
        if sentence.strip():
            print(f"{idx}. {sentence.strip()}")
    
    # 기사 이미지 URL 출력
    if article.top_image:
        print("이미지:", article.top_image)
    
    '''
    # 기사 키워드 출력
    article.nlp()
    print("키워드:", article.keywords)
    
    # 기사 요약 출력
    print("요약:", article.summary)
    '''
    print(f"------------{i}번째 기사------------\n")
