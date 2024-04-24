import pymysql
from dbutils.pooled_db import PooledDB
import datetime


class ArticleInsertor:

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

