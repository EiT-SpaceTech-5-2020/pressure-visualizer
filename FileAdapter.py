import csv
import datetime
import os
from Settings import Settings
from kivy.logger import Logger

class FileAdapter(object):
    points = []
    dir = ''
    pointsPerRow = 1
    __nodataCounter = 0
    __nodata = False

    def __init__(self, settings : Settings):
        self.__nodataCounter = 0;
        self.__nodata = False
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
            if self.__nodata:
                self.__nodata = False
                self.__nodataCounter = 0
                self.setFilename()
            self.points.append(data[-1])
        else:
            if len(self.points) > 0:
                self.points.append(self.points[-1])
            else:
                self.points.append(0)
            self.__nodataCounter += 1

        if self.__nodataCounter >= self.pointsPerRow:
            self.__nodata = True
            self.points.clear()

        if len(self.points) >= self.pointsPerRow and not self.__nodata:
            self.__nodataCounter = 0
            self.write()
            

    def write(self):
        rows = []
        n = len(self.points)
        step = self.pointsPerRow
        mod = n % step
        for i in range(0, n - mod, step):  
            rows.append(self.points[i:i + step])

        if mod == 0:
            self.points.clear()
        else:
            self.points = self.points[-mod:]

        with open(self.fileName, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(rows)
