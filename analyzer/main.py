from dotenv import load_dotenv
from common.slack_bot import SlackAPI
from common.article_repository import ArticleRepository
from analyzer.grammer_analyzer import GrammarAnalyzer
import os


if os.getenv('CI') != 'true':
    load_dotenv()

slack_token = os.environ["SLACK_TOKEN"]


host = os.environ["MYSQL_HOST"]
username = os.environ["MYSQL_USERNAME"]
password = os.environ["MYSQL_PASSWORD"]
database = os.environ["MYSQL_DATABASE"]


analyzer_url = os.environ["ANALYZER_URL"]

def main():
    article_repository = ArticleRepository(host, username, password, database)
    slack_bot = SlackAPI(slack_token)
    analyzer = GrammarAnalyzer(analyzer_url)

    articles = article_repository.findAll(language="ENGLISH")
    channel_id = slack_bot.get_channel_id("polingo-logs")


    slack_bot.post_message(channel_id, f"Analyzer : News Analyze started")
    for article in articles:
        for article_setentence in article["sentences"]:
            origin_text = article_setentence["origin_text"]

            article_setentence["grammars"] = analyzer.analyze(origin_text)
        article_repository.update(article["sentences"])
    slack_bot.post_message(channel_id, f"Analyzer : News Analyze completed")




if __name__ == '__main__':
    main()