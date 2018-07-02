import sys
import time 
import csv
from Phidget22.Devices.Spatial import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from cmath import *
#from SpatialTry import *

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

"""def AvarageX(listOfX):
    
    avX = 0 
    sumX = 0
    count = len(listOfX)

    print("IN THE METHOD") #, count

    for i in listOfX:
        print("Element: %d" %i)
        sumX = sumX + i
        count = count + 1 

   # avX = sumX / count

    return avX"""
"""
Contains data for acceleration/gyro/compass depending on what the board supports, as well as a timestamp.
This event is fired at a fixed rate as determined by the DataRate property.
"""

def SpatialDataHandler(e, acceleration, angularRate, fieldStrength, timestamp):
#write the data into a file
    
    file = open("NE.txt", "a")
    file.write("Field Strength: %7.3f  %8.3f  %8.3f \n" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))
    file.write("Acceleration:   %7.3f  %8.3f  %8.3f \n" % (acceleration[0], acceleration[1], acceleration[2]))
    print("Field Strength: %7.3f  %8.3f  %8.3f" % (fieldStrength[0], fieldStrength[1], fieldStrength[2]))
    print("Acceleration:   %7.3f  %8.3f  %8.3f" % (acceleration[0], acceleration[1], acceleration[2]))
    print("Angular rate:   %7.3f  %8.3f  %8.3f \n" % (angularRate[0], angularRate[1], angularRate[2]))


    
    
"""    with open('spatial_data.csv', 'w') as csvfile:
        fieldnames = ['FieldStrX', 'FieldStrY', 'FieldStrY', 'AccX', 'AccY', 'AccZ', 'AngRateX', 'AngRateY', 'AngRateZ']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     
        writer.writeheader()
        writer.writerows({'FieldStrX' : fieldStrength[0], 'FieldStrY' : fieldStrength[1], 
            'FieldStrY' : fieldStrength[2], 'AccX' : acceleration[0], 'AccY' : acceleration[1], 
            'AccZ' : acceleration[2], 'AngRateX' : angularRate[0], 'AngRateY' : angularRate[1], 
            'AngRateZ' : angularRate[2]})"""
    
   # filePlot = open("plotNorthSteadyX.txt", "a")
   # filePlot.write("%7.3f" % (fieldStrength[0]))


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
   # ch.setMagnetometerCorrectionParameters(0.36341, 0.09927, 0.11774, -0.07688,  2.66012, 2.56018, 3.03476, 0.01156, -0.07656, 0.00600, 0.06844, -0.05628, 0.07447)
    
    print("Waiting for the Phidget Spatial Object to be attached...")

    file = open("NE.txt", "a")
    file.write("--------------------------------------------")
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

