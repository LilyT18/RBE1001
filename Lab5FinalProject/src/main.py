# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       lilyt                                                        #
# 	Created:      12/8/2025, 1:12:05 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

rightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False) #TODO: find motor #
leftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True) #TODO: find motor #
controller = Controller()
rack1 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, False) #Motor 58
rack2 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, True) #Motor 59
ai_vision_15__Red_Folder = Colordesc(1, 222, 31, 63, 11, 0.48) #TODO: figure out what this means
ai_vision_15 = AiVision(Ports.PORT15, ai_vision_15__Red_Folder) #TODO: confirm port
bumper_g = Bumper(brain.three_wire_port.g) #TODO: confirm port

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
IDENTIFYCORRECTBIN = 2 #Uses camera to detect color of bin and match it with the fruit
PICKFRUIT = 3 #Drives towards fruit and picks it
GOTOISLE = 4 #Goes to spcific aisle (1, 2, or 3)
GOTOBINS = 5 #Based off of current aisle, goes to the bin area
DEPOSITFRUIT= 6 #Deposits fruit into correct bin
RETURNTOBASE = 7 #Returns to starting position from bin area

currentState = IDLE
rackLevel = 0
levelOne = .75 #Turns
levelTwo = 2 #Turns
toFruitDistance = 2.5 #Turns

#Used to detect motion completion
wasMoving = False
def checkMotionComplete():
    global wasMoving

    retVal = False

    isMoving = leftMotor.is_spinning() or rightMotor.is_spinning() or rack1.is_spinning() or rack2.is_spinning()

    if(wasMoving and not isMoving):
        retVal = True

    wasMoving = isMoving
    return retVal

#TODO: complete handle
# Define stage 1
def handleLeft1():
    global currentState
    global rackLevel
    
    pass

#TODO: complete handle
# Define stage 2
def handleLeft2():
    global currentState
    global rackLevel
    
    pass

#TODO: Goes to next state after motion is complete
def handleMotionComplete():
    global currentState
    pass

        
def goToStage(stageNum):
    global currentState
    #Need to adjust distance values for different stages
    if(stageNum == 1):
        rackMove(FORWARD, speedOfRack, levelOne)
    elif(stageNum == 2):
        rackMove(FORWARD, speedOfRack, levelTwo)
    
#Returns rack to initial resting position  
def returnRackToBase(stageNum):
    pass

#Drive toward fruit from set position
def driveToFruit(direction):
    drive(direction, speedOfTravel, toFruitDistance) #Adjust distance as needed

#Returns rack to base to pick fruit
def pickFruit():
    returnRackToBase(rackLevel)
  
#TODO: Needs completed
#Go back to rack position after depositing fruit  
def returnRobotToBase():
    pass

#TODO: Check if code works and test to make sure it works
#Ilakkiya this is yourssssss
#You'll need to check the ports of the camera 
def getColorFromCamera():
    detectedObjects = ai_vision_15.largest_object()
    if(detectedObjects.exists):
        return detectedObjects.color
    else:
        return None

#TODO: Ilakkiya this is also yoursssss
#Center robot to camera object
def centerRobotToCameraObject():
    pass

controller.buttonL1.pressed(handleLeft1)
controller.buttonL2.pressed(handleLeft2)

while True:
    if(checkMotionComplete()): 
        handleMotionComplete()