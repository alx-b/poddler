import httpx
from pathlib import Path


def download_file(episode):
    with httpx.stream("GET", episode.url) as stream:
        with open(
            f"{Path.home()}/Music/podcasts/{episode.number}._{episode.title}.mp3",
            "wb",
        ) as file:
            for chunk in stream.iter_bytes():
                if chunk:
                    file.write(chunk)
