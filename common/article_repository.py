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
            cursor = conn.cursor()
            # SQL 쿼리 작성
            sql = """
            SELECT news.id, news.title, news.publish_date, news.image_url, news.news_url,
                   news_sentence.grammars, news_sentence.origin_text, news_sentence.translated_text
            FROM news
            JOIN news_sentence ON news.id = news_sentence.news_id
            ORDER BY news.publish_date DESC
            LIMIT %s OFFSET %s
            """
            # SQL 쿼리 실행
            cursor.execute(sql, (limit, offset))
            # 결과를 가져와 반환
            result = cursor.fetchall()
            return result
        except pymysql.Error as e:
            print(f"Error: {e}")
            conn.rollback()
            raise
        finally:
            # 커서 및 커넥션 종료
            cursor.close()
            conn.close()

    def updateAll(self, articles : list):
        print("update")