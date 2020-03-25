from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from SerialAdapter import SerialAdapter
from DataRouter import DataRouter
from FileAdapter import FileAdapter
from CustomGraph import CustomGraph
from Settings import Settings

from kivy.logger import Logger

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

class ScreenCalibrate(Screen):
    pass


class ScreenSettings(Screen):
    loaded = False
    def onEnter(self):
        global settings
        global sa
        if not self.loaded:
            self.loaded = True
            self.add_widget(settings.getWidget())

        settings.updateAvailablePorts()


def update(self, **kwargs):
    global sa
    global dr
    data = sa.getAll()
    dr.recieve(data)


class Manager(ScreenManager):
    screen_visualize = ObjectProperty(None)
    screen_calibrate = ObjectProperty(None)
    screen_settings = ObjectProperty(None)

    def setScreen(self, newScreen):
        self.current = newScreen


class PressureVisualizer(App):
    def build(self):
        global settings
        global sa
        sa = SerialAdapter(settings)
        sa.open()

        global dr
        dr = DataRouter()

        global fa
        fa = FileAdapter(settings)
        dr.addListener(fa.addPoints)

        Clock.schedule_interval(update, 1.0/60)

        return RootContainer()


def main():
    global settings
    settings = Settings()
    settings.load('config.ini')

    PressureVisualizer().run()


if __name__ == '__main__':
    main()