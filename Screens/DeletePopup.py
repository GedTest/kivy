from Screens.EditPopup import Edit
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
            brick.name = self.validate(self.content_cls.ids.edit_name.text, 'sample text')
            brick.color = self.validate(self.content_cls.ids.edit_color.text, '#')
            brick.type = self.validate(self.content_cls.ids.edit_type.text, 'standard')
            brick.image = 'Brick/4568385Animal_Body_Part_Claw_Tooth_Horn_Small_-_Black.jpg'
            app.db.create(brick)

        elif isinstance(app.current_type, Manual):
            manual = Manual()
            manual.name = self.validate(self.content_cls.ids.edit_name.text, 'sample text')
            manual.number_of_pages = self.validate(self.content_cls.widgets['number_of_pages'].text, 0)
            manual.image = 'Manual/Fierce-flyer-manual.jpg'
            app.db.create(manual)

        elif isinstance(app.current_type, Set):
            set = Set()
            set.name = self.validate(self.content_cls.ids.edit_name.text, 'sample text')
            set.year = self.validate(self.content_cls.widgets['year'].text, 0)
            set.number_of_pieces = self.validate(self.content_cls.widgets['number_of_pieces'].text, 0)
            set.price = self.validate(self.content_cls.widgets['price'].text, 0)
            set.image = 'Set/31004Fierce-flyer.jpg'
            app.db.create(set)

        self.dismiss()

    def validate(self, str, default_value):
        return str if (str != '') else default_value
