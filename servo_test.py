#!/usr/bin/env python3
import time
import rcpy.servo as servo

servo1 = servo.servo1
UP = 0.7
DOWN = -0.9

servo.enable()
clk= servo1.start(0.02)
print("Moving it down")
servo1.pulse(DOWN)
time.sleep(2)
servo1.pulse(UP)
print("Moving it up")
time.sleep(2)

