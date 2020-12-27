from typing import List, Dict, Optional
import itertools
import feedparser


def has_no_bozo_error(parsed_url) -> bool:
    return not bool(parsed_url.bozo)


def has_entries(parsed_url) -> bool:
    return bool(parsed_url.entries)


def has_a_version(parsed_url) -> bool:
    return bool(parsed_url.version)


def is_not_none(parsed_url) -> bool:
    return bool(parsed_url is not None)


def has_no_error(parsed_url) -> Optional[feedparser.util.FeedParserDict]:
    if (
        has_no_bozo_error(parsed_url)
        and has_entries(parsed_url)
        and has_a_version(parsed_url)
    ):
        return parsed_url
    return None


def get_parsed_url(url: str) -> Optional[feedparser.util.FeedParserDict]:
    return has_no_error(feedparser.parse(url))


def url_is_parsable(url: str) -> bool:
    try:
        return bool(feedparser.parse(url).version)
    except AttributeError:
        print("No version")
    return False


# Podcast overall info


def get_podcast_title(parsed_url) -> str:
    return parsed_url.feed.title


def get_podcast_description(parsed_url) -> str:
    return parsed_url.feed.description


def get_podcast_image_url(parsed_url) -> str:
    return parsed_url.feed.image.url


# Episode info


def get_items(parsed_url) -> List[feedparser.util.FeedParserDict]:
    return parsed_url.entries


def get_episodes_title(items) -> List[str]:
    return [item["title"] for item in items]


def get_episodes_date(items) -> List[str]:
    return [item.published for item in items]


def get_entries_enclosures(items) -> List[List]:
    return [item.enclosures for item in items]


def is_audio_url(item) -> bool:
    try:
        return bool("audio" in item.type)
    except AttributeError:
        print("No type")
    return False


def flatten_iterable(enclosures) -> itertools.chain:
    return itertools.chain.from_iterable(enclosures)


def get_audio_urls(flat_iterable) -> List[str]:
    return [item.href for item in flat_iterable if is_audio_url(item)]
