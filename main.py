import os

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.app import MDApp

from Screens.Screens import Screens
from Database.database import Database, Brick, Manual, Set


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super(ContentNavigationDrawer, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def set_database_objects(self, cls_name):
        if cls_name == "Brick":
            self.app.database_objects = self.app.db.read(Brick, Brick.name)
        elif cls_name == "Manual":
            self.app.database_objects = self.app.db.read(Manual, Manual.name)
        else:
            self.app.database_objects = self.app.db.read(Set, Set.name)


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class MainApp(MDApp):
    db = Database(dbtype='sqlite', dbname='LEGO.db')
    database_objects = db.read(Brick, Brick.name)
    root_path = os.path.dirname(os.path.realpath(__file__))

    def build(self):
        return


MainApp().run()
