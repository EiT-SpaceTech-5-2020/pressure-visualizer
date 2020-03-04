import os
import time
import math
import numpy as np
from serial import *

x = 0.0

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

while True:
    x += 0.3
    value = int((np.sin(x) + 1) / 2 * np.power(2, 10))
    print(value)
    ser.write(value.to_bytes(2, byteorder="little", signed=False))
    #os.system("echo " + str(np.sin(x)) + " > COM2")
    time.sleep(1)