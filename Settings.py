from kivy.config import ConfigParser
from kivy.uix.settings import SettingsWithNoMenu, SettingTitle, Label
from SerialAdapter import SerialAdapter

class Settings:

    __defaults = {
        'data': {
            'dir': 'data/', 
            'ppr': 20
        },
        'com': {
            'port': 'COM1', 
            'baudrate': 9600,
            'bytesize': '8',
            'parity': 'None',
            'stopbits': '1'
        } 
    }

    def __init__(self):
        self.config = ConfigParser()
        self.widget = SettingsWithNoMenu()


    def load(self, filename):
        self.config.read(filename)
        for k, v in self.__defaults.items():
            self.config.setdefaults(k, v)

        self.panel = self.widget.create_json_panel('Settings', self.config, data=self.windgetconfigdata)
        self.widget.children[0].add_widget(self.panel)

        self.setPanelOptions('port', SerialAdapter.getPortNames())
        self.setPanelOptions('bytesize', SerialAdapter.BYTESIZE.keys())
        self.setPanelOptions('parity', SerialAdapter.PARITY.keys())
        self.setPanelOptions('stopbits', SerialAdapter.STOPBITS.keys())


    def updateAvailablePorts(self):
        self.setPanelOptions('port', SerialAdapter.getPortNames())
    
            
    def getPanelSetting(self, key):
        return next((x for x in self.panel.children if not isinstance(x, SettingTitle) and not isinstance(x, Label) and x.key == key), None)

    def setPanelOptions(self, key, options):
        s = self.getPanelSetting(key)
        if s != None:
            s.options = options


    def getWidget(self):
        return self.widget


    def addCallback(self, callback, section = None, key = None):
        self.config.add_callback(callback, section, key)
        if key != None:
            callback(section, key, self.get(section, key))


    def get(self, section, key):
        return self.config.get(section, key)


    def set(self, section, key, value):
        return self.config.set(section, key, value)


    def getDefault(self, section, key):
        return self.__defaults[section][key]


    windgetconfigdata = """[
  {
    "type": "title",
    "title": "Data"
  },
  {
    "type": "path",
    "title": "Data export directory",
    "desc": "The directory data files are writen to",
    "key": "dir",
    "section": "data"
  },
  {
    "type": "numeric",
    "title": "Points per row",
    "desc": "The numnber of data points per row in the data file",
    "key": "ppr",
    "section": "data"
  },
  {
    "type": "title",
    "title": "COM"
  },
  {
    "type": "options",
    "title": "COM port",
    "desc": "The com port of the device",
    "key": "port",
    "section": "com",
    "options": ["COM1"]
  },
  {
    "type": "numeric",
    "title": "Baudrate",
    "desc": "Symbols per second",
    "key": "baudrate",
    "section": "com"
  },
  {
    "type": "options",
    "title": "Byte size",
    "desc": "Number of data bits",
    "key": "bytesize",
    "section": "com",
    "options": []
  },
  {
    "type": "options",
    "title": "Stop bits",
    "desc": "Number of stop bits",
    "key": "stopbits",
    "section": "com",
    "options": []
  },
  {
    "type": "options",
    "title": "Parity",
    "desc": "Enable parity checking",
    "key": "parity",
    "section": "com",
    "options": []
  }
]""" 