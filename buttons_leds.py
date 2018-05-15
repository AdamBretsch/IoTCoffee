#!/usr/bin/env python3
import time
import Adafruit_BBIO.GPIO as GPIO

button1="GP0_3"  # GP0 for buttons


LED1   ="GREEN" #GP1 for leds

# Set the GPIO pins:
GPIO.setup(LED1,    GPIO.OUT)
GPIO.setup(button1, GPIO.IN)

# Turn on LEDs to default state
GPIO.output(LED1, 0)


def updateLED(channel):
    print("wet detected")
    state = GPIO.input(channel)
    GPIO.output(LED1, state)

print("Running...")

GPIO.add_event_detect(button1, GPIO.BOTH, callback=updateLED) # RISING, FALLING or BOTH

try:
  while True:
    time.sleep(100)

except KeyboardInterrupt:
    print("Cleaning Up")
    GPIO.cleanup()
GPIO.cleanup()
