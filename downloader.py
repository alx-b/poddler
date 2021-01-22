import httpx
from pathlib import Path


def create_podcast_folder(folder_name):
    Path(f"{Path.home()}/Music/podcasts/{folder_name}/").mkdir(
        parents=True, exist_ok=True
    )


def download_file(episode):
    pod_title = episode.podcast_title.replace(" ", "_")
    ep_title = episode.title.replace(" ", "_")
    create_podcast_folder(pod_title)
    with httpx.stream("GET", episode.url) as stream:
        with open(
            f"{Path.home()}/Music/podcasts/{pod_title}/{episode.number}._{ep_title}.mp3",
            "wb",
        ) as file:
            for chunk in stream.iter_bytes():
                if chunk:
                    file.write(chunk)
