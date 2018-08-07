#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from random import randint

LedPin = 11    # pin11

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led



def loop():

	
	while True:
		GPIO.output(LedPin, GPIO.LOW)  # led on
		time.sleep(1)
		cycle_wait = randint(5,15)
		timeout = time.time() + cycle_wait
			while True:
				print('standby for' + cycle_wait + 'seconds')
				GPIO.output(LedPin, GPIO.LOW)  # led on
				time.sleep(0.75)
				GPIO.output(LedPin, GPIO.HIGH) # led off
				time.sleep(0.25)
				if time.time() > timeout:
					break

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
