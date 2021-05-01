import RPi.GPIO as GPIO
import time
import sys, termios, tty, os

#-----------------------------------------------------
# Global settings
##
# set off warnings
GPIO.setwarnings(False)
#set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

#-----------------------------------------------------
# TILT
# servo MG90D, limited angle type
# tested responsivness from 3.2 to 11.1 duty PWM
# approx 160 degrees angle

# setup
pin = 21
GPIO.setup(pin, GPIO.OUT)
tilt = GPIO.PWM(pin, 50) # 50 Hz
# set min and max values for tilt pwm
tilt_min = 4
tilt_mid = 7.5
tilt_max = 11
degree = 1./150.*(tilt_max-tilt_min)
increment = degree*2 # increment to add to servo positions
step_sleep = 0.025 # time to sleep between increments

# initiate
tilt.start(0)
tilt.ChangeDutyCycle(0)
tilt_current = tilt_min

# startup seqence
def tilt_initiate():
    global tilt_current
    while tilt_current < tilt_mid:
        print('initiating')
        tilt_current += increment
        tilt.ChangeDutyCycle(tilt_current)
        time.sleep(step_sleep)
    tilt_current = tilt_mid
    tilt.ChangeDutyCycle(tilt_current)
    time.sleep(step_sleep)
    tilt.ChangeDutyCycle(0)
    print('ready')
# shutdown sequence
def tilt_shutdown():
    global tilt_current
    while tilt_current > tilt_min:
        print('shutting down')
        tilt_current -= increment
        tilt.ChangeDutyCycle(tilt_current)
        time.sleep(step_sleep)
    tilt_current = tilt_min
    tilt.ChangeDutyCycle(tilt_current)
    time.sleep(step_sleep)
    tilt.ChangeDutyCycle(0)
    print('shut down')
# functions to change values of tilt
def tilt_up():
    global tilt_current
    if tilt_current < tilt_max:
        print('tilting up')
        tilt_current += increment
        tilt.ChangeDutyCycle(tilt_current)
        time.sleep(step_sleep)
    
def tilt_down():
    global tilt_current
    if tilt_current > tilt_min:
        print('tilting down')
        tilt_current -= increment
        tilt.ChangeDutyCycle(tilt_current)
        time.sleep(step_sleep)
    #tilt.ChangeDutyCycle(tilt_min)


    

# function to read keyboard input
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

#-----------------------------------------------------
# ROTOR

# servo MG996R, continuous 360 degree

#-------------------------------------------------
# MOTION

#Set variables for the GPIO motor pins
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

# Set the GPIO Pin mode
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

# Turn all motors off
def StopMotors():
    GPIO.output(pinMotorAForwards, 0)
    GPIO.output(pinMotorABackwards, 0)
    GPIO.output(pinMotorBForwards, 0)
    GPIO.output(pinMotorBBackwards, 0)

# Turn both motors forwards
def Forwards():
    GPIO.output(pinMotorAForwards, 1)
    GPIO.output(pinMotorABackwards, 0)
    GPIO.output(pinMotorBForwards, 1)
    GPIO.output(pinMotorBBackwards, 0)

# Turn both motors backwards
def Backwards():
    GPIO.output(pinMotorAForwards, 0)
    GPIO.output(pinMotorABackwards, 1)
    GPIO.output(pinMotorBForwards, 0)
    GPIO.output(pinMotorBBackwards, 1)

def Left():
    GPIO.output(pinMotorAForwards, 1)
    GPIO.output(pinMotorABackwards, 0)
    GPIO.output(pinMotorBForwards, 0)
    GPIO.output(pinMotorBBackwards, 1)

def Right():
    GPIO.output(pinMotorAForwards, 0)
    GPIO.output(pinMotorABackwards, 1)
    GPIO.output(pinMotorBForwards, 1)
    GPIO.output(pinMotorBBackwards, 0)

StopMotors()


button_delay = 0.2
# START

tilt_initiate()
while True:
    
    char = getch()
    if (char == "q"):
        tilt_shutdown()
        exit(0)
    if (char == "i"):
        tilt_up()
    if (char == "k"):
        tilt_down()
        
    if (char == "a"):
        print 'Left pressed'
        Left()
        time.sleep(button_delay)

    if (char == "d"):
        print 'Right pressed'
        Right()
        time.sleep(button_delay)          

    elif (char == "w"):
        print 'Up pressed' 
        Forwards()       
        time.sleep(button_delay)          
    
    elif (char == "s"):
        print 'Down pressed'      
        Backwards()
        time.sleep(button_delay)
    
    StopMotors()    
    tilt.ChangeDutyCycle(0)
    