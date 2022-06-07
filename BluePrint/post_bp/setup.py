import sqlite3 as sql
from main import App
from .config import DB
from .post_bp import post_bp

def create_db():
    try:
        with sql.connect(DB.sqlite) as conn:
            cur = conn.cursor()
            SQL_INFO = """CREATE TABLE IF NOT EXISTS post(
                id  TEXT PRIMARY KEY NOT NULL,
                title  TEXT NOT NULL,
                tags  TEXT NOT NULL,
                date  TEXT NOT NULL,
                show  BOOLEAN DEFAULT 1
            )
            """

            cur.execute(SQL_INFO)
            SQL_CONTENT = """CREATE TABLE IF NOT EXISTS content(
                id TEXT PRIMARY KEY NOT NULL,
                content TEXT NOT NULL
            )
            """
            cur.execute(SQL_CONTENT)

            SQL_CONTENT = """CREATE TABLE IF NOT EXISTS ip(
                id TEXT PRIMARY KEY NOT NULL,
                ip TEXT NOT NULL  DEFAULT '',
                view INT DEFAULT 0
            )
            """
            cur.execute(SQL_CONTENT)

            conn.commit()
    except Exception as e:
        raise(e)

create_db()

app = App.get_app()

app.register_blueprint(post_bp)