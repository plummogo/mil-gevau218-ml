# import lib
from tkinter import *
import glob
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)      # SET GPIO NUMBER BOARD
GPIO.setup(11, GPIO.OUT)      # RED LED
GPIO.setup(13, GPIO.OUT)      # BLUE LED
GPIO.setup(15, GPIO.OUT)      # GREEN LED
GPIO.setup(37, GPIO.IN)       # BUTTON

time1 =''
window = Tk()
prev_input = 0

# read sensor address
sysDir = '/sys/bus/w1/devices/'
w1Device = glob.glob(sysDir + '28*')[0]
w1Slave = w1Device + '/w1_slave'

def readTempDev():
  f = open(w1Slave, 'r')
  lines = f.readlines()
  f.close()
  return lines

def readTemp():
  lines = readTempDev()

  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = readTempDev()

  tEquals = lines[1].find('t=')

  if tEquals != -1:
    tempValue = lines[1][tEquals+2:]
    tempCelsius = round((float(tempValue) / 1000.0), 1)
    return tempCelsius

# get system time
def tick():
  global time1
  time2=datetime.datetime.now().strftime('%H:%M:%S')
  if time2 != time1:
    time1 = time2
    curTime.config(text=time2)
    curTemp.config(text=readTemp())
  curTime.after(200,tick)

def close():
    window.destroy()

# create ui window 
window.title('Measure temperature with DS18B20')
window.geometry("300x150")
time = Label(window, text='Time: ').grid(row=1, column=0, sticky = W)
curTime = Label(window, font = ('fixed', 12),)
curTime.grid(sticky = N, row = 1, column = 1, padx = 5, pady = (10,10))
temp = Label(window, text='Temperature: ').grid(row=2, column=0, sticky = W)
curTemp = Label(window, font = ('fixed', 12),)
curTemp.grid(sticky = N, row = 2, column = 1, padx = 5, pady = (10,10))
button = Button(window, text = "Exit", command = close)
button.grid(sticky = N, row = 3, column = 1, padx = 5, pady = (10,10))

window.mainloop()

while True:
    GPIO.output(15, 1)
    input = GPIO.input(37)

    if ((not prev_input) and input):
        GPIO.output(15, 0)
        GPIO.output(13, GPIO.HIGH)
        time.sleep(5)
        tick()
        GPIO.output(15, 1)
    else:
        GPIO.output(15, 0)
        GPIO.output(11, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(15, 1)
    prev_input = input
    time.sleep(0.05)