from vex import *

brain = Brain()

imu = Inertial(Ports.PORT9)

while(True):
    print(imu.rotation())