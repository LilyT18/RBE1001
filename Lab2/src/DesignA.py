from vex import *

brain = Brain()
controller = Controller()

leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
left_sensor = Line(brain.three_wire_port.b)
right_sensor = Line(brain.three_wire_port.a)

countNumTurns = 0

distanceOfTravel = 2 # in rotations
speedOfTravel = 30 # in RPM

#States
IDLE = 0
DRVFWD = 1
TURNRIGHT = 2
TURNLEFT = 3

current_state = DRVFWD

def turn(direction):
    if direction == "RIGHT":
        leftMotor.spin_for(FORWARD, 0.5, TURNS, 50, RPM)
    elif direction == "LEFT":
        rightMotor.spin_for(FORWARD, 0.5, TURNS, 50, RPM)

Kp = 10

def handleSonarTimer():
    if(current_state == DRVFWD):
        if (right_sensor.reflectivity() > 1500):
            right = 1
        else:
            right = 0
        if (left_sensor.reflectivity() > 1500):
            left = 1
        else:
            left = 0

        print(right, left)

        distance_error = left - right

        driving_effort = Kp * distance_error
        print(driving_effort)

        base_speed = 200
        
        leftMotor.spin(FORWARD, base_speed - driving_effort, RPM)
        rightMotor.spin(FORWARD, base_speed + driving_effort, RPM)

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
    if (right_sensor.reflectivity() < 1500 and left_sensor.reflectivity() < 1500): #Check value for triggered
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