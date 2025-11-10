from vex import *

brain=Brain()
lineSensor = Line(brain.three_wire_port.a)

while(True):
    print(lineSensor.reflectivity())