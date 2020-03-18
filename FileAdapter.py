import csv
import datetime
import os
from Settings import Settings
from kivy.logger import Logger

class FileAdapter(object):
    points = []
    dir = ''
    pointsPerRow = 1

    def __init__(self, settings : Settings):
        self.settings = settings
        settings.addCallback(self.onDirChanged, 'data', 'dir')
        settings.addCallback(self.onPPRChanged, 'data', 'ppr')


    def onDirChanged(self, section, key, value):
        if value == None or value == '':
            value = self.settings.getDefault(section, key)
            self.settings.config.set(section, key, value)
        if not os.path.isdir(value):
            value = os.path.dirname(value)
            self.settings.config.set(section, key, value)

        if not os.path.exists(value):
            os.makedirs(value)

        if self.dir != value:
            Logger.debug('FileAdapter: Dir changed: %s', value)
            self.dir = value
            self.setFilename()


    def onPPRChanged(self, section, key, value):
        value = int(value)
        if value < 1:
            value = 1
            self.settings.config.set(section, key, value)

        if self.pointsPerRow != value:
            Logger.debug('FileAdapter: PPR changed: %d', value)
            self.pointsPerRow = value
            self.setFilename()


    def setFilename(self):
        now = datetime.datetime.now()
        self.fileName = os.path.join(self.dir, now.strftime("%Y-%m-%d-%H-%M-%S")) + '.csv'
        Logger.debug('FileAdapter: Setting file: %s', self.fileName)

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
