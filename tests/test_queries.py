import pytest
import sqlite3

from .. import queries
from .. import models


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


def test_insert_into_podcast_table(database):
    pod = models.PodcastIn("pod_title_3", "pod_url_3")
    queries.insert_into_podcast_table(database, pod)
    assert queries.get_a_podcast_by_title(database, "pod_title_3") == (
        3,
        "pod_title_3",
        "pod_url_3",
    )


def test_update_a_podcast_title_by_title(database):
    queries.update_a_podcast_title_by_title(database, "pod_title_2", "new_pod_title_2")
    assert queries.get_a_podcast_by_title(database, "new_pod_title_2") == (
        2,
        "new_pod_title_2",
        "pod_url_2",
    )


def test_update_a_podcast_url_by_title(database):
    queries.update_a_podcast_url_by_title(database, "pod_title", "new_pod_url")
    assert queries.get_a_podcast_by_title(database, "pod_title") == (
        1,
        "pod_title",
        "new_pod_url",
    )


def test_delete_a_podcast_by_title(database):
    queries.delete_a_podcast_by_title(database, "pod_title")
    assert queries.get_all_podcasts(database) == [
        (2, "new_pod_title_2", "pod_url_2"),
        (3, "pod_title_3", "pod_url_3"),
    ]
