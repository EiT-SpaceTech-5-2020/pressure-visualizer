import os
import time
import math
import random
import numpy as np
from serial import *
from threading import Thread

targetValue = 0
delta = 1
interval = 0.01

ser = Serial(
    port='COM2',
    baudrate=9600,
    bytesize=EIGHTBITS,
    parity=PARITY_NONE,
    stopbits=STOPBITS_ONE,
    timeout=0.1,
    xonxoff=0,
    rtscts=0,
    interCharTimeout=None
)

def threadFunc():
    value = 0
    while True:
        if np.abs(targetValue-value) < delta:
            value = targetValue
        else:
            value += np.sign(targetValue-value) * delta

        #print(value)
        ser.write(int(value).to_bytes(2, byteorder="little", signed=False))
        time.sleep(interval)

def main():
    thread = Thread(target=threadFunc, args=())
    thread.start()

    while True:
        x = input();
        if x.isdigit() and int(x) > 0:
            targetValue = int(x)

if __name__ == '__main__':
    main()