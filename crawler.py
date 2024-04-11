import newspaper
import nltk
# 최초 실행시 punkt 1번만 다운 필요
#nltk.download('punkt')

cnn_url = 'https://edition.cnn.com'
cnn_paper = newspaper.build(cnn_url, memoize_articles=False)

#bbc_url = 'https://www.bbc.com/news'
#bbc_paper = newspaper.build(bbc_url, memoize_articles=False)

# 최신 10개 기사에 대해 반복
for i, article in enumerate(cnn_paper.articles[:10], 1):
    # 기사 다운로드 및 파싱
    article.download()
    article.parse()
    
    print("URL:", article.url)

    # 발행날짜 출력
    print("발행날짜:", article.publish_date)

    # 기사 제목 출력
    print("제목:", article.title)
    
    # 기사 본문 출력
    #print("본문:", article.text)

    # 문장별로 텍스트 저장
    sentences = nltk.sent_tokenize(article.text)
    print("문장별 텍스트:")
    for idx, sentence in enumerate(sentences, 1):
        print(f"{idx}. {sentence}")
    
    # 기사 이미지 URL 출력
    if article.top_image:
        print("이미지:", article.top_image)
    
    # 기사 키워드 출력
    article.nlp()
    print("키워드:", article.keywords)
    
    # 기사 요약 출력
    print("요약:", article.summary)
    print(f"------------{i}번째 기사------------\n")
