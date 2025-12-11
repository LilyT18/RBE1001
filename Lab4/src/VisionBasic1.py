#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
# AI Vision Color Descriptions
#ai_vision_15__Red_Folder = Colordesc(1, 222, 31, 63, 11, 0.48)
ai_vision_15_green = Colordesc(1, 114, 247, 118, 10, 0.2)
ai_vision_15_orange = Colordesc(2, 232, 143, 125, 10, 0.2)
ai_vision_15_purple = Colordesc(3, 181, 135, 217, 10, 0.2)
# AI Vision Code Descriptions
ai_vision_15 = AiVision(Ports.PORT15, ai_vision_15_green)
bumper_g = Bumper(brain.three_wire_port.g)


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
'''
This code demonstrates a basic search and drive towards behaviour with the camera.

The robot has three states:
    IDLE - waiting for the button press
    SEARCHING - spins slowly until it finds an object
    APPROACHING - drives towards the object

Camera checking is done on a timer. If no object is found, a counter is incremented and
if the counter reaches a threshold, the robot goes back into searching mode.
'''

## Define states and state variable
ROBOT_IDLE = 0
ROBOT_SEARCHING = 1
ROBOT_APPROACHING = 2

current_state = ROBOT_IDLE

'''
We'll use a timer to read the camera every cameraInterval milliseconds
'''
cameraInterval = 50
cameraTimer = Timer()

def handleButton():
    global current_state

    if(current_state == ROBOT_IDLE):
        print('IDLE -> SEARCHING') ## Pro-tip: print out state _transitions_
        current_state = ROBOT_SEARCHING
        left_motor.spin(FORWARD, 30)
        right_motor.spin(FORWARD, -30)

        ## start the timer for the camera
        cameraTimer.event(cameraTimerCallback, cameraInterval)

    else: ## failsafe; go to IDLE from any other state when button is pressed
        print(' -> IDLE')
        current_state = ROBOT_IDLE
        left_motor.stop()
        right_motor.stop()

bumper_g.pressed(handleButton)

def cameraTimerCallback():
    global current_state
    global missedDetections

    ## Here we use a checker-handler, where the checker checks if there is a new object detection.
    ## We don't use a "CheckForObjects()" function because take_snapshot() acts as the checker.
    ## It returns a non-empty list if there is a detection.
    objects = ai_vision_15.take_snapshot(ai_vision_15_green)
    if objects: 
        print("Object detected")
        handleObjectDetection()

    # restart the timer
    if(current_state != ROBOT_IDLE):
        cameraTimer.event(cameraTimerCallback, cameraInterval)

def handleObjectDetection():
    global current_state
    global object_timer

    cx = ai_vision_15.largest_object().centerX
    cy = ai_vision_15.largest_object().centerY
    width = ai_vision_15.largest_object().width
    height = ai_vision_15.largest_object().height

    ## TODO: Add code to print out the coordinates and size
    print("Coordinates: " + str(cx) + "," + str(cy))
    print("Size(w,h):" + str(width) + "," + str(height))


    if current_state == ROBOT_SEARCHING:
        print('SEARCHING -> APPROACHING') ## Pro-tip: print out state _transitions_
        current_state = ROBOT_APPROACHING

    ## Not elif, because we want the logic to cascade
    if current_state == ROBOT_APPROACHING:

        target_x = 160
        K_x = 0.2

        error = cx - target_x
        turn_effort = K_x * error


        ## TODO: Edit code to approach or back up to hold the right position
        left_motor.spin(FORWARD, 20 - turn_effort)
        right_motor.spin(FORWARD, 20 + turn_effort)

        



## Our main loop
while True:
    cameraTimerCallback()
