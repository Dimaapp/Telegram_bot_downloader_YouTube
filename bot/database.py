import sqlite3 as sq

with sq.connect('urls_video.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        video BLOB NOT NULL
    )""")

