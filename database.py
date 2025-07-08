import sqlite3


class Database:
    def __init__(self, db_name='movies.sqlite'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                type TEXT,
                status TEXT,
	            score TEXT,
	            runtime_ep_count TEXT,
	            release_year TEXT,
                date_unified TEXT
            )
        """)
        self.conn.commit()

    # CRUD
    def fetch_all_movies(self):
        self.cursor.execute("SELECT * FROM movies")
        return self.cursor.fetchall()

    def fetch_completed_movies(self):
        self.cursor.execute("SELECT * FROM movies WHERE status = 'Completed'")
        return self.cursor.fetchall()

    def fetch_watching_movies(self):
        self.cursor.execute("SELECT * FROM movies WHERE status = 'Watching'")
        return self.cursor.fetchall()

    def fetch_plan_to_watch_movies(self):
        self.cursor.execute("SELECT * FROM movies WHERE status = 'Plan to Watch'")
        return self.cursor.fetchall()

    def insert_movie(self, movie):
        self.cursor.execute('''INSERT INTO movies (title, type, status, score, 
        runtime_ep_count, release_year, date_unified) VALUES (?, ?, ?, ?, ?, ?, ?)''', movie.as_tuple())
        self.conn.commit()

    def update_movie(self, movie):
        self.cursor.execute('''UPDATE movies SET title=?, type=?, status=?, score=?, runtime_ep_count=?,
        release_year=?, date_unified=? WHERE id=?''',
                            (movie.as_tuple_update()))
        self.conn.commit()

    def delete_movie(self, id):
        self.cursor.execute("DELETE FROM movies WHERE id=?", (id,))
        self.conn.commit()

    def db_matching(self, title):
        self.cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f"{title}%",))
        return self.cursor.fetchall()

    def clear(self):
        self.cursor.execute("DELETE FROM movies")
        self.conn.commit()