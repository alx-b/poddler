from typing import List, Dict, Optional, Iterable
import itertools
import feedparser
from feedparser.util import FeedParserDict


def _has_no_bozo_error(parsed_url: FeedParserDict) -> bool:
    return not bool(parsed_url.bozo)


def _has_entries(parsed_url: FeedParserDict) -> bool:
    return bool(parsed_url.entries)


def _has_a_version(parsed_url: FeedParserDict) -> bool:
    return bool(parsed_url.version)


def _has_no_error(parsed_url: FeedParserDict) -> Optional[FeedParserDict]:
    if (
        _has_no_bozo_error(parsed_url)
        and _has_entries(parsed_url)
        and _has_a_version(parsed_url)
    ):
        return parsed_url
    return None


def get_parsed_url(url: str) -> Optional[FeedParserDict]:
    return _has_no_error(feedparser.parse(url))


# Podcast overall info


def get_podcast_title(parsed_url: FeedParserDict) -> str:
    return parsed_url.feed.title


def get_podcast_description(parsed_url: FeedParserDict) -> str:
    return parsed_url.feed.description


def get_podcast_image_url(parsed_url: FeedParserDict) -> str:
    return parsed_url.feed.image.url


# Episode info


def get_items(parsed_url: FeedParserDict) -> List[FeedParserDict]:
    return parsed_url.entries


def get_an_episode_title(item: FeedParserDict) -> str:
    return item["title"]


def get_an_episode_date(item: FeedParserDict) -> List[str]:
    return item.published


def get_entry_enclosure(item: FeedParserDict) -> List:
    return item.enclosures


def _is_audio_url(item: FeedParserDict) -> bool:
    try:
        return bool("audio" in item.type)
    except AttributeError:
        print("No type")
    return False


def get_audio_urls(iterable: Iterable) -> List[str]:
    return [item.href for item in iterable if _is_audio_url(item)]
