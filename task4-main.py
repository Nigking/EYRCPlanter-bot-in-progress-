'''
*Team Id: 584
*Author List: Prakhar Mishra,Srishti Lalchandani
*
*Filename: task4-main.py
*Theme: Planter Bot
*Functions: NONE
*Global Variables: Motor1A,Motor1B,Motor1E,Motor2A,Motor2B,Motor2E,s,k,bluPin,greenPin,redPin,l,z,left,right
*
'''
import cv2 
import os
import picamera
import picamera.array
from picamera.array import PiRGBArray
import numpy as np
import time

import RPi.GPIO as GPIO
from time import sleep


import RPi.GPIO as GPIO
from time import sleep
from integrated import blink,blend_transparent,stopwork

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 33
Motor1B = 35
Motor1E = 37
Motor2A = 36
Motor2B = 38
Motor2E = 40

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
left = GPIO.PWM(Motor1E, 100)
right = GPIO.PWM(Motor2E, 100)
left.start(00)
right.start(00)
s = ("carnation.png","tulipred.png","gerber.png","lily-double.png","hydrangeayellow.png","sunflower.png","orchid.png","tulipblue.png","hydrangeablue.png")
#s:: holds the nmaes of overlay images file in array according to the table provided
k=-1 #k:holds the index according to color marker detected for s


bluePin = 11   #Set to appropriate GPIO
redPin = 13 #Should be set in the
greenPin = 15 #GPIO.BOARD format
camera = picamera.PiCamera()
camera.resolution = (480,480)
camera.framerate = 35
raw_cap = PiRGBArray(camera,(480,480))
#Let camera warm up
time.sleep(0.1)
frame_cnt = 0
l=1
z=0
left.ChangeDutyCycle(00)
right.ChangeDutyCycle(00)
#GPIO.output(Motor1A,GPIO.HIGH)
#GPIO.output(Motor1B,GPIO.LOW)

#GPIO.output(Motor2A,GPIO.HIGH)
#GPIO.output(Motor2B,GPIO.LOW)

plant=cv2.imread("Plantation.png")
cv2.imshow("background",plant)
for frame in camera.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(480,480)):
    color_image = frame.array
    img = color_image
    
    #Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Blur image to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    #covert image into binary image for blackline detection.
    thresh = 80
    #thresh = 95
    im_bw = cv2.threshold(blurred, thresh, 255, cv2.THRESH_BINARY)[1]
    #(thresh, im_bw) = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #perform two sweeps to determine the orientation of black line
    #cv2.imshow("feed",im_bw)
    
    #sq1 = im_bw[200:300, 105:205]
    #sq2 = im_bw[200:300, 205:305]
    #sq3 = im_bw[200:300, 305:405]
    sq1 = im_bw[0:100, 105:205]
    sq2 = im_bw[0:100, 205:305]
    sq3 = im_bw[0:100, 305:405]
    #cv2.imshow("feed1",sq1)
    #cv2.imshow("feed2",sq2)
    #cv2.imshow("feed3",sq3)
    s1=cv2.countNonZero(sq1)
    s2=cv2.countNonZero(sq2)
    s3=cv2.countNonZero(sq3)
    sz=100*100
    if (s1<=5000):
        a1='B'
    else:
        a1='W'
    sz=100*100
    if (s2<=5000):
        a2='B'
    else:
        a2='W'
    sz=100*100
    if (s3<=5000):
        a3='B'
    else:
        a3='W'
    
    k=a1+a2+a3
    print k
    sq1s = im_bw[380:480, 105:205]
    sq2s = im_bw[380:480, 205:305]
    sq3s = im_bw[380:480, 305:405]
    s1s=cv2.countNonZero(sq1s)
    s2s=cv2.countNonZero(sq2s)
    s3s=cv2.countNonZero(sq3s)
    #cv2.imshow("feed1s",sq1s)
    #cv2.imshow("feed2s",sq2s)
    #cv2.imshow("feed3s",sq3s)
    if (s1<=5000):
        a1s='B'
    else:
        a1s='W'
    sz=100*100
    if (s2<=5000):
        a2s='B'
    else:
        a2s='W'
    sz=100*100
    if (s3<=5000):
        a3s='B'
    else:
        a3s='W'
    if (s1s<=5000):
        a1s1='B'
    else:
        a1s1='W'
    
    if (s2s<=5000):
        a2s1='B'
    else:
        a2s1='W'
    sz=100*100
    if (s3s<=5000):
        a3s1='B'
    else:
        a3s1='W'
    ks1=a1s1+a2s1+a3s1
    ks=a1s+a2s+a3s

    if ((z<3)or(z==4)):
        if ((ks1=='WBW')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            left.ChangeDutyCycle(80)
            right.ChangeDutyCycle(80)

        if(ks1=='WWW'):
            
            if (l==2):
                right.ChangeDutyCycle(0)
                left.ChangeDutyCycle(80)
            if(l==3):
                right.ChangeDutyCycle(80)
                left.ChangeDutyCycle(0)
            
        if (ks1=='BWW'):
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(80)
            l=2
        if ((ks1=='WBW')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "straight"
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
        
        if (ks1=='WWB'):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "right"
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(0)
            l=3


        if ((ks1=='BBB')and(frame_cnt>20)and(z==0)):
            z=z+1
            
            
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(0)
            stopwork(1)
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
            time.sleep(.5)
        if ((ks1=='BBB')and(frame_cnt>200)and(z==1)):
            z=z+1
            
            
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(0)
            stopwork(2)
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
            time.sleep(.5)
            
        if ((ks1=='BBB')and(frame_cnt>550)and(z==2)):
            z=z+1
            
            
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(0)
            stopwork(3)
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
            time.sleep(.5)
        if ((ks1=='BBB')and(frame_cnt>1200)and(z==4)):
            z=z+1
            
            
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(0)
            time.sleep(.5)
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
            
        
    if (z==3):
        if ((k=='WBW')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            left.ChangeDutyCycle(50)
            right.ChangeDutyCycle(50)

        if(k=='WWW'):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "plane" 
        #GPIO.output(Motor1E,GPIO.LOW)
        #GPIO.output(Motor2E,GPIO.LOW)
            if (l==2):
                right.ChangeDutyCycle(0)
                left.ChangeDutyCycle(50)
            if(l==3):
                right.ChangeDutyCycle(50)
                left.ChangeDutyCycle(0)
            
        if (k=='BWW'):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "left"
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(50)
          #print x1value
                #print x2value
            l=2
        if ((k=='WBW')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "straight"
            right.ChangeDutyCycle(50)
            left.ChangeDutyCycle(50)
        
        if (k=='WWB'):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "right"
            right.ChangeDutyCycle(50)
            left.ChangeDutyCycle(0)
            l=3


        if ((ks1=='BBB')and(frame_cnt>1000)and(z==3)):
            z=z+1
            time.sleep(.65)
            
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(0)
            stopwork(3)
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
            time.sleep(.5)
    if (z==5):
        if ((k=='WBW')or(k=='BWB')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            left.ChangeDutyCycle(80)
            right.ChangeDutyCycle(80)

        if((k=='WWW')or(k=='BBB')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "plane" 
        #GPIO.output(Motor1E,GPIO.LOW)
        #GPIO.output(Motor2E,GPIO.LOW)
            if (l==2):
                right.ChangeDutyCycle(0)
                left.ChangeDutyCycle(80)
            if(l==3):
                right.ChangeDutyCycle(80)
                left.ChangeDutyCycle(0)
            
        if ((k=='BWW')or(k=='WBB')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "left"
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(80)
          #print x1value
                #print x2value
            l=2
        if ((k=='WBW')or(k=='BWB')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "straight"
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(80)
        
        if ((k=='WWB')or(k=='BBW')):
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)

            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)        

            print "right"
            right.ChangeDutyCycle(80)
            left.ChangeDutyCycle(0)
            l=3


        if ((ks1=='BBB')and(frame_cnt>1250)and(z==5)):
            z=z+1
            time.sleep(.65)
            
            
            right.ChangeDutyCycle(0)
            left.ChangeDutyCycle(0)
            stopwork(5)
            break


    cv2.waitKey(1)
    raw_cap.truncate(0)
    #x=480 y=480 max values
    #dividing image into 3 sectors
    #first check orientation for whole image if not determined check line orientation in each sector.

    frame_cnt = frame_cnt + 1
    print frame_cnt
    #if the picam has captured 10 seconds of video leave the loop and stop recording
    if(frame_cnt> 10000):
		#cam.stop_preview()
		#cam.close()
        break
    
print ("Ending....")

cv2.destroyAllWindows()
    
