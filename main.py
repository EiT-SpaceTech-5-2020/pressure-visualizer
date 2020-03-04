from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from SerialAdapter import SerialAdapter
from Graph import Graph

global sa

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
        sa = SerialAdapter()
        sa.open('COM1')
        sa.startReading()
        return Menu()
    def visualize(self):
        print("WOOO")

if __name__ == '__main__':
    PressureVisualizer().run()

#graph = Graph(sa)
#Clock.schedule_interval(graph.update, 1.0 / 60.0)
#self.add_widget(graph)