import psycopg2 # Or your preferred driver like sqlite3

class DBManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
    
    def execute(self, query, params):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()
