from serial import *
import serial.tools.list_ports
from threading import Thread
import time

class SerialAdapter:
    __stopReading = False
    thread = None
    
    def __init__(self, settings):
        self.settings = settings

        self.values = []
        self.ser = Serial(
            port=settings.get('com','port'),
            baudrate=int(settings.get('com','baudrate')), 
            bytesize=SerialAdapter.BYTESIZE[settings.get('com','bytesize')], 
            parity=SerialAdapter.PARITY[settings.get('com','parity')], 
            stopbits=SerialAdapter.STOPBITS[settings.get('com','stopbits')],
            timeout=0.1,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )

        settings.addCallback(self.onValueChanged, 'com')


    def open(self):
        if not self.ser.isOpen():
            self.ser.open()
        if self.thread == None:
            self.startReading()

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
        self.stopReading()
        if self.ser.isOpen():
            self.ser.close()


    def isOpen(self):
        return self.ser.isOpen()


    def startReading(self):
        if self.ser.isOpen():
            self.thread = Thread(target=self.receiving, args=())
            self.thread.start()


    def stopReading(self):
        if self.thread != None:
            self.__stopReading = True
            self.thread.join()
            self.thread = None
            self.__stopReading = False


    def receiving(self):
        buffer = [] 
        self.ser.flushInput()
        while not self.__stopReading:
            # Read available data
            buffer += self.ser.read(self.ser.inWaiting())
            #if len(buffer) > 0:
                #print('[SerialAdapter] Buffer: ', buffer)

            if len(buffer) >= 2:
                value = buffer[:2]
                buffer = buffer[2:]
                value = int.from_bytes(value, byteorder='little', signed=False);
                self.values.append(value)
                #print('[SerialAdapter] Value: ', value)


    def getAll(self):
        temp = self.values.copy()
        self.values.clear()
        return temp


    def write(self, data):
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