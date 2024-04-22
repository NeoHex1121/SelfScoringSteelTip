import RPi.GPIO as GPIO
import time

x_channel = []
x_fpga = []
y_channel = []
y_fpga = []

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)



CS7 = 7
GPIO.setup(CS7, GPIO.IN)

A73 = 13
GPIO.setup(A73, GPIO.IN)

while True: 
    if (GPIO.input(CS7)) and (GPIO.input(A73)) == 0:
        x_channel = '010100'
        x_fpga = 'CS7'
        y_channel = '010100'
        y_fpga = 'A73'
    print (y_channel, y_fpga, x_channel, x_fpga)