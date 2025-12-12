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
ai_vision_15 = AiVision(Ports.PORT15) 
#bumper_g = Bumper(brain.three_wire_port.g) #TODO: confirm 
leftLine = Line(brain.three_wire_port.a) 
rightLine = Line(brain.three_wire_port.b) 
rangeFinder = Sonar(brain.three_wire_port.e) 
claw = Motor(Ports.PORT5, GearSetting.RATIO_36_1, False) #Motor 57

speedOfTravel = 80 #RPM
speedOfRack = 20 #RPM
rackTravelHeight = 1 #Turns
speedOfClaw = 20 #RPM
moveClawDistance = 0.2 #Turns
turnDistance = 3.6 #Turns for 90 degree turn

def drive(direction, speed, turns):
    leftMotor.set_velocity(speed, RPM)
    leftMotor.spin_for(direction, turns, TURNS, wait = False)

    rightMotor.set_velocity(speed, RPM)
    rightMotor.spin_for(direction, turns, TURNS, wait = False)
    wait(5000, MSEC) #Wait for drive to complete
    
def rackMove(direction, speed, distance):
    rack1.set_velocity(speed, RPM)
    rack1.spin_for(direction, distance, TURNS, wait = False)

    rack2.set_velocity(speed, RPM)
    rack2.spin_for(direction, distance, TURNS, wait = False)

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

#States
IDLE = 0
GOTOAISLEROW = 1 #Goes to spcific tree (1 - 6)
GOTOSTAGE = 2 #Goes to specific heig
PICKFRUIT = 3 #Drives towards fruit and picks it
GOTOBINS = 4 #Based off of current aisle, goes to the bin area
DEPOSITFRUIT= 5 #Deposits fruit into correct bin
RETURNTOBASE = 6 #Returns to starting position from bin area

currentState = IDLE
toFruitDistance = 2.5 #Turns
fruitColor = "PURPLE" #GREEN, ORANGE, PURPLE
treeNum = 0
aisleRow = 22
arrivedAtLocation = False

rackLevel = 0
stageOne = 0 #Turns
stageTwo = 1.65 #Turns
rackHeight = 0 #Turns

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
    global aisleRow
    
    print("Button L1 Pressed")
    treeNum = 1
    rackLevel = 2    
    aisleRow = 11
    
    if(currentState == IDLE):
        print("IDLE --> GOTOTREE")
        currentState = GOTOAISLEROW
        
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
    global aisleRow
    aisleRow = 22
    rackLevel = 1
    
    print("Button L2 Pressed")
    treeNum = 4
    
    if(currentState == IDLE):
        print("IDLE --> GOTOAISLEROW")
        currentState = GOTOAISLEROW
        
        goToAisleRow()
    else:
        print(" --> IDLE")
        currentState = IDLE
        rightMotor.stop()
        leftMotor.stop()
        rack1.stop()
        rack2.stop()

# Define tree 1 stage 1
def handleRight2():
    global currentState
    global rackLevel
    global treeNum 
    global aisleRow
    
    print("Button R2 Pressed")
    treeNum = 1
    rackLevel = 1    
    aisleRow = 11
    
    if(currentState == IDLE):
        print("IDLE --> GOTOAISLEROW")
        currentState = GOTOAISLEROW
        
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
    
    if(currentState == GOTOAISLEROW):
        print("GOTOAISLEROW --> GOTOSTAGE")
        currentState = GOTOSTAGE
        
        goToStage(rackLevel)
    elif(currentState == GOTOSTAGE):
        print("GOTOSTAGE --> PICKFRUIT")
        currentState = PICKFRUIT
        
        pickFruit()
    elif(currentState == GOTOBINS):
        print("PICKFRUIT --> GOTOBINS")
        currentState = GOTOBINS
        
        goToBins()
    elif(currentState == PICKFRUIT):
        print("PICKFRUIT --> DEPOSITFRUIT")
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
    if(stageNum == 2):
        rackMove(FORWARD, speedOfRack, stageTwo)
        wait(5000, MSEC)
    handleMotionComplete()
    
#Returns rack to initial resting position  
def rackToTravel(stageNum):
    rackMove(REVERSE, speedOfRack, stageNum)

#Drive toward fruit from set position
def driveToFruit(direction):
    print("Driving to fruit")
    drive(direction, speedOfTravel, 2) #Adjust distance as needed
    wait(5000, MSEC)

#Returns rack to base to pick fruit
def pickFruit():
    clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
    wait(2000, MSEC)
    print("Driving")
    drive(FORWARD, speedOfTravel, 3.5)
    wait(5000, MSEC)
    print("Picking fruit")
    clawMove(REVERSE, speedOfClaw, moveClawDistance) #Close claw
    print("waiting")
    wait(3000, MSEC)
    print("Racking to travel")
    drive(REVERSE, speedOfTravel, 3.5)
    wait(5000, MSEC)
    if(rackLevel == 2):
        rackToTravel(stageTwo)
    handleMotionComplete()
  
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
    drive(FORWARD, speedOfTravel, 2.5) #Adjust distance as needed
    ninetyTurn("LEFT", speedOfTravel, turnDistance)

#TODO: Test/tune function
#Go to specific tree number
def goToTree(aisleRow):
    if(treeNum == 1):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance)
    elif(treeNum == 2):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 5) #Adjust distance as needed
        #lineTracking(300) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance)
    elif(treeNum == 3):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 10) #Adjust distance as needed
        #lineTracking(300) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance) 
    elif(treeNum == 4):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance)
        lineTracking(300) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
    elif(treeNum == 5):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance)
        lineTracking(100) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        lineTracking(500) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
    elif(treeNum == 6):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance)
        lineTracking(100) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        lineTracking(300) #Adjust distance as needed
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
    else:
        print("Invalid tree number")

#Get aisle and row from aisleRow number
def getAisleRow(aisleRowNum):
    return math.floor(aisleRowNum/10), aisleRowNum%10

#TODO: Test/Tune function
#Go to tree based off of aisle row
def goToAisleRow():
    aisle, row = getAisleRow(aisleRow)
    print("Aisle: ", aisle, " Row: ", row)
    if(aisle == 1):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 8.5)
        wait(5000, MSEC)
        goToRow(row)
    elif(aisle == 2):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 4) #Adjust distance as needed
        ninetyTurn("RIGHT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 22)
        wait(17000, MSEC)
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        goToRow(row)
    elif(aisle == 3):
        ninetyTurn("LEFT", speedOfTravel, turnDistance)
        drive(FORWARD, speedOfTravel, 1) #Adjust distance as needed
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
        goToRow(row)
    else:
        print("Invalid aisle number")

#TODO: Test/tune function
#Go to specific row in aisle
def goToRow(row):
    if(row == 1):
        leftMotor.set_velocity(speedOfTravel, RPM)
        leftMotor.spin_for(FORWARD, 3.65, TURNS, wait = False) #Adjust turns as needed

        rightMotor.set_velocity(speedOfTravel, RPM)
        rightMotor.spin_for(REVERSE, 3.65, TURNS, wait = False) #Adjust turns as needed
        wait(4000, MSEC)
        drive(FORWARD, speedOfTravel, 3)
        handleMotionComplete()
    elif(row == 2):
        drive(FORWARD, speedOfTravel, 2) 
        wait(2000, MSEC)
        handleMotionComplete()
    elif(row == 3):
        drive(FORWARD, speedOfTravel, 10) 
    elif(row == 4):
        drive(FORWARD, speedOfTravel, 15) 
    else:
        print("Invalid row number")

#TODO: Test/tune function
#Go to bin area based off of aisleRow
def goToBins():
    aisle, row = getAisleRow(aisleRow)
    
    while True:
        leftMotor.set_velocity(speedOfTravel, RPM)
        leftMotor.spin(FORWARD, wait = False)

        rightMotor.set_velocity(speedOfTravel, RPM)
        rightMotor.spin(FORWARD, wait = False)
        
        if(aisle == 1):
            if(checkDistanceSensing(1200) and  not checkDistanceSensing(300)): #Test this distance
                leftMotor.stop()
                rightMotor.stop()
                break
        elif(aisle == 2):
            if(checkDistanceSensing(800) and  not checkDistanceSensing(300)): #Test this distance
                leftMotor.stop()
                rightMotor.stop()
                break
        elif(aisle == 3):
            if(checkDistanceSensing(500) and  not checkDistanceSensing(300)): #Test this distance
                leftMotor.stop()
                rightMotor.stop()
                break
        else:
            print("Invalid aisle number")
            break
    
    while True:
        leftMotor.set_velocity(speedOfTravel, RPM)
        leftMotor.spin(FORWARD, wait = False)

        rightMotor.set_velocity(speedOfTravel, RPM)
        rightMotor.spin(FORWARD, wait = False)
        if(checkDistanceSensing(500)): #Test this distance
            leftMotor.stop()
            rightMotor.stop()
            break
        if(rightLine.value() > 2000 and leftLine.value() > 2000):
            leftMotor.stop()
            rightMotor.stop()
            break
    ninetyTurn("RIGHT", speedOfTravel, turnDistance)
    lineTracking(300) #Adjust distance as needed
    ninetyTurn("RIGHT", speedOfTravel, turnDistance)

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
        if(aisleRow == 11):
            ninetyTurn("RIGHT", speedOfTravel, turnDistance)
            wait(2500, MSEC)
            drive(FORWARD, speedOfTravel, 8) #Adjust distance as needed
            wait(4000, MSEC)
            ninetyTurn("LEFT", speedOfTravel, turnDistance)
            wait(2500, MSEC)
            drive(FORWARD, speedOfTravel, 4) #Adjust distance as needed
            wait(3500, MSEC)
            ninetyTurn("RIGHT", speedOfTravel, turnDistance)
            wait(2500, MSEC)
            drive(FORWARD, speedOfTravel, 3) #Adjust distance as needed
            wait(2500, MSEC)
            clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
            wait(2000, MSEC)
            drive(REVERSE, speedOfTravel, 2.75) #Adjust distance as needed
            clawMove(REVERSE, speedOfClaw, moveClawDistance) #Close claw
            wait(2500, MSEC)
        elif(aisleRow == 22):
            ninetyTurn("LEFT", speedOfTravel, turnDistance)
            wait(2500, MSEC)
            drive(FORWARD, speedOfTravel, 16) #Adjust distance as needed
            wait(15000, MSEC)
            ninetyTurn("LEFT", speedOfTravel, turnDistance)
            wait(2500, MSEC)
            drive(FORWARD, speedOfTravel, 7) #Adjust distance as needed
            wait(3500, MSEC)
            clawMove(FORWARD, speedOfClaw, moveClawDistance) #Open claw
            wait(2000, MSEC)
            drive(REVERSE, speedOfTravel, 2.75) #Adjust distance as needed
            clawMove(REVERSE, speedOfClaw, moveClawDistance) #Close claw
            wait(2500, MSEC)
        handleMotionComplete()
    else:
        print("Invalid fruit color")

#Line tracking function with proportional control
def lineTracking(distanceFrom):
    Kp = 30.0  # Proportional gain, adjust as needed
    print("Starting line tracking")
    while True:
        leftDetected = leftLine.value() > 2000  # Adjust threshold as needed (0-100)
        rightDetected = rightLine.value() > 2000        
        # Calculate error: positive = too far right, negative = too far left
        if leftDetected and rightDetected:
            error = 0
            
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
        if(checkDistanceSensing(distanceFrom)):
            leftMotor.stop()
            rightMotor.stop()
            break

#Distance tracking function
#Distance less than distanceFrommm returns True
def checkDistanceSensing(distanceFrom):
    if(rangeFinder.distance(DistanceUnits.MM) < distanceFrom):
        return True
    else:
        return False
    
#Open and close claw function
#Forward --> open, Reverse --> close
def clawMove(direction, speed, distance):
    claw.set_velocity(speed, RPM)
    claw.spin_for(direction, distance, TURNS, wait = False)

#Use the camera to return the color being detected
#Three colors: green, orange, and purple
ai_vision_15_green = Colordesc(1, 114, 247, 118, 10, 0.2)
ai_vision_15_orange = Colordesc(2, 232, 143, 125, 10, 0.2)
ai_vision_15_purple = Colordesc(3, 181, 135, 217, 10, 0.2)
def getColorFromCamera():
    #detectedObjects = ai_vision_15.largest_object()
    if(ai_vision_15.take_snapshot(ai_vision_15_green)):
        return "GREEN"
    elif(ai_vision_15.take_snapshot(ai_vision_15_orange)):
        return "ORANGE"
    elif(ai_vision_15.take_snapshot(ai_vision_15_purple)):
        return "PURPLE"
    else:
        return None

#Center robot to camera object
def centerRobotToCameraObject():
    if(ai_vision_15.largest_object().exists):
        cx = ai_vision_15.largest_object().centerX
        cy = ai_vision_15.largest_object().centerY

    target_x = 160
    K_x = 0.2

    #centering the fruit
    error = cx - target_x
    turn_effort = K_x * error

    while (ai_vision_15.largest_object().width < 160 or ai_vision_15.largest_object().height < 160):
        leftMotor.spin(FORWARD, 20 - turn_effort)
        rightMotor.spin(FORWARD, 20 + turn_effort)
    leftMotor.stop()
    rightMotor.stop()

#For testing individual functions
def handleRight1():
    print("Button R1 Pressed")
    #goToAisleRow()
    #goToStage(1)
    #wait(5000, MSEC)
    #rackToTravel(stageTwo)
    #pickFruit()
    #depositFruit()
    #centerRobotToCameraObject()
    while True:
        color = getColorFromCamera()
        print(color)
        wait(1000, MSEC)
    
controller.buttonL1.pressed(handleLeft1)
controller.buttonL2.pressed(handleLeft2)
controller.buttonR1.pressed(handleRight1)
controller.buttonR2.pressed(handleRight2)

while True:
    pass
    #if(checkMotionComplete()): 
       # handleMotionComplete()