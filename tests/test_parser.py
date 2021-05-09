import pytest
import feedparser
from feedparser.util import FeedParserDict
import pathlib

from poddler import parser


def get_path():
    path = f"{pathlib.Path.cwd()}/fake_rss_feed.xml"
    path2 = f"{pathlib.Path.cwd()}/tests/fake_rss_feed.xml"
    return path if pathlib.Path(path).exists() else path2


FEED_URL = get_path()


@pytest.fixture(scope="session")
def parsed_url():
    return feedparser.parse(FEED_URL)


def test_bozo_error(parsed_url):
    assert parser._has_no_bozo_error(parsed_url) is True


def test_has_entries(parsed_url):
    assert parser._has_entries(parsed_url) is True


def test_feed_has_a_version(parsed_url):
    assert parser._has_a_version(parsed_url) is True


def test_has_no_error(parsed_url):
    assert parser._has_no_error(parsed_url) == parsed_url


def test_get_parsed_url(parsed_url):
    assert parser.get_parsed_url(FEED_URL) == parsed_url


def test_get_podcast_title(parsed_url):
    assert parser.get_podcast_title(parsed_url) == "Channel/Podcast Title"


def test_get_items(parsed_url):
    assert parser.get_items(parsed_url) == parsed_url.entries


def test_get_an_episode_title(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_an_episode_title(items[0]) == "2: EPISODE TITLE"


def test_get_episode_date(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_an_episode_date(items[0]) == "Fri, 18 Dec 2019 05:00:43 +0000"


def test_get_entry_enclosures(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_entry_enclosures(items[0]) == [
        {
            "length": "50270833",
            "type": "audio/mpeg",
            "href": "https://url-to-episode2.mp3",
        }
    ]


def test_is_audio_url(parsed_url):
    pass


def test_get_audio_urls(parsed_url):
    items = parser.get_items(parsed_url)
    item = items[0]
    enclosures = parser.get_entry_enclosures(item)
    assert parser.get_audio_urls(enclosures) == [
        "https://url-to-episode2.mp3",
    ]
