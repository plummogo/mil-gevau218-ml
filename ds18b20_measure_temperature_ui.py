# import lib
from tkinter import *
import glob
import time
import datetime

time1 =''

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

# grafikus ablak létrehozása
window = Tk()
window.title('Measure temperature with DS18B20')
window.geometry("300x150")
time = Label(window, text='Idő: ').grid(row=1, column=0, sticky = W)
curTime = Label(window, font = ('fixed', 12),)
curTime.grid(sticky = N, row = 1, column = 1, padx = 5, pady = (10,10))
temp = Label(window, text='Hőmérséklet: ').grid(row=2, column=0, sticky = W)
curTemp = Label(window, font = ('fixed', 12),)
curTemp.grid(sticky = N, row = 2, column = 1, padx = 5, pady = (10,10))
button = Button(window, text = "EXIT", command = close)
button.grid(sticky = N, row = 3, column = 1, padx = 5, pady = (10,10))

tick()
window.mainloop()