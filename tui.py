# import curses
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

        self.box = self.add(
            BoxOneChoice,
            height=25,
        )

        self.box2 = self.add(
            BoxMultiChoice,
            height=25,
        )

        self.box3 = self.add(
            BoxMultiLine,
            height=25,
            # contained_widget=npyscreen.MultiLine,
            # contained_widget_arguments={"values": ["fffff", "aaaa"]},
        )

        # Keybindings:
        self.entry.entry_widget.add_handlers({"^A": self.get_info})
        self.box.entry_widget.add_handlers({"^A": self.get_episode_list})
        self.box2.entry_widget.add_handlers({"^A": self.episode_to_download})

        self.get_podcast_list()

    def get_podcast_list(self, *args):
        podcasts = api.get_all_podcasts()
        self.box.values = [podcast.title for podcast in podcasts]
        self.box.display()

    def get_episode_list(self, *args):
        pod_title = self.box.entry_widget.get_selected_objects()[0]
        podcast = api.get_a_podcast_by_title(pod_title)
        all_episodes = api.get_all_episodes_from_feed(podcast.url)
        ep_info = [(ep.number, ep.title, ep.date) for ep in all_episodes]
        self.box2.values = ep_info
        self.box2.display()

    def get_info(self, *args):
        url = self.entry.value
        self.entry.value = ""
        api.get_podcast_info_and_save_to_database(url)
        self.get_podcast_list()

    def episode_to_download(self, *args):
        pod_title = self.box.entry_widget.get_selected_objects()[0]
        podcast = api.get_a_podcast_by_title(pod_title)
        ep_titles = self.box2.entry_widget.get_selected_objects()
        # TODO
        # self.box3.values = selected_title
        # self.box3.display()


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
