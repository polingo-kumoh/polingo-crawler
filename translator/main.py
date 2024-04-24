from common.article_repository import ArticleRepository
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

    articles = article_repository.findAll()

    for article in articles:
        for article_setentence in article.sentences:
            print(f"Do Translate : {article_setentence}")

    article_repository.updateAll(articles)

if __name__ == '__main__':
    main()