from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from SerialAdapter import SerialAdapter
from DataRouter import DataRouter
from FileAdapter import FileAdapter
from CustomGraph import CustomGraph
from Settings import Settings

from kivy.config import Config

from kivy.logger import Logger

import numpy as np


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
            dr.addListener(self.children[0].addPoints)



class ScreenCalibrate(Screen):
    loaded = False

    def addPointOne(self, instance):
        settings.set("calibration","user_point1", self.text_input_1.text)
        settings.config.set("calibration","sensor_point1", np.mean(previousDataPoints))
        settings.saveConfig()

    def addPointTwo(self, instance):
        settings.set("calibration","user_point2", self.text_input_2.text)
        settings.config.set("calibration","sensor_point2", np.mean(previousDataPoints))
        settings.saveConfig()

    def setCalibration(self, instance):
        setCalibration()

    def onEnter(self):
        if not self.loaded:
            self.loaded = True
            self.add_button_1 = Button(text='Add point')
            self.text_input_1 = TextInput(text=settings.get("calibration","user_point1"))
            self.add_button_1.bind(on_press=self.addPointOne)
            self.add_button_2 = Button(text='Add point')
            self.text_input_2 = TextInput(text=settings.get("calibration","user_point2"))
            self.add_button_2.bind(on_press=self.addPointTwo)
            self.set_calibration_button = Button(text='Set Calibration')
            self.set_calibration_button.bind(on_press=self.setCalibration)


            layout = GridLayout(cols = 3, row_force_default=True, row_default_height=40)
            layout.add_widget(Label(text='Point One'))
            layout.add_widget(self.text_input_1)
            layout.add_widget(self.add_button_1)
            layout.add_widget(Label(text='Point Two'))
            layout.add_widget(self.text_input_2)
            layout.add_widget(self.add_button_2)
            layout.add_widget(self.set_calibration_button)

            self.add_widget(layout)


class ScreenSettings(Screen):
    loaded = False
    def onEnter(self):
        if not self.loaded:
            self.loaded = True
            self.add_widget(settings.getWidget())

        settings.updateAvailablePorts()

def update(self, **kwargs):
    global data
    data = np.array(sa.getAll())
    global previousDataPoints
    previousDataPoints.extend(data)
    previousDataPoints = previousDataPoints[1 - maxPoints:]
    bar = m*data + b
    dr.recieve(bar)

def setCalibration():
    global m, b

    y = np.array([float(settings.get("calibration","user_point1")), float(settings.get("calibration","user_point2"))])
    x = np.array([float(settings.get("calibration","sensor_point1")), float(settings.get("calibration","sensor_point2"))])

    A = np.vstack([x, np.ones(len(x))]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]

    print("Calibration set", "m =", str(m), "b =", str(b))


class Manager(ScreenManager):
    screen_visualize = ObjectProperty(None)
    screen_settings = ObjectProperty(None)
    screen_calibrate = ObjectProperty(None)

    def setScreen(self, newScreen):
        self.current = newScreen


class PressureVisualizer(App):
    def build(self):
        global sa
        sa = SerialAdapter(settings)
        sa.open()

        global dr
        dr = DataRouter()

        global fa
        fa = FileAdapter(settings)
        dr.addListener(fa.addPoints)

        Clock.schedule_interval(update, 1.0/60)

        self.icon = "assets/eit5.ico"

        return RootContainer()


def main():
    global settings
    global previousDataPoints
    global maxPoints
    maxPoints = 10

    previousDataPoints = [0]*maxPoints

    settings = Settings()
    settings.load('config.ini')
    setCalibration()

    PressureVisualizer().run()


if __name__ == '__main__':
    main()