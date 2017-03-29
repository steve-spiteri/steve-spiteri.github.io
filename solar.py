#!/usr/bin/python

import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import smbus
import sys
import requests

GPIO.VERSION
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

try:
    while True:
        sensor = BMP085.BMP085()
        bus = smbus.SMBus(1)

        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        # Un-comment the line below to convert the temperature to Fahrenheit.
        # temperature = temperature * 9/5.0 + 32
        temp = sensor.read_temperature()
        pressure = sensor.read_pressure()
        altitude = sensor.read_altitude()
        power = bus.read_byte(0x48)/50
        light = bus.read_byte(0x48)
        time_date = str(time.strftime("%d/%m/%Y %H:%M:%S"))
        print('Temp = {0:0.2f} *C'.format(temp))
        print('Humidity={0:0.1f}%'.format(humidity))
        print('Pressure = {0:0.2f} Pa'.format(pressure))
        print('Altitude = {0:0.2f} m'.format(altitude))
        print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
        bus.write_byte_data(0x48,0x40 | ((0) & 0x03), 0)
        print('Solar Panel (V) = {0:0.2f}'.format(power))
        bus.write_byte_data(0x48,0x40 | ((2) & 0x03), 0)
        print('Light Level = {0:0.2f}'.format(light))
        print('Time = '+ time_date + '\n\n')
        # the next two lines are part of the database uploading, keep them commented out for hardware build
        # url = 'http://springdb.eu5.org/spring/test_files/insert_test_input.php?id_login=99&power='+str(power)+'&temperature='+str(temp)+'&light='+str(light)+'&bar_pressure='+str(pressure)+'&humidity='+str(humidity)+'&date='+str(time_date)
        # requests.get(url)
        # if the code reaches here, all sensors worked, turn led green
        GPIO.output(11,0)
        GPIO.output(12,1)
        time.sleep(15)
        
except Exception:
    # if the code reaches here, a sensor failed, led turns red
    GPIO.output(11,1)
    GPIO.output(12,0)
except KeyboardInterrupt:
    GPIO.cleanup()