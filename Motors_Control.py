import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep, time

# Pin definitions
led_pin = 4
servo1_pin = 15
servo2_pin = 18
trig_pin = 25
echo_pin = 8
l298n_in1_pin = 2
l298n_in2_pin = 6
l298n_in3_pin = 3
l298n_in4_pin = 13

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set pin modes output\input
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(l298n_in1_pin, GPIO.OUT)
GPIO.setup(l298n_in2_pin, GPIO.OUT)
GPIO.setup(l298n_in3_pin, GPIO.OUT)
GPIO.setup(l298n_in4_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

servo = Servo(servo2_pin)

    
def forward(x):
    GPIO.output(l298n_in1_pin, GPIO.HIGH)
    GPIO.output(l298n_in3_pin, GPIO.HIGH)
    print("Moving Forward")
    sleep(x)
    GPIO.output(l298n_in1_pin, GPIO.LOW)
    GPIO.output(l298n_in3_pin, GPIO.LOW)

def reverse(x):
    GPIO.output(l298n_in2_pin, GPIO.HIGH)
    GPIO.output(l298n_in4_pin, GPIO.HIGH)
    print("Moving Reverse")
    sleep(x)
    GPIO.output(l298n_in2_pin, GPIO.LOW)
    GPIO.output(l298n_in4_pin, GPIO.LOW)

def distance():
    # set Trigger to HIGH
    GPIO.output(trig_pin, True)
 
    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(trig_pin, False)
 
    StartTime = time()
    StopTime = time()
 
    # save StartTime
    while GPIO.input(echo_pin) == 0:
        StartTime = time()
 
    # save time of arrival
    while GPIO.input(echo_pin) == 1:
        StopTime = time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance



while True:
    
    #forward(1)
    #reverse(1)
    #sleep(5)

    #servo.min()
    #sleep(0.5)
    #servo.mid()
    #sleep(0.5)
    #servo.max()
    #sleep(0.5)
    
    #GPIO.output(led_pin, GPIO.HIGH) # Turn LED on
    #sleep(1)                   # Delay for 1 second
    #GPIO.output(led_pin, GPIO.LOW)  # Turn LED off
    #sleep(1)
    # Delay for 1 second

    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)
    sleep(1)
    
    