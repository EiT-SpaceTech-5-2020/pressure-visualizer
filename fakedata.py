import os
import time
import numpy as np

x = 0.0

while True:
    x += 0.3
    os.system("echo " + str(np.sin(x)) + " > COM2")
    time.sleep(0.01)