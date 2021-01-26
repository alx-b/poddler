# import curses
import concurrent.futures
import threading
import npyscreen

import api


class AppForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.entry = self.add(
            BoxTextField,
            height=3,
            contained_widget_arguments={"name": "url:"},
        )

        self.box = self.add(BoxOneChoice, height=20)
        self.box2 = self.add(BoxMultiChoice, height=20)
        self.box3 = self.add(BoxMultiLine, height=20)
        self.box4 = self.add(BoxMultiLine, height=10)
        self.box4.name = "Status"

        # Keybindings:
        self.entry.entry_widget.add_handlers({"^A": self.get_info})
        self.box.entry_widget.add_handlers({"^A": self.get_episode_list})
        self.box2.entry_widget.add_handlers({"^A": self.episode_to_download})
        self.box3.entry_widget.add_handlers({"^A": self.download_episodes})
        self.box.entry_widget.add_handlers({"^D": self.delete_selected_podcast})

        self.episodes_to_dl = []

        self.get_podcast_list()

    def get_info(self, *args):
        url = self.entry.value
        self.entry.value = ""
        api.get_podcast_info_and_save_to_database(url)
        self.get_podcast_list()

    def get_podcast_list(self, *args):
        podcasts = api.get_all_podcasts()
        self.box.values = [podcast.title for podcast in podcasts]
        self.box.display()

    def get_episode_list(self, *args):
        self.box2.value = []
        pod_title = self.box.entry_widget.get_selected_objects()[0]
        episodes = api.get_podcast_and_its_episode_from_title(pod_title)
        self.box2.values = episodes
        self.box2.display()

    def episode_to_download(self, *args):
        self.episodes_to_dl += self.box2.entry_widget.get_selected_objects()
        self.box2.value = []
        self.box3.values = self.episodes_to_dl
        self.box3.display()

    def download_episodes(self, *args):
        self.episodes_to_dl = []
        thread1 = threading.Thread(target=self.download_concurrently, daemon=True)
        thread1.start()
        self.box3.values = []
        self.box3.display()

    def download_concurrently(self):
        episodes = self.box3.values
        with concurrent.futures.ThreadPoolExecutor() as tpexec:
            # Use .submit with list comprehension instead of .map,
            # else you get result in starting order
            downloads = [tpexec.submit(api.download_episode, ep) for ep in episodes]
            for episode in episodes:
                self.box4.values.append(f"Download started: {episode.title}")
            self.box4.display()

            for download in concurrent.futures.as_completed(downloads):
                self.box4.values.append(download.result())
                self.box4.display()

        self.box4.display()

    def delete_selected_podcast(self, *args):
        pod_title = self.box.entry_widget.get_selected_objects()[0]
        api.delete_a_podcast_by_title(pod_title)
        self.box.value = []
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
    name = "To Download"


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm(
            "MAIN",
            AppForm,
            name="Poddler",
        )


if __name__ == "__main__":
    app = Application().run()
