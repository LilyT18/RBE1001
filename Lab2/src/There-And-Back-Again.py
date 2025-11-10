#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
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
#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

# Button
button_g = Bumper(brain.three_wire_port.d)

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

# Begin project code


# define the states
IDLE = 0
DRIVING_OUT = 1
TURNING = 2
DRIVING_BACK = 3

current_state = IDLE


"""
Pro-tip: print out upon state transistions.
"""
def handleButton():
    global current_state

    if(current_state == IDLE):
        print('IDLE -> DRIVING')
        current_state = DRIVING_OUT
        left_motor.spin_for(FORWARD, 10, TURNS, 60, RPM, wait = False)
        right_motor.spin_for(FORWARD, 10, TURNS, 60, RPM, wait = False)

    else:
        print(' -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

wasMoving = False
def checkMotionComplete():
    global wasMoving

    retVal = False

    isMoving = left_motor.is_spinning() or right_motor.is_spinning()

    if(wasMoving and not isMoving):
        retVal = True

    wasMoving = isMoving
    return retVal

def handleMotionComplete():
    global current_state

    if(current_state == DRIVING_OUT):
        print('DRIVING_OUT -> TURNING')
        current_state = TURNING
        left_motor.spin_for(REVERSE, 7, TURNS, 60, RPM, wait = False)
        right_motor.spin_for(FORWARD, 7, TURNS, 60, RPM, wait = False)

    elif(current_state == TURNING):
        print('TURNING -> DRIVING_BACK')
        current_state = DRIVING_BACK
        left_motor.spin_for(FORWARD, 10, TURNS, 60, RPM, wait = False)
        right_motor.spin_for(FORWARD, 10, TURNS, 60, RPM, wait = False)
    
    elif(current_state == DRIVING_BACK):
        print('DRIVING_BACK -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()


"""
The line below makes use of VEX's built-in event management. Basically, you set up a "callback", 
basically, a function that gets called whenever the button is pressed (there's a corresponding
one for released). Whenever the button is pressed, the handleButton function will get called,
_without you having to do anything else_.

"""
button_g.pressed(handleButton)

handleButton()

"""
Note that the main doesn't "do" anything. That is because the event (button press) is captured
automatically. So we have an empty main program!!!
"""
# The main loop
while True:
    if(checkMotionComplete()): handleMotionComplete()

    ## make things easier to read, when we print
    ## you may want to comment it out to improve performance
    sleep(50) 
