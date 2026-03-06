import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            # Таблица комбинаций
            conn.execute('''
                CREATE TABLE IF NOT EXISTS win_combinations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    combination TEXT NOT NULL,
                    payout INTEGER NOT NULL
                )
            ''')

            # Таблица победителей
            conn.execute('''
                CREATE TABLE IF NOT EXISTS winners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    total_win INTEGER NOT NULL DEFAULT 0
                )
            ''')

            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

def get_combinations(self):
    return self.__select_data("SELECT combination, payout FROM win_combinations")

def get_winner(self, user_id):
    return self.__select_data(
        "SELECT total_win FROM winners WHERE user_id = ?",
        (user_id,)
    )
def update_winner(self, user_id, username, payout):
    existing = self.get_winner(user_id)

    if existing:
        new_total = existing[0][0] + payout
        self.__executemany(
            "UPDATE winners SET total_win = ?, username = ? WHERE user_id = ?",
            [(new_total, username, user_id)]
        )
    else:
        self.__executemany(
            "INSERT INTO winners (user_id, username, total_win) VALUES (?, ?, ?)",
            [(user_id, username, payout)]
        )


            
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    