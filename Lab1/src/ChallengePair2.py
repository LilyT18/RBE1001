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

# Make random actually random
#def initializeRandomSeed():
 #   wait(100, MSEC)
  #  random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
   # urandom.seed(int(random))
      
# Set random seed 
#initializeRandomSeed()

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
distanceOfTravel = float("inf") #in turns approx. 1m
speedOfTravel = 150 #in RPM

# start out in the idle state
current_state = IDLE

# Bumper
bumperSwitch = Bumper(brain.three_wire_port.g) #Check port number

# Reflectance
reflectanceSensor = Line(brain.three_wire_port.a) #Check port number

# Rangefinder
rangefinder = Sonar(brain.three_wire_port.e) #Check port number

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
        
        drive_for(FORWARD, distanceOfTravel, speedOfTravel)
        
    else: # in any other state, the button acts as a kill switch
        print(' -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

# Handler for the bumper switch
def handleBumperG():
    global current_state

    if(current_state == DRIVING_FWD):
        print('FORWARD -> BACKWARD')
        current_state = DRIVING_BKWD
      
        drive_for(REVERSE, distanceOfTravel, speedOfTravel)
    
    elif(current_state == DRIVING_BKWD):
        print('BACKWARD -> IDLE')
        current_state = IDLE

    else:
        print('E-stop')


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
        print('FORWARD -> BACKWARD')
        current_state = DRIVING_BKWD
      
        drive_for(REVERSE, distanceOfTravel, speedOfTravel)
    
    elif(current_state == DRIVING_BKWD):
        print('BACKWARD -> IDLE')
        current_state = IDLE

    else:
        print('E-stop') # Should print when button is used as E-stop


## Checker for the reflectance sensor
wasTriggered = False
def checkReflectanceTriggered():
    global wasTriggered

    retVal = False

    isTriggered = reflectanceSensor.value() < 2600 #Value might have to be adjusted

    if(wasTriggered and not isTriggered):
        retVal = True

    wasTriggered = isTriggered
    return retVal

## Handler for when the reflectance sensor triggers
def handleReflectanceTriggered():
    global current_state
    
    if(current_state == DRIVING_FWD):
        print('FORWARD -> BACKWARD')
        current_state = DRIVING_BKWD
      
        drive_for(REVERSE, distanceOfTravel, speedOfTravel)
    
    elif(current_state == DRIVING_BKWD):
        print('BACKWARD -> IDLE')
        current_state = IDLE

    else:
        print('E-stop')


controller_1.buttonL1.pressed(handleLeft1Button)
  
bumperSwitch.pressed(handleBumperG)


# The main loop
while True:
    if(checkMotionComplete()): handleMotionComplete()
    if(checkReflectanceTriggered()): handleReflectanceTriggered()