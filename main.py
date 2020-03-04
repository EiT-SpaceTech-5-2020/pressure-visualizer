from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class Menu(BoxLayout):
    manager = ObjectProperty(None)


class ScreenVisualize(Screen):
    pass


class ScreenExport(Screen):
    pass


class ScreenCalibrate(Screen):
    pass


class Manager(ScreenManager):
    screen_visualize = ObjectProperty(None)
    screen_export = ObjectProperty(None)
    screen_calibrate = ObjectProperty(None)


class PressureVisualizer(App):
    def build(self):
        return Menu()
    def visualize(self):
        print("WOOO")


if __name__ == '__main__':
    PressureVisualizer().run()