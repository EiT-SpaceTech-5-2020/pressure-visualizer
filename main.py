from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from SerialAdapter import SerialAdapter
from CustomGraph import CustomGraph

global sa

class Menu(BoxLayout):
    manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.manager.screen_visualize.onEnter()

class ScreenVisualize(Screen):
    loaded = False
    def onEnter(self):
        if not self.loaded:
            self.loaded = True
            global sa
            self.children[0].setDataSource(sa)
            Clock.schedule_interval(self.children[0].update, 1.0 / 60.0)


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
        global sa
        sa = SerialAdapter()
        sa.open('COM1')
        sa.startReading()
        return Menu()
    def visualize(self):
        print("WOOO")

if __name__ == '__main__':
    PressureVisualizer().run()