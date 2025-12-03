# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       lilyt                                                        #
# 	Created:      12/2/2025, 2:36:19 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

rightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
controller = Controller()
rack1 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, False) #Motor 58
rack2 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, True) #Motor 59

speedOfTravel = 80 #RPM
speedOfRack = 50 #RPM

def drive(direction, speed, turns):
    leftMotor.set_velocity(speed, RPM)
    leftMotor.spin_for(direction, turns, TURNS, wait = False)

    rightMotor.set_velocity(speed, RPM)
    rightMotor.spin_for(direction, turns, TURNS, wait = False)
    
def rackMove(direction, speed, distance):
    rack1.set_velocity(speed, RPM)
    rack1.spin_for(direction, distance, TURNS, wait = False)

    rack2.set_velocity(speed, RPM)
    rack2.spin_for(direction, distance, TURNS, wait = False)

#States
IDLE = 0
GOTOSTAGE = 1 #Goes to specific height
DRIVETOFRUIT = 2
PICKFRUIT = 3 #Drives towards fruit and picks it

currentState = IDLE
rackLevel = 0
levelOne = .75 #Turns
levelTwo = 2 #Turns
driveDistance = 2.5 #Turns

wasMoving = False
def checkMotionComplete():
    global wasMoving

    retVal = False

    isMoving = leftMotor.is_spinning() or rightMotor.is_spinning() or rack1.is_spinning() or rack2.is_spinning()

    if(wasMoving and not isMoving):
        retVal = True

    wasMoving = isMoving
    return retVal

#Define stage 1
def handleLeft1():
    global currentState
    global rackLevel
    
    if(currentState == IDLE):
        print("IDLE -> GOTOSTAGE")
        currentState = GOTOSTAGE
        rackLevel = 1
        goToStage(1)
    else: 
        print(' -> IDLE')
        currentState = IDLE
        leftMotor.stop()
        rightMotor.stop()

#Define stage 2
def handleLeft2():
    global currentState
    global rackLevel
    
    if(currentState == IDLE):
        print("IDLE -> GOTOSTAGE")
        currentState = PICKFRUIT
        rackLevel = 2
        goToStage(2)
    else: 
        print(' -> IDLE')
        currentState = IDLE
        leftMotor.stop()
        rightMotor.stop()

def handleMotionComplete():
    global currentState

    if(currentState == GOTOSTAGE):
        print(' -> DRIVETOFRUIT')
        currentState = DRIVETOFRUIT
        driveToFruit(REVERSE)
    elif(currentState == DRIVETOFRUIT):
        print(' -> PICKFRUIT')
        currentState = PICKFRUIT
        pickFruit()
    elif(currentState == PICKFRUIT):
        print(' -> IDLE')
        currentState = IDLE
        
def goToStage(stageNum):
    global currentState
    #Need to adjust distance values for different stages
    if(stageNum == 1):
        rackMove(FORWARD, speedOfRack, levelOne)
    elif(stageNum == 2):
        rackMove(FORWARD, speedOfRack, levelTwo)
        
def returnRackToBase(stageNum):
    global currentState
    #Need to adjust distance values for different stages
    if(stageNum == 1):
        rackMove(REVERSE, speedOfRack, levelOne)
    elif(stageNum == 2):
        rackMove(REVERSE, speedOfRack, levelTwo)

def driveToFruit(direction):
    drive(direction, speedOfTravel, driveDistance) #Adjust distance as needed

def pickFruit():
    returnRackToBase(rackLevel)
    #drive(FORWARD, speedOfTravel, driveDistance) #Adjust distance as needed
    
controller.buttonL1.pressed(handleLeft1)
controller.buttonL2.pressed(handleLeft2)

while True:
    if(checkMotionComplete()): 
        handleMotionComplete()