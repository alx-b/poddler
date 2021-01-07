from dataclasses import dataclass


@dataclass
class PodcastIn:
    title: str
    url: str


@dataclass
class PodcastOut:
    pk: int
    title: str
    url: str


@dataclass
class Episode:
    # podcast_id: int
    number: int
    title: str
    url: str
    date: str
