#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
ROBOT_IDLE = 0
ROBOT_LEFTING = 1
ROBOT_RIGHTING = 2

robotState = ROBOT_IDLE

controller = Controller()

imu = Inertial(Ports.PORT20)

left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

def IMU_event_handler():
    print(imu.rotation())

    ## TODO: Nested checker to see if we've turned far enough
    ## You'll need to check the state and then the value
    if (robotState == ROBOT_LEFTING): pass
    elif (robotState == ROBOT_RIGHTING): pass

imu.changed(IMU_event_handler)

initialHeading = 0

## Button handler. Note that we check the state and then act accordingly
def handleLeft1Button():
    global robotState
    global initialHeading
    print("Button L1")

    ## Store the heading when we start so we can check if we're done later
    initialHeading = imu.rotation()
    robotState = ROBOT_LEFTING    
    left_motor.spin(REVERSE, 60)
    right_motor.spin(FORWARD, 60)

## Button handler. Note that we check the state and then act accordingly
def handleRight1Button():
    global robotState
    global initialHeading
    print("Button R1")

    ## Store the heading when we start so we can check if we're done later
    initialHeading = imu.rotation()
    robotState = ROBOT_RIGHTING    
    left_motor.spin(FORWARD, 60)
    right_motor.spin(REVERSE, 60)

controller.buttonL1.pressed(handleLeft1Button)
controller.buttonR1.pressed(handleRight1Button)

while True:
    pass
