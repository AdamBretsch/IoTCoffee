#!/usr/bin/env python3
import time
import Adafruit_BBIO.GPIO as GPIO
import rcpy.motor as motor

pump = motor.motor3
WET ="P9_23"  # GP0 for buttons

# Set the GPIO pins:
GPIO.setup(WET, GPIO.IN)


print("looking for water")
while True:
  if GPIO.input(WET):
	  print("it is wet here, stopping pump")
	  pump.set(0)
  else:
	  print("dry as a bone, pumping")
	  pump.set(1)

  time.sleep(0.5)

