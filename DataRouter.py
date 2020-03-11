class DataRouter(object):

    def __init__(self):
        self.listeners = []


    def addListener(self, f):
        self.listeners.append(f)


    def recieve(self, data):
        for l in self.listeners:
            l(data)

