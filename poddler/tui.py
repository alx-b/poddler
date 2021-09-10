# import curses
import concurrent.futures
import threading
import urllib
import npyscreen

import handler

# npyscreen.disableColor()


class AppForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self) -> None:
        """Initialization (equivalent to __init__)"""
        # Widgets:
        self.url = self.add(
            BoxUrl, height=3, contained_widget_arguments={"name": "url:"}
        )
        self.podcast = self.add(BoxPodcast, height=12)
        self.episode = self.add(BoxEpisode, height=12)
        self.status = self.add(BoxStatus, height=10)
        # Keybindings:
        self.url.entry_widget.add_handlers({"^A": self.get_info})
        self.podcast.entry_widget.add_handlers({"^A": self.get_episode_list})
        self.podcast.entry_widget.add_handlers({"^D": self.delete_selected_podcast})
        self.episode.entry_widget.add_handlers({"^A": self.download_episodes})

        self.podcast.get_podcast_list()

    def get_info(self, *args) -> None:
        """Gets podcast info, saves to database, display podcasts

        Parameters:
            *args: Needed for keybinding
        """
        try:
            handler.get_podcast_info_and_save_to_database(self.url.value)
        except AttributeError:
            self.status.values.append("Not an URL!")
        except urllib.error.URLError:
            self.status.values.append("Invalid URL")

        self.url.value = ""
        self.status.display()
        self.podcast.get_podcast_list()

    def get_episode_list(self, *args) -> None:
        """Gets and display episodes of the selected podcast

        Parameters:
            *args: Needed for keybinding
        """
        try:
            self.episode.values = ["Loading..."]
            self.episode.display()
            self.episode.values = handler.get_podcast_and_its_episode_from_title(
                self.podcast.get_selected_podcast_title()
            )
            self.episode.display()
        except IndexError:
            self.status.values.append("You haven't select a podcast!")
            self.status.display()
        self.episode.value = []

    def delete_selected_podcast(self, *args) -> None:
        """Delete selected podcast and refresh podcast list

        Parameters:
            *args: Needed for keybinding
        """
        try:
            handler.delete_a_podcast_by_title(self.podcast.get_selected_podcast_title())
        except IndexError:
            self.status.values.append("You haven't select a podcast!")
            self.status.display()

        self.podcast.value = []
        self.podcast.get_podcast_list()

    def download_episodes(self, *args) -> None:
        """Start downloading thread

        Parameters:
            *args: Needed for keybinding
        """
        threading.Thread(target=self._download_concurrently, daemon=True).start()

    def _download_concurrently(self) -> None:
        try:
            episodes = self.episode.entry_widget.get_selected_objects()
            self.episode.value = []
            self.episode.display()
            with concurrent.futures.ThreadPoolExecutor() as tpexec:
                # Use .submit with list comprehension instead of .map,
                # else you get result in starting order
                downloads = [
                    tpexec.submit(handler.download_episode, ep) for ep in episodes
                ]
                for episode in episodes:
                    self.status.values.append(f"Download started: {episode.title}")
                self.status.display()

                for download in concurrent.futures.as_completed(downloads):
                    self.status.values.append(download.result())
                    self.status.display()
        except TypeError:
            self.status.values.append("You haven't select any episodes!")

        self.status.display()


class BoxUrl(npyscreen.BoxTitle):
    class Url(npyscreen.TitleText):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    _contained_widget = Url
    name = "Add a New Feed"


class BoxPodcast(npyscreen.BoxTitle):
    class Podcast(npyscreen.SelectOne):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    _contained_widget = Podcast
    name = "Podcasts"

    def get_selected_podcast_title(self):
        return self.entry_widget.get_selected_objects()[0]

    def get_podcast_list(self, *args):
        self.values = [podcast.title for podcast in handler.get_all_podcasts()]
        self.display()


class BoxEpisode(npyscreen.BoxTitle):
    class Episode(npyscreen.MultiSelect):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    _contained_widget = Episode
    name = "Episodes"


class BoxStatus(npyscreen.BoxTitle):
    class Status(npyscreen.MultiLine):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    _contained_widget = Status
    name = "Status"


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(PoddlerTheme)
        self.addForm("MAIN", AppForm, name="Poddler", color="LABEL")


class PoddlerTheme(npyscreen.ThemeManager):
    default_colors = {
        "DEFAULT": "WHITE_BLACK",
        "FORMDEFAULT": "WHITE_BLACK",
        "NO_EDIT": "BLUE_BLACK",
        "STANDOUT": "CYAN_BLACK",
        "CURSOR": "WHITE_BLACK",
        "CURSOR_INVERSE": "BLACK_WHITE",
        "LABEL": "BLUE_BLACK",
        "LABELBOLD": "WHITE_BLACK",
        "CONTROL": "BLUE_BLACK",
        "IMPORTANT": "GREEN_BLACK",
        "SAFE": "GREEN_BLACK",
        "WARNING": "YELLOW_BLACK",
        "DANGER": "RED_BLACK",
        "CRITICAL": "BLACK_RED",
        "GOOD": "GREEN_BLACK",
        "GOODHL": "GREEN_BLACK",
        "VERYGOOD": "BLACK_GREEN",
        "CAUTION": "YELLOW_BLACK",
        "CAUTIONHL": "BLACK_YELLOW",
    }


if __name__ == "__main__":
    app = Application().run()
