import parser
import queries
import models


def get_all_podcasts():
    podcasts = queries.get_all_podcasts(queries.open_db())
    return [models.PodcastOut(pod[0], pod[1], pod[2]) for pod in podcasts]


def get_podcast_info_and_save_to_database(url):
    title = parser.get_podcast_title(parser.get_parsed_url(url))
    queries.insert_into_podcast_table(queries.open_db(), models.PodcastIn(title, url))


def get_a_podcast_by_title(title):
    pod = queries.get_a_podcast_by_title(queries.open_db(), title)
    return models.PodcastOut(pod[0], pod[1], pod[2])


def episode_has_audio_url(episode):
    return bool(parser.get_audio_urls(parser.get_entry_enclosure(episode)))


def get_all_episodes_from_feed(url):
    episodes = parser.get_items(parser.get_parsed_url(url))
    obj_episodes = []
    for episode in episodes:
        if episode_has_audio_url(episode):
            obj_episodes.append(
                models.Episode(
                    number=None,
                    title=parser.get_an_episode_title(episode),
                    # Gives a list with only 1 string value
                    url=parser.get_audio_urls(parser.get_entry_enclosure(episode))[0],
                    date=parser.get_an_episode_date(episode),
                )
            )

    for idx, ep in enumerate(reversed(obj_episodes)):
        ep.number = idx

    return obj_episodes
