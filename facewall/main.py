from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

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
       # print(n_u)

        popup_instance = PersonWindow()

        popup_instance.user_name = str("Name: "+n_u.name)
        popup_instance.user_age = str("Age: "+str(n_u.age))
        popup_instance.user_country = str("Country: "+n_u.country)
        popup_instance.user_info = str("Info: " + n_u.info)

        new_popup = Popup(title=n_u.name, content=popup_instance, size_hint=(None, None), size=(400, 400))
        new_popup.open()


class Person:

    def __init__(self, name, age, country, info=""):
        self.name = name
        self.age = age
        self.country = country
        parts = name.split(" ")
        self.initials = parts[0][0]+parts[1][0]
        self.info = info

    def __str__(self):
        return f'My name is {self.name} I am {self.age}. I am from {self.country}.'


class PersonWindow(FloatLayout):
    user_name = StringProperty()
    user_age = StringProperty()
    user_country = StringProperty()
    user_info = StringProperty()


class PersonWidget(DraggableBoxLayout):
    def add_widget(self, widget, *args, **kwargs):
        widget.pos_hint = {'x': 0, 'y': 0}
        return super().add_widget(widget)
    

class Widgets(Widget):

    def __init__(self, **kwargs):
        super(Widgets, self).__init__(**kwargs)
        self.persons = {"AN": Person("Anna Nováková", 18, "Czech Republic"), "VR": Person("Vanessa Ramirez", 20, "Spain"),
                        "WS": Person("William Smith", 45, "Great Britain"), "OZ": Person("Oliver Zambezi", 17, "India")}


kv = '''
GridLayout:
    size: root.width, root.height
    cols: 2

    GridLayout:
        col_default_width: root.width * 0.75
        col_force_default: True

        rows: 6
        Button:
            text: "My friends"
            size_hint: 1.0, 0.4

        DraggableBoxLayout:
            drag_classes: ['person']
            orientation: 'vertical'
            canvas:
                Color:
                    rgba: (1, 1, 1, .2) if app.drag_controller.dragging and app.drag_controller.widget_dragged and app.drag_controller.widget_dragged.drag_cls == 'person' else (0, 0, 0, 0)
                Rectangle:
                    pos: self.pos
                    size: self.size
                    
            GridLayout:
                cols: 4
                Image:
                    source: 'user_images/VR.png'
                    size: (root.width/8, root.height/8)
                Label:
                    text: "Name: Vanessa Ramirez"
                Label:
                    text: "Age: 20"
                Label:
                    text: "Info: Lorem ipsum..."

    GridLayout:
        col_default_width: root.width * 0.25
        col_force_default: True
        size_hint: (0.33, 1)
        rows: 2

        Button:
            text: "People"
            size_hint: 1.0, 0.1

        GridLayout:
            row_default_height: root.height * 0.15
            row_force_default: True
            cols: 2
            id: people
            
            DraggableBoxLayout:
                drag_classes: ['person']
                orientation: 'vertical'
                DragLabel:
                    drag_cls: 'person'
                    Image:
                        source: 'user_images/AN.png'
                        size: (root.width/8, root.height/8)
                    Button:
                        size: (self.parent.size[0]/3, self.parent.size[1]/3)
                        pos: (self.parent.pos[0], self.parent.pos[1])
                        text: "Info"
                        on_release: self.parent.show_info()
                        
            DraggableBoxLayout:
                drag_classes: ['person']
                orientation: 'vertical'
                DragLabel:
                    drag_cls: 'person'
                    Image:
                        source: 'user_images/OZ.png'
                        size: (root.width/8, root.height/8)
                    Button:
                        size: (self.parent.size[0]/3, self.parent.size[1]/3)
                        pos: (self.parent.pos[0], self.parent.pos[1])
                        text: "Info"
                        on_release: self.parent.show_info()
                        
            DraggableBoxLayout:
                drag_classes: ['person']
                orientation: 'vertical'
                DragLabel:
                    drag_cls: 'person'
                    Image:
                        source: 'user_images/VR.png'
                        size: (root.width/8, root.height/8)
                    Button:
                        size: (self.parent.size[0]/3, self.parent.size[1]/3)
                        pos: (self.parent.pos[0], self.parent.pos[1])
                        text: "Info"
                        on_release: self.parent.show_info()
                        
            DraggableBoxLayout:
                drag_classes: ['person']
                orientation: 'vertical'
                DragLabel:
                    drag_cls: 'person'
                    Image:
                        source: 'user_images/WS.png'
                        size: (root.width/8, root.height/8)
                    Button:
                        size: (self.parent.size[0]/3, self.parent.size[1]/3)
                        pos: (self.parent.pos[0], self.parent.pos[1])
                        text: "Info"
                        on_release: self.parent.show_info()
'''


class Facewall(App):
    drag_controller = drag_controller

    def build(self):
        return Builder.load_string(kv)#Widgets()

    def on_start(self):
        people = self.root.ids.people
        for i in range(4):
            people.add_widget(PersonWidget())


if __name__ == "__main__":
    Facewall().run()
