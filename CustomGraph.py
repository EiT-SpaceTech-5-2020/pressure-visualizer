from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
import kivy_garden.graph as kg
import math

class CustomGraph(kg.Graph):
    points = []
    maxPoints = 100

    def __init__(self, **kwargs):
        super(CustomGraph, self).__init__(**kwargs)
        self.xlabel = 'Time'
        self.ylabel = 'Value'
        self.x_ticks_minor=5
        self.x_ticks_major=25
        self.y_ticks_major=128
        self.y_grid_label=True
        self.x_grid_label=True
        self.padding=5
        self.x_grid=True
        self.y_grid=True
        self.xmin=-0
        self.xmax=self.maxPoints
        self.ymin=-0
        self.ymax=1024

        self.plot = kg.MeshLinePlot(color=[1, 0, 0, 1])
        self.add_plot(self.plot)

    def setDataSource(self, dataSource):
        self.dataSource = dataSource

    def update_points(self, *args):
        data = self.dataSource.getAll()
        if len(data) > 0:
             self.points.extend(data)
             print(self.points)
             if len(self.points) >= self.maxPoints:
                 self.points = self.points[1-self.maxPoints:]
             self.plot.points = [(x, self.points[x]) for x in range(0, len(self.points))]

    def update_axis(self, *args):
        self.xmax = self.maxPoints
        if len(self.points) > 0:
            self.ymax = max(self.points)

    def update(self, dt):
        self.update_points(dt)
        self.update_axis(dt)
        pass