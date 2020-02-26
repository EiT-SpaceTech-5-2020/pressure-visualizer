from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

class MainWindow(Widget):
 
   def update(self, dt):
       pass

class PressureVisualizer(App):
    def build(self):
        mainWindow = MainWindow()
        #Clock.schedule_interval(mainWindow.update, 1.0 / 60.0)
        return mainWindow


if __name__ == '__main__':
    PressureVisualizer().run()