import pytest
import feedparser
from feedparser.util import FeedParserDict
import pathlib

from .. import parser

# FEED_URL = f"{pathlib.Path.cwd()}/fake_rss_feed.xml"


def get_path():
    path = f"{pathlib.Path.cwd()}/fake_rss_feed.xml"
    path2 = f"{pathlib.Path.cwd()}/tests/fake_rss_feed.xml"
    return path if pathlib.Path(path).exists() else path2


FEED_URL = get_path()


@pytest.fixture(scope="session")
def parsed_url():
    return feedparser.parse(FEED_URL)


@pytest.mark.parametrize("url, result", [(FEED_URL, True), ("", False)])
def test_url_is_parsable(url, result):
    assert parser.url_is_parsable(url) is result


def test_bozo_error(parsed_url):
    assert parser.has_no_bozo_error(parsed_url) is True


def test_has_entries(parsed_url):
    assert parser.has_entries(parsed_url) is True


def test_feed_has_a_version(parsed_url):
    assert parser.has_a_version(parsed_url) is True


def test_has_no_error(parsed_url):
    assert parser.has_no_error(parsed_url) == parsed_url


def test_get_parsed_url(parsed_url):
    assert parser.get_parsed_url(FEED_URL) == parsed_url


def test_get_podcast_title(parsed_url):
    assert parser.get_podcast_title(parsed_url) == "Channel/Podcast Title"


def test_is_not_none(parsed_url):
    assert parser.is_not_none(parsed_url) is True


def test_get_podcast_description(parsed_url):
    assert parser.get_podcast_description(parsed_url) == "itunes summary"


def test_get_podcast_image_url(parsed_url):
    assert (
        parser.get_podcast_image_url(parsed_url)
        == "https://podnetwork.com/wp-content/uploads/2020/09/PodcastTitle_2000x2000.jpg"
    )


def test_get_items(parsed_url):
    assert parser.get_items(parsed_url) == parsed_url.entries


def test_get_episodes_title(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_episodes_title(items) == [
        "2: EPISODE TITLE",
        "1: EPISODE TITLE",
    ]


def test_get_an_episode_title(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_an_episode_title(items[0]) == "2: EPISODE TITLE"


def test_get_episodes_date(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_episodes_date(items) == [
        "Fri, 18 Dec 2019 05:00:43 +0000",
        "Mon, 28 Sep 2019 08:00:18 +0000",
    ]


def test_get_episode_date(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_an_episode_date(items[0]) == "Fri, 18 Dec 2019 05:00:43 +0000"


def test_get_entries_enclosures(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_entries_enclosures(items) == [
        [
            {
                "length": "50270833",
                "type": "audio/mpeg",
                "href": "https://url-to-episode2.mp3",
            }
        ],
        [
            {
                "length": "48970827",
                "type": "audio/mpeg",
                "href": "https://url-to-episode1.mp3",
            }
        ],
    ]


def test_get_entry_enclosures(parsed_url):
    items = parser.get_items(parsed_url)
    assert parser.get_entry_enclosure(items[0]) == [
        {
            "length": "50270833",
            "type": "audio/mpeg",
            "href": "https://url-to-episode2.mp3",
        }
    ]


def test_is_audio_url(parsed_url):
    items = parser.get_items(parsed_url)
    enclosures = parser.get_entries_enclosures(items)
    iterable = list(parser.flatten_iterable(enclosures))
    assert parser.is_audio_url(iterable[0]) is True


def test_flatten_iterable(parsed_url):
    items = parser.get_items(parsed_url)
    enclosures = parser.get_entries_enclosures(items)
    assert parser.flatten_iterable(enclosures) is not None


def test_get_audio_urls(parsed_url):
    items = parser.get_items(parsed_url)
    enclosures = parser.get_entries_enclosures(items)
    iterable = parser.flatten_iterable(enclosures)
    assert parser.get_audio_urls(iterable) == [
        "https://url-to-episode2.mp3",
        "https://url-to-episode1.mp3",
    ]
