
import requests
import json
class GrammarAnalyzer:
    def __init__(self, url):
        self.url = url

    def analyze(self, text):
        data = {'query': text}
        headers = {'Content-Type': 'application/json; charset=utf-8'}


        # POST 요청 보내기
        response = requests.post(self.url, data=json.dumps(data), headers=headers)

        # 응답 내용 확인
        if response.status_code == 200:
            return json.loads(response.text)['results']
        else:
            print("요청 실패:", response.status_code)