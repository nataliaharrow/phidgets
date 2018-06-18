import sys
import time 
from Phidget22.Devices.Spatial import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

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
        e.setCompassCorrectionParameters(self, 0.36341, 0.09927, 0.11774, -0.07688,  2.66012, 2.56018, 3.03476, 0.01156, -0.07656, 0.00600, 0.06844, -0.05628, 0.07447)
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
def SpatialDataHandler(e, acceleration, angularRate, fieldStrength, timestamp):
#write the data into a file
    
    file = open("calibrated.txt", "a")
    file.write("Field Strength: %7.3f  %8.3f  %8.3f \n" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))
    #file.write("\n")

   # filePlot = open("plotNorthSteadyX.txt", "a")
   # filePlot.write("%7.3f" % (fieldStrength[0]))

    print("Field Strength: %7.3f  %8.3f  %8.3f" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))

    #file.close()
    #stop writing data
    # print("Acceleration  : %7.3f  %8.3f  %8.3f" % (acceleration[0], acceleration[1], acceleration[2]))
    # print("Angular Rate  : %7.3f  %8.3f  %s8.3f" % (angularRate[0], angularRate[1], angularRate[2]))
    # print("Field Strength: %7.3f  %8.3f  %8.3f" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))
    # print("Timestamp: %f\n" % timestamp)

try:
    ch.setOnAttachHandler(SpatialAttached)
    ch.setOnDetachHandler(SpatialDetached)
    ch.setOnErrorHandler(ErrorEvent)
    ch.setOnSpatialDataHandler(SpatialDataHandler)

    print("Waiting for the Phidget Spatial Object to be attached...")
 #line to clea the file:   open("northToWest.txt", 'w').close()

    file = open("calibrated.txt", "a")
    file.write("--------------------------------------------")
    #file.write("\n")

    #filePlot = open("plotNorthSteadyX.txt", "a")

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

