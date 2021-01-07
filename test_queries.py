import pytest
import sqlite3
import queries


@pytest.fixture(scope="session")
def database():
    with sqlite3.connect(":memory:") as db:
        return (db, db.cursor())


@pytest.fixture(scope="session")
def db_setup(database):
    db, cursor = database
    db.execute(
        """CREATE TABLE IF NOT EXISTS podcasts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT,
          url TEXT UNIQUE)"""
    )
    cursor.executemany(
        "INSERT INTO podcasts(title, url) VALUES (?, ?)",
        [
            ("pod_title", "pod_url"),
            ("pod_title_2", "pod_url_2"),
        ],
    )
    db.commit()


@pytest.mark.usefixtures("db_setup")
def test_get_all_podcasts(database):
    assert queries.get_all_podcasts(database) == [
        (1, "pod_title", "pod_url"),
        (2, "pod_title_2", "pod_url_2"),
    ]


def test_get_a_podcast_by_title(database):
    assert queries.get_a_podcast_by_title(database, "pod_title") == (
        1,
        "pod_title",
        "pod_url",
    )
