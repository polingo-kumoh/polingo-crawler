import pymysql
from dbutils.pooled_db import PooledDB
import datetime


class ArticleRepository:

    def __init__(self, host, username, password, database):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            host=host,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )

    def insert(self, article):
        # 커넥션 풀에서 커넥션 가져오기
        conn = self.pool.connection()
        now = datetime.datetime.now()
        try:
            # 커서 생성
            cursor = conn.cursor()

            sql1 = """
            INSERT INTO news (created_at, publish_date, updated_at, image_url, news_url, title, language)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql1, (now, article["publish_date"], now, article["image"], article["url"], article["title"] , article["language"]))

            inserted_id = cursor.lastrowid

            sql2 = """
            INSERT INTO news_sentence (news_id,origin_text)
            VALUES (%s, %s)
            """

            for sentence in article["sentences"]:
                cursor.execute(sql2, (inserted_id, sentence))

            conn.commit()
            print("Data inserted successfully.")
        except pymysql.Error as e:
            print(f"Error: {e}")
            conn.rollback()
            raise
        finally:
            # 커서 및 커넥션 종료
            cursor.close()
            conn.close()

    def findAll(self, offset=0, limit=10):
        # 데이터베이스 연결 설정
        conn = self.pool.connection()
        try:
            # 커서 생성
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # 뉴스 기사만 먼저 가져옴
            sql_news = """
            SELECT id, title, publish_date, image_url, news_url, language
            FROM news
            ORDER BY publish_date DESC, id
            LIMIT %s OFFSET %s
            """
            cursor.execute(sql_news, (limit, offset))
            news_list = cursor.fetchall()

            # 뉴스 데이터를 dictionary로 구성
            news_dict = {news['id']: news for news in news_list}
            for news in news_dict.values():
                news['sentences'] = []

            # 각 뉴스에 해당하는 모든 문장을 가져옴
            if news_dict:
                sql_sentences = """
                SELECT news_id, id as sentence_id, grammars, origin_text, translated_text
                FROM news_sentence
                WHERE news_id IN (%s)
                """
                # IN 절에 사용할 뉴스 ID 목록 생성
                news_ids = list(news_dict.keys())
                format_strings = ','.join(['%s'] * len(news_ids))
                cursor.execute(sql_sentences % format_strings, tuple(news_ids))
                sentences = cursor.fetchall()

                # 문장을 해당 뉴스에 추가
                for sentence in sentences:
                    if sentence['news_id'] in news_dict:
                        news_dict[sentence['news_id']]['sentences'].append(sentence)

            return list(news_dict.values())

        except pymysql.Error as e:
            print(f"Error: {e}")
            conn.rollback()
            raise
        finally:
            # 커서 및 커넥션 종료
            cursor.close()
            conn.close()

    def update(self, sentences : list):
        # 데이터베이스 연결 설정
        conn = self.pool.connection()
        try:

            for sentence in sentences:
                # 커서 생성
                cursor = conn.cursor()
                # SQL 쿼리 작성
                sql_update = """
                UPDATE news_sentence
                SET translated_text = %s
                WHERE id = %s
                """
                # SQL 쿼리 실행
                cursor.execute(sql_update, (sentence["translated_text"], sentence["sentence_id"]))
            # 변경사항 저장
            conn.commit()
            print("article sentences save completed")
        finally:
            conn.close()