from common.article_repository import ArticleRepository
from translator import ArticleTraslator
from dotenv import load_dotenv
import os


if os.getenv('CI') != 'true':
    load_dotenv()

import os

slack_token = os.environ["SLACK_TOKEN"]

host = os.environ["MYSQL_HOST"]
username = os.environ["MYSQL_USERNAME"]
password = os.environ["MYSQL_PASSWORD"]
database = os.environ["MYSQL_DATABASE"]


def main():
    article_repository = ArticleRepository(host, username, password, database)
    translator = ArticleTraslator()

    articles = article_repository.findAll()

    for article in articles:
        for article_setentence in article["sentences"]:
            origin_text = article_setentence["origin_text"]
            language_code = get_lang_code(article["language"])

            article_setentence["translated_text"] = translator.translate(origin_text,language_code)
        article_repository.update(article["sentences"])

def get_lang_code(code):
    if code == "ENGLISH" :
        return "en"
    else:
        return "ja"

if __name__ == '__main__':
    main()