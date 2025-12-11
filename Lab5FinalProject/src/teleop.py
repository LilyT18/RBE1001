# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       lilyt                                                        #
# 	Created:      12/8/2025, 1:12:05 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Bin1 - Green
# Bin2 - Orange
# Bin3 - Purple

# Field Layout
# NOT DRAWN TO SCALE
# ----------------------------------------------------------------- #
#  Robot  |                                                         #
#  Start  |                                                         #
# ---------                                                         #
# 	               _____          _____          _____              #
# -------	      |Tree |        |Tree |        |Tree |             #
# 	Bin |         |  1  |        |  2  |        |  3  |             #
# 	 3  |          -----          -----          -----              #
# -------	                                                        #
# 	Bin |                                                           #
# 	 2  |          _____          _____          _____              #
# -------	      |Tree |        |Tree |        |Tree |             #
#   Bin |         |  4  |        |  5  |        |  6  |             #
#    1  |          -----          -----          -----              # 
# -------                                                           #
#                                                                   #
# ----------------------------------------------------------------- #



from vex import *

# Brain should be defined by default
brain = Brain()

rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False) #Motor 64
leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True) #Motor 63
controller = Controller()
rack1 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False) #Motor 59
rack2 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True) #Motor 58
ai_vision_15__Red_Folder = Colordesc(1, 222, 31, 63, 11, 0.48) #TODO: figure out what this means
ai_vision_15 = AiVision(Ports.PORT15, ai_vision_15__Red_Folder) 
#bumper_g = Bumper(brain.three_wire_port.g) #TODO: confirm 
leftLine = Line(brain.three_wire_port.a) 
rightLine = Line(brain.three_wire_port.b) 
rangeFinder = Sonar(brain.three_wire_port.e) 
claw = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False) #Motor 57

speedOfTravel = 80 #RPM
speedOfRack = 30 #RPM
rackTravelHeight = 1 #Turns
speedOfClaw = 20 #RPM
moveClawDistance = 0.5 #Turns
turnDistance = 3.65

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
GOTOTREE = 1 #Goes to spcific tree (1 - 6)
GOTOSTAGE = 2 #Goes to specific heig
PICKFRUIT = 3 #Drives towards fruit and picks it
GOTOBINS = 4 #Based off of current aisle, goes to the bin area
DEPOSITFRUIT= 5 #Deposits fruit into correct bin
RETURNTOBASE = 6 #Returns to starting position from bin area

currentState = IDLE
toFruitDistance = 2.5 #Turns
fruitColor = None
treeNum = 0
aisleRow = 12
arrivedAtLocation = False

rackLevel = 0
stageOne = .75 #Turns
stageTwo = 2 #Turns
rackHeight = 0 #Turns

def handleRight1():
    print("Button R1 Pressed")
    goToAisleRow()

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

# Define tree 1 stage 2
def handleLeft1():
    global currentState
    global rackLevel
    global treeNum 
    
    print("Button L1 Pressed")
    treeNum = 1
    
    if(currentState == IDLE):
        print("IDLE --> GOTOTREE")
        currentState = GOTOTREE
        
        goToAisleRow()
    else:
        print(" --> IDLE")
        currentState = IDLE
        rightMotor.stop()
        leftMotor.stop()
        rack1.stop()
        rack2.stop()

# Define tree 4 stage 1
def handleLeft2():
    global currentState
    global rackLevel
    global treeNum
    
    print("Button L2 Pressed")
    treeNum = 4
    
    if(currentState == IDLE):
        print("IDLE --> GOTOTREE")
        currentState = GOTOTREE
        
        goToAisleRow()
    else:
        print(" --> IDLE")
        currentState = IDLE
        rightMotor.stop()
        leftMotor.stop()
        rack1.stop()
        rack2.stop()

#Goes to next state after motion is complete
def handleMotionComplete():
    global currentState
    
    if(currentState == GOTOTREE):
        print("GOTOTREE --> GOTOSTAGE")
        currentState = GOTOSTAGE
        
        goToStage(rackLevel)
    elif(currentState == GOTOSTAGE):
        print("GOTOSTAGE --> PICKFRUIT")
        currentState = PICKFRUIT
        
        pickFruit()
    elif(currentState == PICKFRUIT):
        print("PICKFRUIT --> GOTOBINS")
        currentState = GOTOBINS
        
        goToBins()
    elif(currentState == GOTOBINS):
        print("GOTOBINS --> DEPOSITFRUIT")
        currentState = DEPOSITFRUIT
        
        depositFruit()
    elif(currentState == DEPOSITFRUIT):
        print("DEPOSITFRUIT --> RETURNTOBASE")
        currentState = RETURNTOBASE
        
        returnRobotToBase()
    else:
        print(" --> IDLE")
        currentState = IDLE
        rightMotor.stop()
        leftMotor.stop()    
        rack1.stop()
        rack2.stop()
    
#Go to specific stage height 
def goToStage(stageNum):
    global currentState
    if(stageNum == 1):
        rackMove(FORWARD, speedOfRack, stageOne)
    elif(stageNum == 2):
        rackMove(FORWARD, speedOfRack, stageTwo)
    
#Returns rack to initial resting position  
def rackToTravel():
    global rackHeight
    temprack = rackHeight - rackTravelHeight
    
    rackMove(REVERSE, speedOfRack, temprack)
    rackHeight = rackTravelHeight

#Drive toward fruit from set position
def driveToFruit(direction):
    drive(direction, speedOfTravel, toFruitDistance) #Adjust distance as needed

#Returns rack to base to pick fruit
def pickFruit():
    clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
    centerRobotToCameraObject() #Ilakkiya's portion
    driveToFruit(FORWARD)
    clawMove(REVERSE, speedOfClaw, moveClawDistance) #Close claw
    rackToTravel()
  
#TODO: Test/tune function
#Go back to initial position after depositing fruit  
def returnRobotToBase():
    ninetyTurn("RIGHT", speedOfTravel, turnDistance)
    while True:
        rightMotor.set_velocity(speedOfTravel, RPM)
        leftMotor.set_velocity(speedOfTravel, RPM)
        rightMotor.spin(FORWARD)
        leftMotor.spin(FORWARD)
        if(checkDistanceSensing(300)): #Test this distance
            rightMotor.stop()
            leftMotor.stop()
            break
    ninetyTurn("LEFT", speedOfTravel, turnDistance)
    drive(FORWARD, speedOfTravel, 2) #Adjust distance as needed
    ninetyTurn("LEFT", speedOfTravel, turnDistance)


def getAisleRow(aisleRowNum):
    return aisleRowNum/10, aisleRowNum%10

#TODO: Test/Tune function
#Go to tree based off of aisle row
def goToAisleRow():
    aisle, row = getAisleRow(aisleRow)
    if(aisle == 1):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        goToRow(row)
    elif(aisle == 2):
        lineTracking(1000)
        wait(10000, MSEC)
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        goToRow(row)
    elif(aisle == 3):
        lineTracking(1500)
        drive(FORWARD, speedOfTravel, 3)
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        goToRow(row)
    else:
        print("Invalid aisle number")

#TODO: Test/tune function
#Go to specific row in aisle
def goToRow(row):
    if(row == 1):
        lineTracking(350)
    elif(row == 2):
        lineTracking(1300)
    elif(row == 3):
        lineTracking(2400) 
    elif(row == 4):
        lineTracking(3450) 
    else:
        print("Invalid row number")

#TODO: Test/tune function
#Go to bin area based off of aisleRow
def goToBins():
    pass

#TODO: Test/Tune function
#Deposit fruit into correct bin based off of fruitColor
def depositFruit():
    if(fruitColor == "GREEN"):
        drive(FORWARD, speedOfTravel, 2) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
        drive(REVERSE, speedOfTravel, 1) #Adjust distance as needed
    elif(fruitColor == "ORANGE"):
        drive(FORWARD, speedOfTravel, 4) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
        drive(REVERSE, speedOfTravel, 1) #Adjust distance as needed
    elif(fruitColor == "PURPLE"):
        drive(FORWARD, speedOfTravel, 6) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
        drive(REVERSE, speedOfTravel, 1) #Adjust distance as needed
    else:
        print("Invalid fruit color")

#Line tracking function with proportional control
def lineTracking(distanceFrom):
    Kp = 30.0  # Proportional gain, adjust as needed
    
    while True:
        leftDetected = leftLine.value() > 2000  # Adjust threshold as needed (0-100)
        rightDetected = rightLine.value() > 2000        
        # Calculate error: positive = too far right, negative = too far left
        if leftDetected and rightDetected:
            error = 0
            leftMotor.set_velocity(speedOfTravel, RPM)
            rightMotor.set_velocity(speedOfTravel, RPM)
            
        elif leftDetected and not rightDetected:
            error = 1
            
        elif not leftDetected and rightDetected:
            error = -1
            
        else:
            leftMotor.stop()
            rightMotor.stop()
            break
        
        correction = Kp * error
        
        leftMotorSpeed = speedOfTravel - correction
        rightMotorSpeed = speedOfTravel + correction
        
        leftMotor.set_velocity(leftMotorSpeed, RPM)
        rightMotor.set_velocity(rightMotorSpeed, RPM)
        
        leftMotor.spin(FORWARD)
        rightMotor.spin(FORWARD)
        
        wait(10, MSEC)
        if(checkDistanceSensing(distanceFrom)):
            leftMotor.stop()
            rightMotor.stop()
            break

#Distance tracking function
#Distance less than distanceFrommm returns True
def checkDistanceSensing(distanceFrom):
    if(rangeFinder.distance(DistanceUnits.MM) > distanceFrom):
        return True
    else:
        return False

#90 degree turn function
def ninetyTurn(direction, speed, distance):
    if(direction == "RIGHT"):
        print("Turning RIGHT")
        leftMotor.set_velocity(speed, RPM)
        leftMotor.spin_for(FORWARD, distance, TURNS, wait = False) #Adjust turns as needed

        rightMotor.set_velocity(speed, RPM)
        rightMotor.spin_for(REVERSE, distance, TURNS, wait = False) #Adjust turns as needed
    elif(direction == "LEFT"):
        leftMotor.set_velocity(speed, RPM)
        leftMotor.spin_for(REVERSE, distance, TURNS, wait = False) #Adjust turns as needed

        rightMotor.set_velocity(speed, RPM)
        rightMotor.spin_for(FORWARD, distance, TURNS, wait = False) #Adjust turns as needed
    else:
        print("Invalid turn direction")
    wait(5000, MSEC) #Wait for turn to complete

#Open and close claw function
#Forward --> open, Reverse --> close
def clawMove(direction, speed, distance):
    claw.set_velocity(speed, RPM)
    claw.spin_for(direction, distance, TURNS, wait = True)

#TODO: Check if code works and test to make sure it works
#Ilakkiya this is yourssssss
#You'll need to check the ports of the camera 
#Use the camera to return the color being detected
#Three colors: green, orange, and purple
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
#For testing individual functions

controller.buttonL1.pressed(handleLeft1)
controller.buttonL2.pressed(handleLeft2)
controller.buttonR1.pressed(handleRight1)