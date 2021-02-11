import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle


class Person:
    def __init__(self, name, age, country):
        self.name = name
        self.age = age
        self.country = country
        self.image = ""
        self.info = ""

    def __str__(self):
        return f'My name is {self.name} I am {self.age}. I am  from {self.country}.'


class Widgets(Widget):
    def __init__(self, **kwargs):
        super(Widgets, self).__init__(**kwargs)

        with self.canvas:
            self.rect = Rectangle(pos=(2000, 1100), size=(75, 75))

    def on_touch_move(self, touch):
        self.rect.pos = touch.pos
        print(self.rect.pos)

    def on_touch_up(self, touch):
        self.rect.pos = (2000, 1100)


class Facewall(App):
    def build(self):
        return Widgets()


if __name__ == "__main__":
    Facewall().run()