from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget

person_list = [
    {"name": "Anna Nováková", "state": "CZE", "img": "images/AN.png"},
    {"name": "William Smith", "state": "USA", "img": "images/WS.png"},
    {"name": "Vanessa Ramirez", "state": "IND", "img": "images/VR.png"}
]


class MyItem(TwoLineAvatarListItem):

    def __init__(self, name, state, img, *args, **kwargs):
        super(MyItem, self).__init__(*args)
        self.text = name
        self.secondary_text = state
        self.image = ImageLeftWidget(source=img)
        self.add_widget(self.image)

    def on_press(self):
        print(self.text)

    def on_touch_down(self, touch):
        self.image.source = "images/WS.png"

    def on_touch_up(self, touch):
        self.image.source = "images/VR.png"


class Persons(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(Persons, self).__init__(orientation="horizontal")

        scroll_view = ScrollView()
        list_of_persons = MDList()

        for person in person_list:
            list_of_persons.add_widget(MyItem(name=person['name'], state=person['state'], img=person['img']))

        scroll_view.add_widget(list_of_persons)
        self.add_widget(scroll_view)
