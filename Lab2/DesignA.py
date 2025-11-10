from vex import *

brain = Brain()
controller = Controller()

leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
distanceSensor = Sonar(Ports.PORT9)#Check port number

countNumTurns = 0

distanceOfTravel = 2 # in rotations
speedOfTravel = 30 # in RPM

#States
IDLE = 0
DRVFWD = 1
TURNRIGHT = 2
TURNLEFT = 3

currentState = IDLE

def turn(direction):
    if direction == "RIGHT":
        leftMotor.spin_for(FORWARD, 0.5, TURNS, 50, RPM)
    elif direction == "LEFT":
        rightMotor.spin_for(FORWARD, 0.5, TURNS, 50, RPM)

Kp = 10

def handleSonarTimer():
    if(currentState == DRVFWD):
        distance = distanceSensor.distance(MM) / 10
        print(distance)

        distance_error = 10 - distance

        driving_effort = Kp * distance_error
        
        leftMotor.spin(FORWARD, driving_effort, RPM)
        rightMotor.spin(FORWARD, driving_effort, RPM)

    sonarTimer.event(handleSonarTimer, 50)

sonarTimer = Timer()

def handleLeft1Button():
    global current_state
    print('Left 1 Button Pressed')

    if(current_state == IDLE):
        print('IDLE -> FORWARD')
        current_state = DRVFWD
        
        sonarTimer.event(handleSonarTimer, 50)
        
    else:
        print(' -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()

def handleBumperG():
    global current_state
    global countNumTurns

    if(current_state == DRVFWD and countNumTurns < 3):
        print('FORWARD -> TURNRIGHT')
        current_state = TURNRIGHT
      
        turn("RIGHT")
    
    elif(current_state == TURNRIGHT):
        print('TURNRIGHT -> FORWARD')
        current_state = DRVFWD
        
        sonarTimer.event(handleSonarTimer, 50)
        countNumTurns += 1

    elif(current_state == TURNLEFT):
        print('TURNLEFT -> FORWARD')
        current_state = DRVFWD
        
        turn("LEFT")
    
    elif(current_state == DRVFWD and countNumTurns >= 3):
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

    if(current_state == DRVFWD and countNumTurns < 3):
        print('FORWARD -> TURNRIGHT')
        current_state = TURNRIGHT
      
        turn("RIGHT")
    
    elif(current_state == TURNRIGHT):
        print('TURNRIGHT -> FORWARD')
        current_state = DRVFWD
        
        sonarTimer.event(handleSonarTimer, 50)
        countNumTurns += 1

    elif(current_state == TURNLEFT):
        print('TURNLEFT -> FORWARD')
        current_state = DRVFWD
        
        turn("LEFT")
    
    elif(current_state == DRVFWD and countNumTurns >= 3):
        print('FORWARD -> IDLE')
        current_state = IDLE
        
    else:
        print('E-stop')


def checkDistanceTriggered():
    if distanceSensor.distance(MM) < 10: #Check value for triggered
        return True
    return False

def handleReflectanceTriggered():
    global current_state
    global countNumTurns
    
    if(current_state == DRVFWD and countNumTurns < 3):
        print('FORWARD -> TURNRIGHT')
        current_state = TURNRIGHT
      
        turn("RIGHT")
    
    elif(current_state == TURNRIGHT):
        print('TURNRIGHT -> FORWARD')
        current_state = DRVFWD
        
        sonarTimer.event(handleSonarTimer, 50)
        countNumTurns += 1

    elif(current_state == TURNLEFT):
        print('TURNLEFT -> FORWARD')
        current_state = DRVFWD
        
        turn("LEFT")
    
    elif(current_state == DRVFWD and countNumTurns >= 3):
        print('FORWARD -> IDLE')
        current_state = IDLE
        
    else:
        print('E-stop')

controller.buttonL1.pressed(handleLeft1Button)

while True:
    if(checkMotionComplete()): handleMotionComplete()
    if(checkDistanceTriggered()): handleReflectanceTriggered()