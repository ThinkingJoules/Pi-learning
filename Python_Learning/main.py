#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import datetime
from datetime import date
import sqlite_lib


AO_pin = 0 #flame sensor AO connected to ADC chanannel 0
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

durStart = 0
durEnd = 0
node = 'manual-mill'

#port init
def init():
          GPIO.setwarnings(False)
          GPIO.setmode(GPIO.BCM)
          # set up the SPI interface pins
          GPIO.setup(SPIMOSI, GPIO.OUT)
          GPIO.setup(SPIMISO, GPIO.IN)
          GPIO.setup(SPICLK, GPIO.OUT)
          GPIO.setup(SPICS, GPIO.OUT)
          pass

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def currentVoltage():
                 ad_value = readadc(AO_pin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                 voltage= ad_value*(3.3/1024)*5
                 return voltage

def waitForStart(conn, mintime, minvolts):
        print 'Standing By'
	global durStart
        while True:
                timeout = time.time() + mintime
                while time.time() < timeout:
                    #print 'light on, but waiting for minOnTime'
                    if currentVoltage() < minvolts:
                        #print 'just a blink, still waiting'
                        break
                else:
                    break
                time.sleep(0.05)
        print '{} {} {} {}'.format('Cycle started at',datetime.datetime.now().isoformat(), 'ISO Week:', date.today().isocalendar()[1])
        durStart = time.time()
        standbyTime = float(durStart) - float(durEnd)
        standbyRd = round(standbyTime, 2)
        week = 'W' + str(date.today().isocalendar()[1])
        isoDate = datetime.datetime.now()
        unixTime = time.time()
        event = (week,isoDate,unixTime,node,'Cycle Start',standbyRd)
        sqlite_lib.create_event(conn,event)
        return durStart

def waitForEnd(conn, mintime, minvolts):
        print 'In Cycle'
	global durEnd
        while True:
                if currentVoltage() > minvolts:
                    time.sleep(0.05)
                    #print 'waiting for end of cycle'
                else:
                    print '{} {} {} {}'.format('Cycle ended at',datetime.datetime.now().isoformat(), 'ISO Week:', date.today().isocalendar()[1])
                    durEnd = time.time()
                    durTot = float(durEnd) - float(durStart) + mintime
  		    durTotRnd = round(durTot, 2)
                    week = 'W' + str(date.today().isocalendar()[1])
                    isoDate = datetime.datetime.now()
                    unixTime = time.time()
                    event = (week,isoDate,unixTime,node,'Cycle End',durTotRnd)
                    sqlite_lib.create_event(conn,event)
                    break
        return durEnd

def main():
         init() #set GPIO
         time.sleep(2)
         conn = sqlite_lib.create_connection()
         minOnTime = 2
         minVolts = 2
         print"Starting"
         while True:
                  waitForStart(conn, minOnTime, minVolts)
                  time.sleep(0.05)
                  waitForEnd(conn, minOnTime, minVolts)
                  durTot = float(durEnd) - float(durStart) + minOnTime
	          durTotRnd = round(durTot, 3)
                  print '{} {} {} {}'.format(node,'cycle duration', durTotRnd, 'seconds')
                  #each node user must be named for the machine on which it is logging




if __name__ =='__main__':
         try:
                  main()
         except KeyboardInterrupt:
                  pass
GPIO.cleanup()
