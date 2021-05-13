from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

from Database.database import Brick, Manual, Set


class Edit(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.app = MDApp.get_running_app()
        self.widgets = {}

        if not isinstance(self.app.database_objects[0], Brick):
            self.remove_widget(self.ids.edit_type)
            self.remove_widget(self.ids.edit_color)

            if isinstance(self.app.database_objects[0], Manual):
                num_of_pages_field = MDTextField()
                num_of_pages_field.id = 'edit_number_of_pages'
                num_of_pages_field.hint_text = 'Number of pages'

                self.add_widget(num_of_pages_field)
                self.widgets['number_of_pages'] = num_of_pages_field

            else:
                FIELDS = ['Year', 'Number of pieces', 'Price']

                for field in FIELDS:
                    new_field = MDTextField()
                    new_field.id = 'edit_'+str(field.replace(' ', '_')).lower()
                    new_field.hint_text = field

                    self.add_widget(new_field)
                    self.widgets[str(field.replace(' ', '_')).lower()] = new_field


class EditablePopup(MDDialog):
    def __init__(self, item, editing_item):
        super(EditablePopup, self).__init__(
            type="custom",
            content_cls=Edit(),
            title='Edit item',
            text='Ahoj',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Save changes', on_release=self.save_dialog),
                MDFlatButton(text='Cancel', on_release=self.cancel_dialog)
            ]
        )
        self.item = item
        self.editing_item = editing_item

    def cancel_dialog(self, *args):
        self.dismiss()

    def save_dialog(self, *args):
        updated_item = self.item
        a = updated_item.name
        b = self.content_cls.ids.edit_name.text

        name = a if ((a==b) or (b=='')) else b
        updated_item.name = name

        if isinstance(updated_item, Brick):
            updated_item.color = self.validate(self.content_cls.ids.edit_color.text, '#')
            updated_item.type = self.validate(self.content_cls.ids.edit_type.text, 'standard')

        elif isinstance(updated_item, Manual):
            updated_item.number_of_pages = self.validate(self.content_cls.widgets['number_of_pages'].text, 0)

        elif isinstance(updated_item, Set):
            updated_item.year = self.validate(self.content_cls.widgets['year'].text, 0)
            updated_item.number_of_pieces = self.validate(self.content_cls.widgets['number_of_pieces'].text, 0)
            updated_item.price = self.validate(self.content_cls.widgets['price'].text, 0)

        self.editing_item.content_cls.redraw()

        app = MDApp.get_running_app()
        app.db.update()

        self.dismiss()

    def validate(self, str, default_value):
        return str if (str!='') else default_value
