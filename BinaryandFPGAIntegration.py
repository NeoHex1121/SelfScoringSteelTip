import RPi.GPIO as GPIO
import itertools
import time

# Setup GPIO
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setwarnings(False)

# Define channel select pins and FPGA output pins with labels
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

A71 = 3
A72 = 5
CS7 = 7
A73 = 11
A74 = 13

fpga_output_pins = [GPIO.setup(A71, GPIO.IN), GPIO.setup(A72, GPIO.IN), GPIO.setup(CS7, GPIO.IN), GPIO.setup(A73, GPIO.IN), GPIO.setup(A74, GPIO.IN)]
x_fpga = []
y_fpga = []
binary_list = []

current_binary = binary_list
# Create an infinite iterator
infinite_iterator = itertools.cycle(binary_list)

# Function to trigger FPGA outputs
#def trigger_fpgas():
    # Trigger all FPGAs
    #for pin, name in fpga_output_pins.items():
       # GPIO.output(pin, GPIO.HIGH)
    #time.sleep(0.1)  # Hold high for a short time to simulate detection
    #for pin, name in fpga_output_pins.items():
        #GPIO.output(pin, GPIO.LOW)

# Time delay in seconds between each binary number
time_delay = 0.5  # Adjust as needed

# Main loop to continuously set pins and trigger FPGAs
try:
    while True:
        for i in range(37):
            count=(i) 
        if i == 37:
            i == 0
        binary_list = (list(bin(i)[2:].zfill(6)))
        if binary_list [0] == 1:
            GPIO.output(8, GPIO.HIGH)
        if binary_list [0] == 0:
            GPIO.output(8, GPIO.LOW)
        if binary_list [1] == 1:
            GPIO.output(10, GPIO.HIGH)
        if binary_list [1] == 0:
            GPIO.output(10, GPIO.LOW)
        if binary_list [2] == 1:
            GPIO.output(12, GPIO.HIGH)
        if binary_list [2] == 0:
            GPIO.output(12, GPIO.LOW)
        if binary_list [3] == 1:
            GPIO.output(16, GPIO.HIGH)
        if binary_list [3] == 0:
            GPIO.output(16, GPIO.LOW)
        if binary_list [4] == 1:
            GPIO.output(18, GPIO.HIGH)
        if binary_list [4] == 0:
            GPIO.output(18, GPIO.LOW)
        if binary_list [5] == 1:
            GPIO.output(22, GPIO.HIGH)
        if binary_list [5] == 0:
            GPIO.output(22, GPIO.LOW)
           
        if (GPIO.input(A71)) == 0:
            y_channel = current_binary
            y_fpga = A71
          
        if(GPIO.input(A72)) == 0:
            y_channel = current_binary
            y_fpga = A72
            
        if(GPIO.input(A73)) == 0:
            x_channel = current_binary
            x_fpga = A73
            
        if(GPIO.input(A74)) == 0:
            x_channel = current_binary
            x_fpga = A74
            
    print (y_channel, y_fpga, x_channel, x_fpga)
    time.sleep(time_delay)  # Short pause between updates
except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C exit
    GPIO.cleanup()

# Optionally add GPIO.cleanup() on normal exit too
