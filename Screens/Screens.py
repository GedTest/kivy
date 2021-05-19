from Database.database import Brick
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout

from DetailPopup import DetailPopup


class Card(MDCard):
    def __init__(self, obj, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.item = obj

        self.ids.card_img.source = 'img/'+self.item.image
        self.ids.card_name.text = self.item.name

    def on_release(self):
        popup = DetailPopup(id=self.item.id, cls=type(self.item))
        popup.open()


class ScrollList(ScrollView):
    pass


class Screens(MDBoxLayout):

    def __init__(self, **kwargs):
        super(Screens, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.redraw()

    def redraw(self):
        self.clear_widgets()
        scroll_list = ScrollList()
        database_objects = self.app.db.read(type(self.app.current_type))

        for object in database_objects:
            new_card = Card(obj=object)
            scroll_list.ids.card_list.add_widget(new_card)

        self.add_widget(scroll_list)
