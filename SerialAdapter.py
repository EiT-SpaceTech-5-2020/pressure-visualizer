import time
from threading import Thread
from serial import *
import serial.tools.list_ports
from kivy.logger import Logger

class SerialAdapter:
    __stopReading = False
    __thread = None
    
    def __init__(self, settings):
        Logger.info('Serial: Initializing')
        self.settings = settings

        self.values = []
        self.ser = Serial(
            baudrate=int(settings.get('com','baudrate')), 
            bytesize=SerialAdapter.BYTESIZE[settings.get('com','bytesize')], 
            parity=SerialAdapter.PARITY[settings.get('com','parity')], 
            stopbits=SerialAdapter.STOPBITS[settings.get('com','stopbits')],
            timeout=0.1,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )
        self.ser.setPort(settings.get('com','port'))

        settings.addCallback(self.onValueChanged, 'com')


    def open(self):
        try:
            if not self.ser.isOpen() or self.__thread == None:
                Logger.info('Serial: Attempting to open port: %s', self.ser.port)
                if not self.ser.isOpen():
                    self.ser.open()
                if self.__thread == None:
                    self.startReading()

        except SerialException as e:
            Logger.error('Serial: Failed to open port: %s', self.ser.port)
            Logger.error('Serial: %s', e.args[0])
            self.close()
            self.stopReading()


    def onValueChanged(self, section, key, value):
        if self.ser.isOpen():
            self.close()
            
        if key == 'port':
            self.ser.setPort(value)
        elif key == 'baudrate':
            self.ser.baudrate = value
        elif key == 'bytesize':
            self.ser.bytesize = SerialAdapter.BYTESIZE[value]
        elif key == 'parity':
            self.ser.parity = SerialAdapter.PARITY[value]
        elif key == 'stopbits':
            self.ser.stopbits = SerialAdapter.STOPBITS[value]

        self.open()


    def close(self):
        Logger.info('Serial: Closing port: %s', self.ser.port)
        self.stopReading()
        if self.ser.isOpen():
            self.ser.close()


    def isOpen(self):
        return self.ser.isOpen()


    def startReading(self):
        if self.ser.isOpen():
            Logger.debug('Serial: Start reading')
            self.__thread = Thread(target=self.receiving, args=())
            self.__thread.start()


    def stopReading(self):
        if self.__thread != None:
            Logger.debug('Serial: Stop reading')
            self.__stopReading = True
            self.__thread.join()
            self.__thread = None
            self.__stopReading = False


    def receiving(self):
        self.ser.flushInput()
        while not self.__stopReading:
            rcv = self.ser.readline()
            rcv = rcv.decode("utf-8")
            rcv = rcv.replace('\r', '').replace('\n', '')
            if rcv != "":
                self.values.append(int(rcv))

    def getAll(self):
        temp = self.values.copy()
        self.values.clear()
        return temp


    def write(self, data):
        Logger.trace('Serial: Writing: %d', data)
        self.ser.write(data)


    def getPorts():
        return list(serial.tools.list_ports.comports())


    def getPortNames():
        return [p.device for p in SerialAdapter.getPorts()]


    PARITY = {
        'None': PARITY_NONE,
        'Even': PARITY_EVEN,
        'Odd': PARITY_ODD,
        'Mark': PARITY_MARK,
        'Space': PARITY_SPACE
    }

    STOPBITS = {
        '1': STOPBITS_ONE,
        '1.5': STOPBITS_ONE_POINT_FIVE,
        '2': STOPBITS_TWO
    }

    BYTESIZE = {
        '5': FIVEBITS,
        '6': SIXBITS,
        '7': SEVENBITS,
        '8': EIGHTBITS
    }