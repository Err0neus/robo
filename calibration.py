import RPi.GPIO as GPIO
import time

#set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

pin = 21
print("working with pin " + str(pin))
#set poin as otuptu ans set servo1 and as PWM
GPIO.setup(pin, GPIO.OUT)
servo1 = GPIO.PWM(pin, 50) # pin 18, 50Hz pulse

# start PWM running, but with no pulse
servo1.start(3)
print('setting up')
time.sleep(1)

start = 3
neutral = 6.5
stop =  11
increment = .2 # must be a int division of 0.5

print('start')
servo1.ChangeDutyCycle(start)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
time.sleep(2)
current = start

def move(to):
    global current
    if current > to:
        while current > to:
            current -= increment
            servo1.ChangeDutyCycle(current)
            time.sleep(0.02)
        servo1.ChangeDutyCycle(to)
    elif current < to:
        while current < to:
            current += increment
            servo1.ChangeDutyCycle(current)
            time.sleep(0.02)
        servo1.ChangeDutyCycle(to)
        
    servo1.ChangeDutyCycle(0)
    time.sleep(2)
    
print('neutral')
move(neutral)

print('stop')
move(stop)

print('start')
move(start)

time.sleep(3)
servo1.stop()
GPIO.cleanup()
print('bye')