import parser
import queries
import models
import downloader


def get_all_podcasts():
    podcasts = sorted(queries.get_all_podcasts(), key=lambda pod: pod[1])
    return [models.PodcastOut(pod[0], pod[1], pod[2]) for pod in podcasts]


def get_podcast_info_and_save_to_database(url):
    title = parser.get_podcast_title(parser.get_parsed_url(url))
    queries.insert_into_podcast_table(models.PodcastIn(title, url))


def episode_has_audio_url(episode):
    return bool(parser.get_audio_urls(parser.get_entry_enclosures(episode)))


def get_all_episodes_from_feed(url):
    parsed_url = parser.get_parsed_url(url)
    pod_title = parser.get_podcast_title(parsed_url)
    episodes = parser.get_items(parser.get_parsed_url(url))
    obj_episodes = []
    for episode in episodes:
        if episode_has_audio_url(episode):
            obj_episodes.append(
                models.Episode(
                    podcast_title=pod_title,
                    number=None,
                    title=parser.get_an_episode_title(episode),
                    # Gives a list with only 1 string value
                    url=parser.get_audio_urls(parser.get_entry_enclosures(episode))[0],
                    date=parser.get_an_episode_date(episode),
                )
            )

    for idx, ep in enumerate(reversed(obj_episodes)):
        ep.number = idx

    return obj_episodes


def download_episode(episode):
    downloader.download_file(episode)
    return f"Download completed: {episode.title}"


def _get_a_podcast_by_title(title):
    pod = queries.get_a_podcast_by_title(title)
    return models.PodcastOut(pod[0], pod[1], pod[2])


def get_podcast_and_its_episode_from_title(podcast_title):
    return get_all_episodes_from_feed(_get_a_podcast_by_title(podcast_title).url)


def delete_a_podcast_by_title(title):
    queries.delete_a_podcast_by_title(title)
