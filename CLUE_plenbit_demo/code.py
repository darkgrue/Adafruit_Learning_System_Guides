# Simple demo for controlling the plen:bit robot
# NOTE: MUST CUT MIDDLE TRACE ON PCA9685 ADDRESS JUMPER!

import time
import busio
import board
from digitalio import DigitalInOut, Direction
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x68)
pca.frequency = 50
led = DigitalInOut(board.P16)
led.direction = Direction.OUTPUT
led.value = True

while True:
    pass
servoSetInit = (1000, 630, 500, 600, 240, 600, 1000, 720)
servoAngle = [1000, 630, 500, 600, 240, 600, 1000, 720]
motionSpeed = 15
servos = []
for s in range(8):
    servos.append(servo.Servo(pca.channels[s], min_pulse=800, max_pulse=2200))

def servoInitialSet():
    print("Initialize servos")
    for n in range(8):
        servos[n].angle = servoSetInit[n] / 10

def servoFree(serv = None):
    if serv:
        print("Release servo #", serv)
        servos[serv].angle = None
    else:
        print("Release all servos")
        for ser in servos:
            ser.angle = None

def servoWrite(num, degrees):
    degrees = min(max(degrees, 0), 180)
    servos[num].angle = degrees

# angle is a list of 8 target values
def setAngle(angle, msec):
    step = [0, 0, 0, 0, 0, 0, 0, 0]
    msec = msec / motionSpeed # now 15//default 10; //speedy 20   Speed Adj
    for val in range(8):
        target = servoSetInit[val] - angle[val]
        target = min(max(target, 0), 1800)
        if target != servoAngle[val]: # Target != Present
            step[val] = (target - servoAngle[val]) / msec
    #print(step)
    for _ in range(msec):
        for val in range(8):
            servoAngle[val] += step[val]
            #print("setting servo %d to %d" % (val, int(servoAngle[val] / 10)))
            servoWrite(val, servoAngle[val] / 10)
        #time.sleep(msec / 1000)
    print(servoAngle)

servoInitialSet()
time.sleep(1)
setAngle([0, 0, -200, 0, 0, 0, 0, 0], 500)
setAngle([0, 0, -1800, 0, 0, 0, 1800, 0], 500)
setAngle([900, 0, -1800, 0, -900, 0, 1800, 0], 500)
setAngle([900, 0, -200, 0, -900, 0, 0, 0], 500)
setAngle([900, 0, -1800, 0, -900, 0, 1800, 0], 500)
setAngle([900, 0, -200, 0, -900, 0, 0, 0], 500)
setAngle([0, 0, -200, 0, 0, 0, 0, 0], 500)
servoFree()
