from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from Database.database import Brick, Manual, Set
from Screens.EditPopup import EditablePopup


class PopupContent(BoxLayout):
    def __init__(self, item, *args, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.redraw()

    def redraw(self):
        self.clear_widgets()

        if isinstance(self.item, Brick):
            color_label = MDLabel(text='Color (HEX): ' + self.item.color)
            type_label = MDLabel(text='Type (standard, special): ' + self.item.type)
            self.add_widget(color_label)
            self.add_widget(type_label)

        elif isinstance(self.item, Manual):
            pages_label = MDLabel(text='Number of pages: ' + str(self.item.number_of_pages))
            self.add_widget(pages_label)

        elif isinstance(self.item, Set):
            year_label = MDLabel(text='Released in year: ' + str(self.item.year))
            pieces_label = MDLabel(text='Number of pieces: ' + str(self.item.number_of_pieces))
            price_label = MDLabel(text='Price: ' + str(self.item.price) + '$')

            self.add_widget(year_label)
            self.add_widget(pieces_label)
            self.add_widget(price_label)

        self.add_widget(Image(source='img/'+self.item.image))


class DetailPopup(MDDialog):
    def __init__(self, id, cls):

        self.app = MDApp.get_running_app()
        self.item = self.app.db.read_by_id(cls, id)
        super().__init__(
            type="custom",
            content_cls=PopupContent(self.item),
            text='Titulek fotky',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Edit', on_release=self.edit_item),
                MDFlatButton(text='Delete', on_release=self.delete_item),
                MDFlatButton(text='Cancel', on_release=self.cancel_dialog)
            ]
        )
        self.title = self.item.name + '\nFactory number: [' + str(self.item.id) + ']'

    def cancel_dialog(self, *args):
        self.dismiss()

    def edit_item(self, *args):
        popup = EditablePopup(item=self.item, editing_item=self)
        popup.open()

    def delete_item(self, *args):
        self.app.db.delete(type(self.item), self.item.id)

        self.app.redraw_screen_with_item(self.item)

        self.dismiss()
