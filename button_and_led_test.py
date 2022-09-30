import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN) # button input
GPIO.setup(33, GPIO.OUT) # green led output
GPIO.setup(34, GPIO.OUT) # red led output

prev_input = 0
while True:
    input = GPIO.input(37)
    if ((not prev_input) and input):
        print ("Gomb lenyomva")
        GPIO.output(33, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(34, GPIO.HIGH)
    else:
        GPIO.output(33, GPIO.LOW)
        GPIO.output(34, GPIO.LOW)
    prev_input = input
    time.sleep(0.2)