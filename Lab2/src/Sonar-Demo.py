#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
range_finder_e = Sonar(brain.three_wire_port.e)


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
## A basic line following program that uses checker/handlers
## See lecture notes for the state diagram

ROBOT_IDLE = 0
ROBOT_STANDOFF = 1

robotState = ROBOT_IDLE

# Controller
controller = Controller()

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

Kp = 10 ## TODO: Pick a Kp to start; then adjust to get good performance

## Sonar timer handler. Note that we check the state and act accordingly
def handleSonarTimer():
    if(robotState == ROBOT_STANDOFF):
        distance = range_finder_e.distance(MM) / 10
        print(distance)

        # TODO: Define the error
        distance_error = 5 - distance

        # TODO: Calculate the effor from the error
        driving_effort = Kp * distance_error
                
        # TODO: Control the motor speeds 
        left_motor.spin(FORWARD, driving_effort, RPM)
        right_motor.spin(FORWARD, driving_effort, RPM)

    ## Don't forget to restart the timer!
    sonarTimer.event(handleSonarTimer, 50)

## The line timer will tell us when to correct the heading
sonarTimer = Timer()

## This uses the VEX event machinery, 'automatic' checker-handler
## It has the same functionality as "if check timer expired -> handle timer expired"
## Maybe adust the timer interval
sonarTimer.event(handleSonarTimer, 50)

## Button handler. Note that we check the state and then act accordingly
def handleLeft1Button():
    global robotState
    print("Button L1")
    if(robotState == ROBOT_IDLE):
        robotState = ROBOT_STANDOFF        
    elif(robotState == ROBOT_STANDOFF):
        robotState = ROBOT_IDLE    
        left_motor.stop()
        right_motor.stop()    

## Same as "if check button press -> handle button press"
controller.buttonL1.pressed(handleLeft1Button)

## Everything is event-driven through the event library...no code in the main loop!
while True:
    pass