from Screens.EditPopup import Edit, validate, DEFAULT_IMAGE
from kivymd.uix.button import MDFlatButton

from kivymd.uix.dialog import MDDialog

from Database.database import Brick, Manual, Set
from kivymd.app import MDApp


class CreatePopup(MDDialog):
    def __init__(self):
        super(CreatePopup, self).__init__(
            type="custom",
            content_cls=Edit(),
            title='Edit item',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Save changes', on_release=self.create_dialog),
                MDFlatButton(text='Cancel', on_release=self.cancel_dialog)
            ]
        )

    def cancel_dialog(self, *args):
        self.dismiss()

    def create_dialog(self, *args):
        app = MDApp.get_running_app()

        if isinstance(app.current_type, Brick):
            brick = Brick()
            last_id = app.db.read_last_id(Brick)
            brick.id = validate(self.content_cls.ids.edit_id.text, last_id + 1)
            brick.name = validate(self.content_cls.ids.edit_name.text, 'sample text')
            brick.color = validate(self.content_cls.ids.edit_color.text, '#')
            brick.type = validate(self.content_cls.ids.edit_type.text, 'standard', 'Type')
            brick.image = validate(self.content_cls.image, DEFAULT_IMAGE)
            print("Brick.img: ",brick.image)
            app.db.create(brick)

        elif isinstance(app.current_type, Manual):
            manual = Manual()
            last_id = app.db.read_last_id(Manual)
            manual.id = validate(self.content_cls.ids.edit_id.text, last_id + 1)
            manual.name = validate(self.content_cls.ids.edit_name.text, 'sample text')
            manual.number_of_pages = validate(self.content_cls.widgets['number_of_pages'].text, 0)
            manual.image = validate(self.content_cls.image, DEFAULT_IMAGE)
            app.db.create(manual)

        elif isinstance(app.current_type, Set):
            set = Set()
            last_id = app.db.read_last_id(Set)
            set.id = validate(self.content_cls.ids.edit_id.text, last_id + 1)
            set.name = validate(self.content_cls.ids.edit_name.text, 'sample text')
            set.year = validate(self.content_cls.widgets['year'].text, 0)
            set.number_of_pieces = validate(self.content_cls.widgets['number_of_pieces'].text, 0)
            set.price = validate(self.content_cls.widgets['price'].text, 0)
            set.image = validate(self.content_cls.image, DEFAULT_IMAGE)
            app.db.create(set)

        app.redraw_screen_with_item(app.current_type)
        self.dismiss()
