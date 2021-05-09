import pytest
import sqlite3

from poddler import queries
from poddler.models import PodcastIn


@pytest.fixture(scope="session")
def db():
    with sqlite3.connect(":memory:") as db:
        db_setup(db)
        return db


def db_setup(db):
    db.execute(
        """CREATE TABLE IF NOT EXISTS podcasts (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT,
         url TEXT UNIQUE)"""
    )
    db.cursor().executemany(
        "INSERT INTO podcasts(title, url) VALUES (?, ?)",
        [
            ("pod_title", "pod_url"),
            ("pod_title_2", "pod_url_2"),
        ],
    )
    db.commit()


@pytest.mark.usefixtures("db")
def test_get_all_podcasts(db):
    assert queries.get_all_podcasts.__wrapped__(db) == [
        (1, "pod_title", "pod_url"),
        (2, "pod_title_2", "pod_url_2"),
    ]


@pytest.mark.usefixtures("db")
def test_get_a_podcast_by_title(db):
    assert queries.get_a_podcast_by_title.__wrapped__(db, "pod_title") == (
        1,
        "pod_title",
        "pod_url",
    )


@pytest.mark.usefixtures("db")
def test_insert_into_podcast_table(db):
    pod = PodcastIn("pod_title_3", "pod_url_3")
    queries.insert_into_podcast_table.__wrapped__(db, pod)
    assert queries.get_all_podcasts.__wrapped__(db) == [
        (1, "pod_title", "pod_url"),
        (2, "pod_title_2", "pod_url_2"),
        (3, "pod_title_3", "pod_url_3"),
    ]
    # assert queries.get_a_podcast_by_title.__wrapped__(db, "pod_title_3") == (
    #    3,
    #    "pod_title_3",
    #    "pod_url_3",
    # )


@pytest.mark.usefixtures("db")
def test_delete_a_podcast_by_title(db):
    queries.delete_a_podcast_by_title.__wrapped__(db, "pod_title")
    assert queries.get_all_podcasts.__wrapped__(db) == [
        (2, "pod_title_2", "pod_url_2"),
        (3, "pod_title_3", "pod_url_3"),
    ]
