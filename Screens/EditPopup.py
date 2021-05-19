from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast

from kivymd.uix.filemanager import MDFileManager

from kivymd.uix.menu import MDDropdownMenu

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

from Database.database import Brick, Manual, Set


DEFAULT_IMAGE = 'LEGO_LOGO.png'
BASE_DIR = str(Path(__file__).resolve().parent.parent).replace("\\", '/')


class Edit(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.app = MDApp.get_running_app()
        self.widgets = {}

        self.image = ''
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )






        if isinstance(self.app.database_objects[0], Brick):
            self.remove_widget(self.ids.edit_foreign_key)
            TYPES = ('standard', 'special')
            menu_items = [{"viewclass": "OneLineListItem", "text": f"{type}",
                           "on_release": lambda x=f"{type}": self.set_item(x, 'edit_type')} for type in TYPES]

            self.menu_types = MDDropdownMenu(
                caller=self.ids.edit_type,
                items=menu_items,
                position="center",
                width_mult=5,
            )

        else:
            self.remove_widget(self.ids.edit_type)
            self.remove_widget(self.ids.edit_color)

            if isinstance(self.app.database_objects[0], Manual):
                num_of_pages_field = MDTextField()
                num_of_pages_field.id = 'edit_number_of_pages'
                num_of_pages_field.hint_text = 'Number of pages'

                self.add_widget(num_of_pages_field)
                self.widgets['number_of_pages'] = num_of_pages_field

                SETS = self.app.db.read(Set)
                menu_items = [{"viewclass": "OneLineListItem", "text": f"{set}",
                               "on_release": lambda x=f"{set}": self.set_item(x, 'edit_foreign_key')} for set in SETS]

                self.menu_types = MDDropdownMenu(
                    caller=self.ids.edit_foreign_key,
                    items=menu_items,
                    position="center",
                    width_mult=5,
                )
            else:
                self.remove_widget(self.ids.edit_foreign_key)
                FIELDS = ['Year', 'Number of pieces', 'Price']

                for field in FIELDS:
                    new_field = MDTextField()
                    new_field.id = 'edit_'+str(field.replace(' ', '_')).lower()
                    new_field.hint_text = field

                    self.add_widget(new_field)
                    self.widgets[str(field.replace(' ', '_')).lower()] = new_field

    def set_item(self, text_item, widget):
        self.ids[widget].set_item(text_item)
        self.ids[widget].text = text_item

        self.menu_types.dismiss()





    def file_manager_open(self):
        cls = str(type(self.app.current_type)).split('.')[2][:-2]
        self.file_manager.show(BASE_DIR + '/img/' + cls)
        self.manager_open = True

    def select_path(self, path):
        cls = str(type(self.app.current_type)).split('.')[2][:-2]

        splitted_path = path.replace("\\", '/').split('/')
        dest_dir = ''
        for fragment in splitted_path:
            if '.' in fragment:
                dest_dir = fragment
        self.image = cls + '/' + dest_dir

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()







def validate(str, default_value, cmpr_str=''):
    return str if (str != cmpr_str) else default_value


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
        self.app = MDApp.get_running_app()
        self.item = item
        self.editing_item = editing_item

    def cancel_dialog(self, *args):
        self.editing_item.dismiss()
        self.dismiss()

    def save_dialog(self, *args):
        updated_item = self.item
        a = updated_item.name
        b = self.content_cls.ids.edit_name.text

        name = a if ((a==b) or (b=='')) else b
        updated_item.name = name

        last_id = self.app.db.read_last_id(type(updated_item))
        updated_item.id = validate(self.content_cls.ids.edit_id.text, last_id + 1)

        updated_item.image = validate(self.content_cls.image, DEFAULT_IMAGE)

        if isinstance(updated_item, Brick):
            updated_item.color = validate(self.content_cls.ids.edit_color.text, '#')
            updated_item.type = validate(self.content_cls.ids.edit_type.text, 'standard', 'Type')

        elif isinstance(updated_item, Manual):
            updated_item.number_of_pages = validate(self.content_cls.widgets['number_of_pages'].text, 0)

        elif isinstance(updated_item, Set):
            updated_item.year = validate(self.content_cls.widgets['year'].text, 0)
            updated_item.number_of_pieces = validate(self.content_cls.widgets['number_of_pieces'].text, 0)
            updated_item.price = validate(self.content_cls.widgets['price'].text, 0)

        self.app.db.update()
        self.app.redraw_screen_with_item(self.app.current_type)
        self.dismiss()
