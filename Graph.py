from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
import kivy_garden.graph as kg

class Graph(Widget):
    points = []
    maxPoints = 10
    def __init__(self, dataSource, **kwargs):
        super(Graph, self).__init__(**kwargs)
        self.dataSource = dataSource
        self.graph = kg.Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
              x_ticks_major=25, y_ticks_major=1,
              y_grid_label=True, x_grid_label=True, padding=5,
              x_grid=True, y_grid=True, xmin=-0, xmax=self.maxPoints, ymin=-0, ymax=1024 )
        self.plot = kg.MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.add_widget(self.graph)

    def update_points(self, *args):
        data = self.dataSource.getAll()
        if len(data) > 0:
             self.points.extend(data)
             print(self.points)
             if len(self.points) >= self.maxPoints:
                 self.points = self.points[1-self.maxPoints:]
             self.plot.points = [(x, self.points[x]) for x in range(0, len(self.points))]

    def update_axis(self, *args):
        self.graph.xmax = self.maxPoints
        if len(self.points) > 0:
            self.graph.ymax = max(self.points)

    def update(self, dt):
        self.update_points(dt)
        self.update_axis(dt)
        pass