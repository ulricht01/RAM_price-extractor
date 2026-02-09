import sqlite3

class Database:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(f"{db_name}.db")
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ramky (
                name TEXT, 
                price INTEGER, 
                dt_insert TEXT
            );
        """)
        self.conn.commit()

    def check_for_today_data(self, date):
        check = self.cursor.execute("SELECT * FROM ramky WHERE dt_insert = ? LIMIT 1", [date])
        return check.fetchone() is not None
    
    def insert_data(self, name, price, date):
        self.cursor.execute("""INSERT INTO ramky (name, price, dt_insert) VALUES(?, ?, ?);""", [name, price, date])

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()

    def export_data(self):
        data = self.cursor.execute("SELECT * FROM ramky")
        return self.cursor.fetchall()
        



    
        

        