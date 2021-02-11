import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="First name:"))
        self.first_name = TextInput(multiline=False)
        self.inside.add_widget(self.first_name)

        self.inside.add_widget(Label(text="Last name:"))
        self.last_name = TextInput(multiline=False)
        self.inside.add_widget(self.last_name)

        self.inside.add_widget(Label(text="Email:"))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.add_widget(self.inside)
        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        name = self.first_name.text
        last = self.last_name.text
        email = self.email.text

        print(f'name: {name} last name: {last} email: {email}')
        self.first_name.text = ""
        self.last_name.text = ""
        self.email.text = ""


class MyApp(App):
    def build(self):
        return Grid()


if __name__ == "__main__":
    MyApp().run()
