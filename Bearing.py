import sys
import time 
import csv
import math
import array 
from Phidget22.Devices.Spatial import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from cmath import *
#from SpatialTry import *

lastAngles = [0,0,0]

try:
    ch = Spatial()
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

def SpatialAttached(e):
    try:
        attached = e
        attached.resetMagnetometerCorrectionParameters()
        attached.setMagnetometerCorrectionParameters(0.36341, 0.09927, 0.11774, -0.07688,  2.66012, 2.56018, 3.03476, 0.01156, -0.07656, 0.00600, 0.06844, -0.05628, 0.07447)
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")
        
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   

def SpatialDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

"""
Contains data for acceleration/gyro/compass depending on what the board supports, as well as a timestamp.
This event is fired at a fixed rate as determined by the DataRate property.
"""

lastAngles = [0,0,0]

def calculateCompassBearing(e, acceleration, angularRate, fieldStrength, timestamp):
#write the data into a file
    gravity = [acceleration[0], acceleration[1], acceleration[2]]
    magField = [fieldStrength[0], fieldStrength[1], fieldStrength[2]]
   
    rollAngle = math.atan2(gravity[1], gravity[2]);
   # print("Roll angle : %s" % rollAngle)

    pitchAngle = math.atan(-gravity[0] / (gravity[1] * math.sin(rollAngle) + gravity[2] * math.cos(rollAngle)));
    #print("Pitch angle : %s" % rollAngle)

    yawAngle = math.atan2(magField[2] * math.sin(rollAngle) - magField[1] * math.cos(rollAngle),
        magField[0] * math.cos(pitchAngle) + magField[1] * math.sin(pitchAngle) * math.sin(rollAngle) + magField[2] * math.sin(pitchAngle) * math.cos(rollAngle));
    #print("Yaw angle : %s" % rollAngle)

    angles = [rollAngle, pitchAngle, yawAngle]

    compassBearing = yawAngle * (180.0 / math.pi);
  
    print("Bearing before: %s" % compassBearing)

    compassBearingFilter = [[0,0,0]]

    Count = len(compassBearingFilter)
    
    compassBearingFilterSize = 10

    try:
        for i in range(0,3,2):
            if math.fabs(angles[i]-lastAngles[i]) > 3:
                print("TEST")
                for value in compassBearingFilter:
                    if angles[i] > lastAngles[i]:
                        value[i] += 360 * math.pi/180.0
                    else:
                        value[i] -= 360 * math.pi/180.0

        for i in range(len(lastAngles)):
            lastAngles[i] = angles[i]

        compassBearingFilter.append(lastAngles)
        if Count > compassBearingFilterSize:
            compassBearingFilter.pop(0)

        yawAngle = pitchAngle = rollAngle = 0

        for l in range(len(compassBearingFilter)):
            rollAngle += compassBearingFilter[l][0]
            pitchAngle += compassBearingFilter[l][1]
            yawAngle += compassBearingFilter[l][2]
        
        yawAngle /= Count
        pitchAngle /= Count
        rollAngle /= Count

        compassBearing = yawAngle * (180.0 / math.pi)
        print("Bearing after: %s" % compassBearing)

    except:
        print()
  #  print("Field Strength: %7.3f  %8.3f  %8.3f" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))
    
try:
    ch.setOnAttachHandler(SpatialAttached)
    ch.setOnDetachHandler(SpatialDetached)
    ch.setOnErrorHandler(ErrorEvent)
    ch.setOnSpatialDataHandler(calculateCompassBearing)
   
    print("Waiting for the Phidget Spatial Object to be attached...")

    #file.write("\n")

    ch.openWaitForAttachment(5000)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

print("Gathering data for 10 seconds...")
time.sleep(10)

try:
    ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(2)
    exit(1) 
print("Closed Spatial device")
exit(0)


"""

for value in compassBearingFilter:
                    if angles[i] > lastAngles[i]:
                        value[i] += 360 * math.pi / 180.0 
                    else:
                        value[i] -= 360 * math.pi / 180.0 

"""
