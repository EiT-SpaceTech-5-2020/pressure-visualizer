from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from SerialAdapter import SerialAdapter
from DataRouter import DataRouter
from FileAdapter import FileAdapter
from CustomGraph import CustomGraph

global sa
global dr
global fa

class RootContainer(BoxLayout):
    manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(RootContainer, self).__init__(**kwargs)
        self.manager.screen_visualize.onEnter()


class ScreenVisualize(Screen):
    loaded = False
    def onEnter(self):
        if not self.loaded:
            self.loaded = True
            global dr
            dr.addListener(self.children[0].addPoints)


class ScreenExport(Screen):
    pass


class ScreenCalibrate(Screen):
    pass


def update(self, **kwargs):
    global sa
    global dr
    data = sa.getAll();
    if len(data) > 0:
        dr.recieve(data)


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

        global dr
        dr = DataRouter()

        global fa
        fa = FileAdapter()
        dr.addListener(fa.addPoints)

        Clock.schedule_interval(update, 1.0 / 60.0)

        return RootContainer()


    def visualize(self):
        print("WOOO")


def main():
    PressureVisualizer().run()


if __name__ == '__main__':
    main()