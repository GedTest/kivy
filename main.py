from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.card import MDCard

from database import Database, Brick


class Card(MDCard):
    text = StringProperty()
    img = StringProperty()


class MainApp(MDApp):
    db = Database(dbtype='sqlite', dbname='LEGO.db')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("main.kv")

    def build(self):
        return self.screen

    def on_start(self):
        '''Creates a list of cards.'''

        app = App.get_running_app()
        app.db.update()

        db_items = app.db.read(Brick, Brick.name)

        for item in db_items:
            self.screen.ids.md_list.add_widget(
                Card(text='F F', img='img/'+item.image)
            )


if __name__ == '__main__':
    MainApp().run()
