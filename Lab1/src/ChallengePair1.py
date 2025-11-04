#region VEXcode Generated Robot Configuration
from vex import *
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_36_1, False)
controller_1 = Controller(PRIMARY)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:      2025-11-03
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

# define the states
IDLE = 0
DRIVING_FWD = 1
DRIVING_BKWD = 2
HOOK_BASKET = 3
UNHOOK_BASKET = 4
ARM_UP = 5
ARM_DOWN = 6

#5 Turns equivalent to diameter of the 4in wheels
distanceOfTravel = 20 #in turns
speedOfTravel = 150 #in RPM

# start out in the idle state
current_state = IDLE

# Declaring Rangefinder
rangefinder = Sonar(brain.three_wire_port.c) #Check port number

# Helper function to drive both motors in the same direction
def drive_for(direction, turns, speed):
    left_motor.set_velocity(speed, RPM)
    left_motor.spin_for(direction, turns, TURNS, wait = False)

    right_motor.set_velocity(speed, RPM)
    right_motor.spin_for(direction, turns, TURNS, wait = False)

# Handler for the left1 button
def handleLeft1Button():
    global current_state
    print('Left 1 Button Pressed')

    if(current_state == IDLE):
        print('IDLE -> FORWARD')
        current_state = DRIVING_FWD
        
        drive_for(REVERSE, distanceOfTravel, speedOfTravel)
        
    else: # in any other state, the button acts as a kill switch
        print(' -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

# Checks for the _event_ of stopping (not just if the robot is stopped).
wasMoving = False
def checkMotionComplete():
    global wasMoving

    retVal = False

    isMoving = left_motor.is_spinning() or right_motor.is_spinning()

    if(wasMoving and not isMoving):
        retVal = True

    wasMoving = isMoving
    return retVal

# Then we declare a handler for the completion of the motion.
def handleMotionComplete():
    global current_state

    if(current_state == DRIVING_FWD):
        print('FORWARD -> HOOK_BASKET')
        current_state = HOOK_BASKET

        hookBasket()

    elif(current_state == HOOK_BASKET):
        print('HOOK_BASKET -> UNHOOK_BASKET')
        current_state = UNHOOK_BASKET 
           
    elif(current_state == UNHOOK_BASKET):
        print('UNHOOK_BASKET -> IDLE')
        current_state = IDLE


# Checker for the reflectance sensor
def checkRangeFinderDistance():
    if(rangefinder.distance(MM) < 55): #Need to test number
        return True
    return False

## Handler for when the reflectance sensor triggers
def handleRangeFinderDistance():
    global current_state
    
    if(current_state == DRIVING_FWD):
        print('FORWARD -> HOOK_BASKET')
        current_state = HOOK_BASKET

        hookBasket()
        
def hookBasket():
    left_motor.stop()
    right_motor.stop()
    arm_motor.set_velocity(50, RPM)
    arm_motor.spin_for(REVERSE, 400, DEGREES, wait = True)
    drive_for(FORWARD, 3, speedOfTravel)
    wait(1000, MSEC)
    arm_motor.spin_for(FORWARD, 70, DEGREES, wait = True)
    wait(5000, MSEC)
    print(arm_motor.torque())

def returnArmToStartPosition():
    arm_motor.spin_for(FORWARD, 330, DEGREES, wait = True)


controller_1.buttonL1.pressed(handleLeft1Button)
controller_1.buttonL2.pressed(returnArmToStartPosition)

# The main loop
while True:
    if(checkMotionComplete()): handleMotionComplete()
    if(checkRangeFinderDistance()): handleRangeFinderDistance()