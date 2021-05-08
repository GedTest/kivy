from kivymd.app import MDApp
from kivymd.uix.card import MDCard
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


class Screens(MDBoxLayout):

    def __init__(self, **kwargs):
        super(Screens, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.redraw()

    def redraw(self):
        self.clear_widgets()
        database_objects = self.app.database_objects

        for object in database_objects:
            new_card = Card(obj=object)
            self.add_widget(new_card)
