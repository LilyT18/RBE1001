from vex import *

brain = Brain()
controller = Controller()

leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
distanceSensor = Sonar(brain.three_wire_port.e)#Check port number

countNumTurns = 0

distanceOfTravel = 2 # in rotations
speedOfTravel = 70 # in RPM

#States
IDLE = 0
DRVFWD = 1
TURNRIGHT = 2
TURNLEFT = 3

current_state = IDLE

def turn(direction):
    global countNumTurns
    countNumTurns += 1
    leftMotor.set_velocity(speedOfTravel, RPM)
    #left_motor.spin_for(direction, turns, TURNS, wait = False)

    rightMotor.set_velocity(speedOfTravel, RPM)
    #right_motor.spin_for(direction, turns, TURNS, wait = False)
    if direction == "LEFT":
        leftMotor.spin_for(FORWARD, 5, TURNS, 80, RPM)
        rightMotor.spin_for(REVERSE, 5, TURNS, 80, RPM)
    elif direction == "RIGHT":
        rightMotor.spin_for(FORWARD, 7.25, TURNS, 80, RPM)
        #leftMotor.spin_for(REVERSE, 5, TURNS, 80, RPM)
        
Kp = 10

def drive():
    leftMotor.set_velocity(speedOfTravel, RPM)
    leftMotor.spin(FORWARD)

    rightMotor.set_velocity(speedOfTravel, RPM)
    rightMotor.spin(FORWARD)

def handleLeft1Button():
    global current_state
    print('Left 1 Button Pressed')

    if(current_state == IDLE):
        print('IDLE -> FORWARD')
        current_state = DRVFWD
        
        drive()
        
    else:
        print(' -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()

def handleBumperG():
    global current_state
    global countNumTurns
    
    print('Bumper G Pressed')
    
    if(countNumTurns >= 3):
        print(' -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()
    
    elif(current_state == TURNRIGHT):
        print('TURNRIGHT -> FORWARD')
        current_state = DRVFWD
        
        drive()
    
    elif(current_state == DRVFWD):
        print('FORWARD -> IDLE')
        current_state = IDLE
        
    else:
        print('E-stop')

wasMoving = False
def checkMotionComplete():
    global wasMoving

    retVal = False

    isMoving = leftMotor.is_spinning() or rightMotor.is_spinning()

    if(wasMoving and not isMoving):
        retVal = True

    wasMoving = isMoving
    return retVal

def handleMotionComplete():
    global current_state
    global countNumTurns
    print("Handle Motion Complete")

    if(countNumTurns >= 3):
        print(' -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()

    elif(current_state == DRVFWD):
        print('FORWARD -> TURNRIGHT')
        current_state = TURNRIGHT
      
        turn("RIGHT")
    
    elif(current_state == TURNRIGHT):
        print('TURNRIGHT -> FORWARD')
        current_state = DRVFWD
        
        drive()
    
    elif(current_state == DRVFWD):
        print('FORWARD -> IDLE')
        current_state = IDLE


def checkDistanceTriggered():
    if (distanceSensor.distance(MM) < 225): #Check value for triggered
        return True
    return False

def handleDistanceTriggered():
    global current_state
    print("Distance Triggered")
    
    if(current_state == DRVFWD):
        print('FORWARD -> TURNRIGHT')
        current_state = TURNRIGHT
        
        leftMotor.stop()
        rightMotor.stop()
        print(countNumTurns)
      
        turn("RIGHT")
    handleMotionComplete()

controller.buttonL1.pressed(handleLeft1Button)

while True:
    if(checkMotionComplete()): handleMotionComplete()
    if(checkDistanceTriggered()): handleDistanceTriggered()