# import curses
import npyscreen
import concurrent.futures
import threading

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

        self.box3 = self.add(
            BoxMultiLine,
            height=20,
            # contained_widget=npyscreen.MultiLine,
            # contained_widget_arguments={"values": ["fffff", "aaaa"]},
        )

        self.box4 = self.add(BoxMultiLine, height=10)
        self.box4.name = "Status"

        # Keybindings:
        self.entry.entry_widget.add_handlers({"^A": self.get_info})
        self.box.entry_widget.add_handlers({"^A": self.get_episode_list})
        self.box2.entry_widget.add_handlers({"^A": self.episode_to_download})
        self.box3.entry_widget.add_handlers({"^A": self.download_episodes})

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
        # ep_info = [(ep.number, ep.title, ep.date) for ep in all_episodes]
        # self.box2.values = ep_info
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
        # for episode in episodes:
        #    self.box4.values.append(
        #        f"{episode.number}: {episode.title} - is downloading."
        #    )
        #    self.box4.display()
        #    api.download_episode(episode)
        #    self.box4.values.append(
        #        f"{episode.number}: {episode.title} - is downloaded."
        #    )
        #    self.box4.display()
        self.box3.values = []
        self.box3.display()

    def download_concurrently(self):
        episodes = self.box3.values
        self.box4.values.append("start")
        self.box4.display()
        with concurrent.futures.ThreadPoolExecutor() as tpexec:
            tpexec.map(api.download_episode, episodes)
        self.box4.values.append("end")
        self.box4.display()


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
        # self.values = ["fake", "value"]


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
