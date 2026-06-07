import sqlite3 # Or psycopg2 if using Postgres

class DBManager:
    def __init__(self, db_path='database/grc_engine.db'):
        self.db_path = db_path

    def execute(self, query, params=()):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
