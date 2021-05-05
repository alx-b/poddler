# import curses
import concurrent.futures
import threading
import urllib
import npyscreen

import handler


class AppForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        # Widgets:
        self.url = self.add(
            BoxTextField,
            height=3,
            contained_widget_arguments={"name": "url:"},
        )
        self.podcast = self.add(BoxOneChoice, height=20)
        self.episode = self.add(BoxMultiChoice, height=20)
        #self.download = self.add(BoxMultiLine, height=20, name="To Download")
        self.status = self.add(BoxMultiLine, height=10, name="Status")

        # Keybindings:
        self.url.entry_widget.add_handlers({"^A": self.get_info})
        self.podcast.entry_widget.add_handlers({"^A": self.get_episode_list})
        self.episode.entry_widget.add_handlers({"^A": self.download_episodes2})
        #self.episode.entry_widget.add_handlers({"^A": self.episode_to_download})
        #self.download.entry_widget.add_handlers({"^A": self.download_episodes})
        self.podcast.entry_widget.add_handlers({"^D": self.delete_selected_podcast})

        self.to_download = None

        self.episodes_to_dl = []

        self.get_podcast_list()

    def get_info(self, *args):
        url = self.url.value
        self.url.value = ""

        try:
            handler.get_podcast_info_and_save_to_database(url)
        except AttributeError:
            self.status.values.append("Not an URL!")
        except urllib.error.URLError:
            self.status.values.append("Invalid URL")

        self.status.display()

        self.get_podcast_list()

    def get_podcast_list(self, *args):
        podcasts = handler.get_all_podcasts()
        self.podcast.values = [podcast.title for podcast in podcasts]
        self.podcast.display()

    def get_episode_list(self, *args):
        try:
            pod_title = self.podcast.entry_widget.get_selected_objects()[0]
            episodes = handler.get_podcast_and_its_episode_from_title(pod_title)
            self.episode.values = episodes
            self.episode.display()
        except IndexError:
            self.status.values.append("You haven't select a podcast!")
            self.status.display()
        self.episode.value = []

    #def episode_to_download(self, *args):
    #    try:
    #        self.episodes_to_dl += self.episode.entry_widget.get_selected_objects()
    #        self.download.values = self.episodes_to_dl
    #        self.download.display()
    #    except TypeError:
    #        self.status.values.append("You haven't select an episode!")
    #        self.status.display()
    #    self.episode.value = []

    def download_episodes2(self, *args):
        #self.download.values = self.episode.entry_widget.get_selected_objects()
        self.to_download = self.episode.entry_widget.get_selected_objects()
        thread1 = threading.Thread(target=self.download_concurrently, daemon=True)
        thread1.start()
        self.episode.value = []
        self.episode.display()
        

    def download_episodes(self, *args):
        self.episodes_to_dl = []
        thread1 = threading.Thread(target=self.download_concurrently, daemon=True)
        thread1.start()
        #self.download.values = []
        #self.download.display()

    def download_concurrently(self):
        #episodes = self.download.values
        episodes = self.to_download
        with concurrent.futures.ThreadPoolExecutor() as tpexec:
            # Use .submit with list comprehension instead of .map,
            # else you get result in starting order
            downloads = [tpexec.submit(handler.download_episode, ep) for ep in episodes]
            for episode in episodes:
                self.status.values.append(f"Download started: {episode.title}")
            self.status.display()

            for download in concurrent.futures.as_completed(downloads):
                self.status.values.append(download.result())
                self.status.display()

        self.status.display()

    def delete_selected_podcast(self, *args):
        try:
            pod_title = self.podcast.entry_widget.get_selected_objects()[0]
            handler.delete_a_podcast_by_title(pod_title)
        except IndexError:
            self.status.values.append("You haven't select a podcast!")
            self.status.display()

        self.podcast.value = []
        self.get_podcast_list()


class TextField(npyscreen.TitleText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OneChoice(npyscreen.SelectOne):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MultiChoice(npyscreen.MultiSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MultiLine(npyscreen.MultiLine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BoxTextField(npyscreen.BoxTitle):
    _contained_widget = TextField
    name = "Add a New Feed"


class BoxOneChoice(npyscreen.BoxTitle):
    _contained_widget = OneChoice
    name = "Podcasts"


class BoxMultiChoice(npyscreen.BoxTitle):
    _contained_widget = MultiChoice
    name = "Episodes"


class BoxMultiLine(npyscreen.BoxTitle):
    _contained_widget = MultiLine


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm(
            "MAIN",
            AppForm,
            name="Poddler",
        )


if __name__ == "__main__":
    app = Application().run()
