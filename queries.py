from typing import List, Tuple
import sqlite3


def open_db() -> Tuple:
    with sqlite3.connect("podcasts.db") as db:
        return (db, db.cursor())


def create_podcasts_table(database) -> None:
    db, _ = database
    db.execute(
        """CREATE TABLE IF NOT EXISTS podcasts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT,
          url TEXT UNIQUE)"""
    )
    db.commit()


def insert_into_podcast_table(database, podcast) -> None:
    db, cursor = database
    cursor.execute(
        "INSERT INTO podcasts(title, url) VALUES (?, ?)",
        (podcast.title, podcast.url),
    )
    db.commit()


def get_all_podcasts(database) -> List[Tuple]:
    _, cursor = database
    cursor.execute("SELECT * FROM podcasts")
    return cursor.fetchall()


def get_a_podcast_by_title(database, title) -> Tuple[int, str, str]:
    _, cursor = database
    cursor.execute("SELECT * FROM podcasts WHERE title=?", (title,))
    return cursor.fetchone()


def update_a_podcast_title_by_title(database, title, new_title) -> None:
    db, cursor = database
    cursor.execute(
        "UPDATE podcasts SET title=? WHERE title=?",
        (new_title, title),
    )
    db.commit()


def update_a_podcast_url_by_title(database, title, new_url) -> None:
    db, cursor = database
    cursor.execute(
        "UPDATE podcasts SET url=? WHERE title=?",
        (new_url, title),
    )
    db.commit()


def delete_a_podcast_by_title(database, title) -> None:
    db, cursor = database
    cursor.execute("DELETE FROM podcasts WHERE title=?", (title,))
    db.commit()


#########################################
# def get_all_podcast():
#    return map(models.create_podcast_class, get_podcasts())
#
#
# def get_a_podcast(title):
#    return models.create_podcast_class(get_one_podcast(title))
#########################################


if __name__ == "__main__":
    create_podcasts_table(open_db())
