from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy_garden.drag_n_drop import *

drag_controller = DraggableController()


class DraggableBoxLayout(DraggableLayoutBehavior, BoxLayout):

    def compare_pos_to_widget(self, widget, pos):
        if self.orientation == 'vertical':
            return 'before' if pos[1] >= widget.center_y else 'after'
        return 'before' if pos[0] < widget.center_x else 'after'

    def handle_drag_release(self, index, drag_widget):
        self.add_widget(drag_widget, index)


class DragLabel(DraggableObjectBehavior, Label):

    def __init__(self, **kwargs):
        super(DragLabel, self).__init__(
            **kwargs, drag_controller=drag_controller)

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        self.parent.remove_widget(self)

    def show_info(self):
        label = self.children[1]
        btn_initials = label.source.split("/")[1].split(".")[0]

        n_u = Widgets().persons[btn_initials]

        popup_instance = PersonWindow()

        popup_instance.user_name = str("Name: " + n_u.name)
        popup_instance.user_age = str("Age: " + str(n_u.age))
        popup_instance.user_country = str("Country: " + n_u.country)
        popup_instance.user_image = str("user_images/"+btn_initials+".png")
        popup_instance.user_info = str("Info: " + n_u.info)

        new_popup = Popup(title=n_u.name, content=popup_instance, size_hint=(None, None), size=(400, 400))
        new_popup.open()


class Person:

    def __init__(self, name, age, country, info=""):
        self.name = name
        self.age = age
        self.country = country
        parts = name.split(" ")
        self.initials = parts[0][0] + parts[1][0]
        self.info = info

    def __str__(self):
        return f'My name is {self.name} I am {self.age}. I am from {self.country}.'


class PersonWindow(FloatLayout):
    user_name = StringProperty()
    user_age = StringProperty()
    user_country = StringProperty()
    user_image = StringProperty()
    user_info = StringProperty()


class PersonWidget(DraggableBoxLayout):

    def __init__(self, init, **kwargs):
        self.initials = 'user_images/' + init + '.png'
        super(PersonWidget, self).__init__(**kwargs)

    def add_widget(self, widget, *args, **kwargs):
        widget.pos_hint = {'x': 0, 'y': 0}
        return super().add_widget(widget)


class Widgets(Widget):

    def __init__(self, **kwargs):
        super(Widgets, self).__init__(**kwargs)
        self.persons = {"AN": Person("Anna Nováková", 18, "Czech Republic"),
                        "VR": Person("Vanessa Ramirez", 20, "Spain"),
                        "WS": Person("William Smith", 45, "Great Britain"), "OZ": Person("Oliver Zambezi", 17, "India")}


class Facewall(App):
    drag_controller = drag_controller

    def build(self):
        return Widgets()

    def on_start(self):
        initials = Widgets().persons.keys()
        people = self.root.ids.people
        for init in initials:
            people.add_widget(PersonWidget(init))


if __name__ == "__main__":
    Facewall().run()
