#!/usr/bin/env python3
import time
import Adafruit_BBIO.GPIO as GPIO

ON ="GP0_6"  # GP0 for buttons
OFF ="GP0_5"

# Set the GPIO pins:
GPIO.setup(ON,    GPIO.OUT)
GPIO.setup(OFF,    GPIO.OUT)

GPIO.output(ON, 0)
GPIO.output(OFF, 0)

print("Clicking on button")
GPIO.output(ON,1)
time.sleep(1)
GPIO.output(ON,0)

print("Clicking off button")
GPIO.output(OFF,1)
time.sleep(1)
GPIO.output(OFF,0)

