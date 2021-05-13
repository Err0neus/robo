import RPi.GPIO as GPIO
import time
import sys, termios, tty, os

#-----------------------------------------------------
# Global settings

# set off warnings
GPIO.setwarnings(False)
#set GPIO numbering mode
GPIO.setmode(GPIO.BCM)


degree = 1./150.*(12-2) # max - min servo positiont
increment = degree*3 # increment to add to servo positions
step_sleep = 0.03 # time to sleep between increments


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
    print('tilt ready')
# shutdown sequence
def tilt_shutdown():
    global tilt_current
    while tilt_current > tilt_min:
        print('shutting down tilt')
        tilt_current -= increment
        tilt.ChangeDutyCycle(tilt_current)
        time.sleep(step_sleep)
    tilt_current = tilt_min
    tilt.ChangeDutyCycle(tilt_current)
    time.sleep(step_sleep)
    tilt.ChangeDutyCycle(0)
    print('tilt shut down')
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

# servo MG996R, digi hi torque
# setup
pin = 20
GPIO.setup(pin, GPIO.OUT)
rotor = GPIO.PWM(pin, 50) # 50 Hz
# set min and max values for tilt pwm
rotor_min = 2
rotor_mid = 7
rotor_max = 12

# initiate
rotor.start(0)
rotor.ChangeDutyCycle(0)
rotor_current = rotor_mid

# startup seqence
def rotor_initiate():
    global rotor_current
    while rotor_current < rotor_mid:
        print('initiating rotor')
        rotor_current += increment
        rotor.ChangeDutyCycle(rotor_current)
        time.sleep(step_sleep)
    rotor_current = rotor_mid
    rotor.ChangeDutyCycle(rotor_current)
    time.sleep(step_sleep)
    rotor.ChangeDutyCycle(0)
    global rotor_current
    if rotor_current > rotor_mid:
        while rotor_current > rotor_mid:
            print('initiating rotor')
            rotor_current -= increment
            rotor.ChangeDutyCycle(rotor_current)
            time.sleep(step_sleep)
        rotor_current = rotor_mid
        rotor.ChangeDutyCycle(rotor_current)
    if rotor_current < rotor_mid:
        while rotor_current < rotor_mid:
            print('initiating rotor')
            rotor_current += increment
            rotor.ChangeDutyCycle(rotor_current)
            time.sleep(step_sleep)
        rotor_current = rotor_mid
        rotor.ChangeDutyCycle(rotor_current)
        time.sleep(step_sleep)
    rotor.ChangeDutyCycle(0)
    print('rotor ready')
# shutdown sequence
def rotor_shutdown():
    global rotor_current
    if rotor_current > rotor_mid:
        while rotor_current > rotor_mid:
            print('shutting down')
            rotor_current -= increment
            rotor.ChangeDutyCycle(rotor_current)
            time.sleep(step_sleep)
        rotor_current = rotor_mid
        rotor.ChangeDutyCycle(rotor_current)
    if rotor_current < rotor_mid:
        while rotor_current < rotor_mid:
            print('shutting down')
            rotor_current += increment
            rotor.ChangeDutyCycle(rotor_current)
            time.sleep(step_sleep)
        rotor_current = rotor_mid
        rotor.ChangeDutyCycle(rotor_current)
        time.sleep(step_sleep)
    rotor.ChangeDutyCycle(0)
    print('rotor shut down')
# functions to change values of rotor
def rotor_left():
    global rotor_current
    if rotor_current < rotor_max:
        print('rotating left')
        rotor_current += increment
        rotor.ChangeDutyCycle(rotor_current)
        time.sleep(step_sleep)
    
def rotor_right():
    global rotor_current
    if rotor_current > rotor_min:
        print('rotating right')
        rotor_current -= increment
        rotor.ChangeDutyCycle(rotor_current)
        time.sleep(step_sleep)
    #tilt.ChangeDutyCycle(tilt_min)


    

#-------------------------------------------------
# MOTION

#Set variables for the GPIO motor pins
pinMotorAForwards = 8
pinMotorABackwards = 7
pinMotorBForwards = 9
pinMotorBBackwards = 10

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
    GPIO.output(pinMotorAForwards, 0)
    GPIO.output(pinMotorABackwards, 1)
    GPIO.output(pinMotorBForwards, 1)
    GPIO.output(pinMotorBBackwards, 0)

def Right():
    GPIO.output(pinMotorAForwards, 1)
    GPIO.output(pinMotorABackwards, 0)
    GPIO.output(pinMotorBForwards, 0)
    GPIO.output(pinMotorBBackwards, 1)

StopMotors()


button_delay = 0.2
# START

tilt_initiate()
rotor_initiate()

while True:
    
    char = getch()
    if (char == "q"):
        tilt_shutdown()
        rotor_shutdown()
        exit(0)
    if (char == "i"):
        tilt_up()
    if (char == "k"):
        tilt_down()
    if (char == "j"):
        rotor_left()
    if (char == "l"):
        rotor_right()
        
    if (char == "a"):
        print 'moving left'
        Left()
        time.sleep(button_delay)

    if (char == "d"):
        print 'moving right'
        Right()
        time.sleep(button_delay)          

    elif (char == "w"):
        print 'moving forwards' 
        Forwards()       
        time.sleep(button_delay)          
    
    elif (char == "s"):
        print 'moving backwards'      
        Backwards()
        time.sleep(button_delay)
    
    StopMotors()    
    tilt.ChangeDutyCycle(0)
    rotor.ChangeDutyCycle(0)
    