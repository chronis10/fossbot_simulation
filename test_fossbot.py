# Christos Chronis
#Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim

if clientID!=-1:
    print ('Connected to remote API server')

    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(2)
    #Create motor obgects
    _,left_motor = sim.simxGetObjectHandle(clientID,"left_motor", sim.simx_opmode_blocking)
    _,right_motor = sim.simxGetObjectHandle(clientID,"right_motor", sim.simx_opmode_blocking)
    _,ultrasonic = sim.simxGetObjectHandle(clientID,"ultrasonic_sensor", sim.simx_opmode_blocking)
    _,floor_sensor_middle = sim.simxGetObjectHandle(clientID,"MiddleSensor", sim.simx_opmode_blocking)
    _,floor_sensor_left = sim.simxGetObjectHandle(clientID,"LeftSensor", sim.simx_opmode_blocking)
    _,floor_sensor_right = sim.simxGetObjectHandle(clientID,"RightSensor", sim.simx_opmode_blocking)
    
    

    #Control motors
    #Forward -0.2 
    err_code = sim.simxSetJointTargetVelocity(clientID,left_motor,-0.2,sim.simx_opmode_streaming)
    err_code = sim.simxSetJointTargetVelocity(clientID,right_motor,-0.2,sim.simx_opmode_streaming)
    time.sleep(1)
    err_code = sim.simxSetJointTargetVelocity(clientID,left_motor,0,sim.simx_opmode_streaming)
    err_code = sim.simxSetJointTargetVelocity(clientID,right_motor,0,sim.simx_opmode_streaming)
    time.sleep(1)


    #Ultrasonic sensor get distance
    #for i in range(0,10):
        _,detectionState,detectedPoint,detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID, ultrasonic,sim.simx_opmode_streaming)  
        print(detectedPoint)
        time.sleep(1)


    #Floor Sensors
    # [23,23,23] is black line
    for i in range(0,10):
        _,resolution,image=sim.simxGetVisionSensorImage(clientID,floor_sensor_middle,0,sim.simx_opmode_streaming)
        print(f'Middle {image}')
        _,resolution,image=sim.simxGetVisionSensorImage(clientID,floor_sensor_left,0,sim.simx_opmode_streaming)
        print(f'Left {image}')
        _,resolution,image=sim.simxGetVisionSensorImage(clientID,floor_sensor_right,0,sim.simx_opmode_streaming)
        print(f'Right {image}')
        time.sleep(1)

        
    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
