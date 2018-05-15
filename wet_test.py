#!/usr/bin/env python3
import time
import Adafruit_BBIO.GPIO as GPIO

WET ="GP0_5"  # GP0 for buttons

# Set the GPIO pins:
GPIO.setup(WET, GPIO.IN)


print("looking for water")
while True:
  if GPIO.input(WET):
	  print("it is wet here")
  else:
  	  print("dry as a bone")

  time.sleep(1)

