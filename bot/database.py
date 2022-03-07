import sqlite3 as sq

with sq.connect('urls_video.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY,
        url TEXT(200) NOT NULL
    )""")