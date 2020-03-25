from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
import kivy_garden.graph as kg
import math

class CustomGraph(kg.Graph):
    points = [0]
    maxPoints = 10
    fps = 60

    def __init__(self, **kwargs):
        super(CustomGraph, self).__init__(**kwargs)
        self.xlabel = 'Seconds'
        self.ylabel = 'Bar'
        self.x_ticks_minor= int(self.maxPoints/2)
        self.x_ticks_major= int(self.maxPoints/10)
        self.y_ticks_major=100
        self.y_grid_label=True
        self.x_grid_label=True
        self.padding=5
        self.x_grid=True
        self.y_grid=True
        self.xmin=0
        self.xmax=self.maxPoints
        self.ymin=-100
        self.ymax=1000

        self.plot = kg.MeshLinePlot(color=[1, 0, 0, 1])
        self.add_plot(self.plot)


    def setDataSource(self, dataSource):
        self.dataSource = dataSource


    def updatePoints(self, data):
        if len(data) > 0:
            self.points.append(data[-1])
        else:
            self.points.append(self.points[-1])
        
        if len(self.points) >= self.maxPoints*self.fps:
            self.points = self.points[1-self.maxPoints*self.fps:]
            self.updateXticks(2)
        
        self.plot.points = [(x/self.fps, self.points[x]) for x in range(0, len(self.points))]
            

    def updateXticks(self, seconds):
        self.xmin += seconds
        self.maxPoints += seconds
        self.xmax = self.maxPoints

    
    def updateAxis(self, *args):
        self.xmax = self.maxPoints
        if len(self.points) > 0:
            self.ymax = max(self.points)


    def addPoints(self, data):
        self.updatePoints(data)
        #self.updateAxis(dt)