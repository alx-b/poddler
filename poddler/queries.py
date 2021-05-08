from typing import List, Tuple, Callable, Any
import sqlite3
# For the sake of shortening Type Annotation
from sqlite3 import Connection, Cursor
from models import PodcastIn


def open_db(func: Callable) -> Any:
    def wrapper(*args, **kwargs):
        with sqlite3.connect("podcasts.db") as db:
            return func(db, *args, **kwargs)
    return wrapper


@open_db
def create_podcasts_table(db: Connection) -> None:
    db.execute(
        """CREATE TABLE IF NOT EXISTS podcasts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT,
          url TEXT UNIQUE)"""
    )
    db.commit()


@open_db
def insert_into_podcast_table(db: Connection, podcast: PodcastIn) -> None:
    """Insert podcast model into database's podcasts table

    Parameters:
        db: sqlite3.Connection
        podcast: models.PodcastIn
    """
    db.cursor().execute(
        "INSERT INTO podcasts(title, url) VALUES (?, ?)",
        (podcast.title, podcast.url),
    )
    db.commit()


@open_db
def get_all_podcasts(db: Connection) -> List[Tuple]:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM podcasts")
    return cursor.fetchall()


@open_db
def get_a_podcast_by_title(db: Connection, title: str) -> Tuple[int, str, str]:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM podcasts WHERE title=?", (title,))
    return cursor.fetchone()


@open_db
def delete_a_podcast_by_title(db: Connection, title: str) -> None:
    db.cursor().execute("DELETE FROM podcasts WHERE title=?", (title,))
    db.commit()


if __name__ == "__main__":
    create_podcasts_table()
