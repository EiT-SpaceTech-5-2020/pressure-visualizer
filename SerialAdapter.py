from serial import *
from threading import Thread
import time

class SerialAdapter:
    
    def __init__(self):
        self.values = []

    def open(self, port : str):
       self.ser = Serial(
            port=port,
            baudrate=9600,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE,
            timeout=0.1,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )

    def close(self):
        self.ser.close();

    def startReading(self):
        self.thread = Thread(target=self.receiving, args=())
        self.thread.start()

    def stopReading(self):
        self.thread.stop();

    def receiving(self):
        buffer = [] 
        self.ser.flushInput()
        while True:
            # Read available data
            buffer += self.ser.read(self.ser.inWaiting())
            if len(buffer) > 0:
                print('buffer: ', buffer)

            if len(buffer) >= 2:
                value = buffer[:2]
                buffer = buffer[2:]
                value = int.from_bytes(value, byteorder='little', signed=False);
                self.values.append(value)
                pass

    def getAll(self):
        temp = self.values.copy()
        self.values.clear()
        return temp

if __name__ ==  '__main__':
    
    sa = SerialAdapter()
    sa.open('COM1')
    sa.startReading()

    while(True):
        time.sleep(1)
        data = sa.getAll()
        if len(data) > 0:
            print('value: ', data)

