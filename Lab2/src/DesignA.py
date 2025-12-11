from vex import *

brain = Brain()
controller = Controller()

leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
left_sensor = Line(brain.three_wire_port.b)
right_sensor = Line(brain.three_wire_port.a)
distanceSensor = Sonar(brain.three_wire_port.e)

countNumTurns = 0

distanceOfTravel = 2 # in rotations
speedOfTravel = 30 # in RPM

#States
IDLE = 0
LINEFOLLOWING = 1
TURNING = 2

current_state = IDLE

def turn(direction):
    if direction == "LEFT":
        leftMotor.spin_for(FORWARD, 7, TURNS, 50, RPM)
    elif direction == "RIGHT":
        rightMotor.spin_for(FORWARD, 7, TURNS, 50, RPM)

Kp = .8

def handleSonarTimer():
    if(current_state == LINEFOLLOWING):
        '''
        if (right_sensor.reflectivity() > 10):
            right = 1
        else:
            right = 0
        if (left_sensor.reflectivity() > 10):
            left = 1
        else:
            left = 0
            '''
        right = right_sensor.reflectivity()
        left = left_sensor.reflectivity()

        print(right, left)

        distance_error = right - left

        driving_effort = Kp * distance_error
        print(driving_effort)

        base_speed = 100
        
        leftMotor.set_velocity(base_speed - driving_effort, RPM)
        leftMotor.spin(FORWARD)

        rightMotor.set_velocity(base_speed + driving_effort, RPM)
        rightMotor.spin(FORWARD)

    sonarTimer.event(handleSonarTimer, 50)

sonarTimer = Timer()

def handleLeft1Button():
    global current_state
    print('Left 1 Button Pressed')

    if(current_state == IDLE):
        print('IDLE -> LINEFOLLOWING')
        current_state = LINEFOLLOWING
        
        sonarTimer.event(handleSonarTimer, 50)
        
    else:
        print(' -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()

def handleBumperG():
    global current_state
    global countNumTurns

    if(current_state == LINEFOLLOWING and countNumTurns >= 3):
        print('LINEFOLLOWING -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()
    
    elif(current_state == LINEFOLLOWING):
        print('LINEFOLLOWING -> TURNING')
        current_state = TURNING
      
        turn("RIGHT")
    
    elif(current_state == TURNING):
        print('TURNING -> LINEFOLLOWING')
        current_state = LINEFOLLOWING   
        
        sonarTimer.event(handleSonarTimer, 50)
        countNumTurns += 1
        
    else:
        print('E-stop')

wasMoving = False
def checkMotionComplete():
    global wasMoving

    if current_state == IDLE:
        return

    retVal = False

    isMoving = leftMotor.is_spinning() or rightMotor.is_spinning()

    if(wasMoving and not isMoving):
        retVal = True

    wasMoving = isMoving
    return retVal

def handleMotionComplete():
    global current_state
    global countNumTurns

    if current_state == IDLE:
        return

    if(current_state == LINEFOLLOWING and countNumTurns >= 3):
        print('LINEFOLLOWING -> IDLE')
        current_state = IDLE
        leftMotor.stop()
        rightMotor.stop()

    elif(current_state == LINEFOLLOWING):
        print('LINEFOLLOWING -> TURNING')
        current_state = TURNING 
      
        turn("RIGHT")
    
    elif(current_state == TURNING):
        print('TURNING -> LINEFOLLOWING')
        current_state = LINEFOLLOWING   
        
        sonarTimer.event(handleSonarTimer, 50)
        countNumTurns += 1
        
    else:
        print('E-stop')


def checkDistanceTriggered():
    if (distanceSensor.distance(MM) < 225): #Check value for triggered
        return True
    return False

def handleDistanceTriggered():
    global current_state
    global countNumTurns
    
    if(current_state == LINEFOLLOWING):
        print('LINEFOLLOWING -> TURNING')
        current_state = TURNING
      
        leftMotor.stop()
        rightMotor.stop()
        turn("RIGHT")
        countNumTurns += 1
    handleMotionComplete()

controller.buttonL1.pressed(handleLeft1Button)

while True:
    #if(checkMotionComplete()): handleMotionComplete()
    if(checkDistanceTriggered()): handleDistanceTriggered()