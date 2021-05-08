from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivymd.uix.label import MDLabel

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from Database.database import Brick, Manual, Set


class PopupContent(BoxLayout):
    def __init__(self, item, *args, **kwargs):
        super().__init__(**kwargs)

        if isinstance(item, Brick):
            color_label = MDLabel(text='Color (HEX): ' + item.color)
            type_label = MDLabel(text='Type (standard, special): ' + item.type)
            self.add_widget(color_label)
            self.add_widget(type_label)

        elif isinstance(item, Manual):
            pages_label = MDLabel(text='Number of pages: ' + str(item.number_of_pages))
            self.add_widget(pages_label)

        elif isinstance(item, Set):
            year_label = MDLabel(text='Released in year: ' + str(item.year))
            pieces_label = MDLabel(text='Number of pieces: ' + str(item.number_of_pieces))
            price_label = MDLabel(text='Price: ' + str(item.price) + '$')

            self.add_widget(year_label)
            self.add_widget(pieces_label)
            self.add_widget(price_label)


        self.add_widget(Image(source='img/'+item.image))



class DetailPopup(MDDialog):
    def __init__(self, id, cls):
        app = MDApp.get_running_app()
        item = app.db.read_by_id(cls, id)
        super().__init__(
            type="custom",
            content_cls=PopupContent(item),
            text='Titulek fotky',
            size_hint=(.8, 1),
            buttons = [
                MDFlatButton(text='Cancel', on_release=self.cancel_dialog)
            ]
        )
        self.title = item.name + '\nFactory number: [' + str(item.id) + ']'

    def cancel_dialog(self, *args):
        self.dismiss()

