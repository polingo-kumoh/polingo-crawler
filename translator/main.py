from common.article_repository import ArticleRepository
from translator_factory import TranslatorFactory
from dotenv import load_dotenv
from common.slack_bot import SlackAPI
import os


if os.getenv('CI') != 'true':
    load_dotenv()

import os

slack_token = os.environ["SLACK_TOKEN"]

deepl_token_string = os.environ["DEEPL_TOKEN"]
deepl_tokens = deepl_token_string.split(',') if deepl_token_string else []


host = os.environ["MYSQL_HOST"]
username = os.environ["MYSQL_USERNAME"]
password = os.environ["MYSQL_PASSWORD"]
database = os.environ["MYSQL_DATABASE"]


def main():
    article_repository = ArticleRepository(host, username, password, database)
    translator = TranslatorFactory(deepl_tokens)
    slack_bot = SlackAPI(slack_token)


    articles = article_repository.findAll()
    channel_id = slack_bot.get_channel_id("polingo-logs")
    slack_bot.post_message(channel_id, f"Translator : News Translate started")

    for article in articles:
        for article_setentence in article["sentences"]:
            origin_text = article_setentence["origin_text"]

            article_setentence["translated_text"] = translator.translate(origin_text)
        article_repository.update(article["sentences"])

    slack_bot.post_message(channel_id, f"Translator : News Translate completed")


if __name__ == '__main__':
    main()