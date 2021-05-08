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
    podcast_title: str
    number: int
    title: str
    url: str
    date: str

    def __str__(self):
        return f"{self.number}: {self.title} ({self.date})"
