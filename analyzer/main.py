from dotenv import load_dotenv
from common.slack_bot import SlackAPI
from common.article_repository import ArticleRepository
import os


if os.getenv('CI') != 'true':
    load_dotenv()

slack_token = os.environ["SLACK_TOKEN"]


host = os.environ["MYSQL_HOST"]
username = os.environ["MYSQL_USERNAME"]
password = os.environ["MYSQL_PASSWORD"]
database = os.environ["MYSQL_DATABASE"]


def main():
    article_repository = ArticleRepository(host, username, password, database)
    slack_bot = SlackAPI(slack_token)
    articles = article_repository.findAll(language="ENGLISH")

    print()



if __name__ == '__main__':
    main()