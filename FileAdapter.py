import csv
import datetime
import os

class FileAdapter(object):
    points = []
    pointsPerRow = 20
    path = "data/"

    def __init__(self):
        now = datetime.datetime.now()
        self.setPath(self.path)
        self.fileName = self.path + now.strftime("%Y-%m-%d-%H-%M-%S") + '.csv'


    def setPath(self, newPath):
        self.path = newPath
        if not os.path.exists(newPath):
            os.makedirs(newPath)


    def addPoints(self, data):
        if len(data) > 0:
            self.points.extend(data)
            if len(self.points) >= self.pointsPerRow:
                self.write()


    def write(self):
        rows = []
        n = len(self.points)
        step = self.pointsPerRow;
        mod = n % step
        for i in range(0, n - mod, step):  
            rows.append(self.points[i:i + step])
        self.points = self.points[-mod:]

        with open(self.fileName, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(rows)
