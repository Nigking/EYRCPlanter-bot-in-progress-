import RPi.GPIO as GPIO
import time, sys
import cv2
import numpy as np
import picamera
import picamera.array
from picamera.array import PiRGBArray

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


s = ("carnation.png","tulipred.png","gerber.png","lily-double.png","hydrangeayellow.png","sunflower.png","orchid.png","tulipblue.png","hydrangeablue.png")
k=-1

bluePin = 11   #Set to appropriate GPIO
redPin = 13 #Should be set in the
greenPin = 15 #GPIO.BOARD format
def blink(pin):
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin,GPIO.HIGH)
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane
    #print overlay_mask
    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

def stopwork(pzc):
    #Initialize camera
    k=-1
    camera = picamera.PiCamera()
    camera.resolution = (480,480)
    rawCapture = picamera.array.PiRGBArray(camera)
    #Let camera warm up
    time.sleep(0.1)

    #Capture image
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array

    #Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Blur image to reduce noise
    blurred = cv2.bilateralFilter(gray,11,75,0)
    #covert image into binary image for blackline detection.
    thresh = 150
    im_bw = cv2.threshold(blurred, thresh, 255, cv2.THRESH_BINARY)[1]
    #(thresh, im_bw) = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #ret,thresh = cv2.threshold(gray,60,255,0)
    #im_bw=thresh
    cv2.imshow("original",im_bw)
    cv2.waitKey(0)

    contours = cv2.findContours(im_bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#generating the list of contours
    contours=contours[0]
    count=0
    final = np.zeros(img.shape,np.uint8)
    final[...]=255
    
    for i in xrange(1,len(contours)):
        mask = np.zeros(gray.shape,np.uint8)
        mask[...]=0
        cv2.drawContours(mask,contours,i,255,-1)
        x=cv2.mean(img,mask)
        #cv2.drawContours(final,contours,i,x,-1)
        print x
        cv2.imshow("final",final)
        cv2.waitKey(0)
        #cv2.drawContours(final,contours,i,x,-1)
        if x[0]<200 or x[1]<200 or x[2]<200:
            (x1,y1),radius = cv2.minEnclosingCircle(contours[i])
            center = (int(x1),int(y1))
            radius = int(radius) 
            if x[0]-x[1] < 0 and x[2]<x[0] and x[2]<x[1]:
                a1= 3.142*radius*radius
                a2= cv2.contourArea(contours[i])
                cv2.drawContours(final,contours,i,x,-1)
                count=count+1
                blink(greenPin)
                time.sleep(1)
                
                if a2/a1>.75:
                    k=3
                elif a2/a1<=.5:
                    k=4
                else:
                    k=5
            elif x[0]-x[1] > 20 and x[2]<x[0] and x[2]<x[1]:
                count=count+1
                blink(bluePin)
                time.sleep(1)
                a1= 3.142*radius*radius
                a2= cv2.contourArea(contours[i])
                if a2/a1>.75:
                    k=6
                elif a2/a1<=.5:
                    k=7
                else:
                    k=8
            elif x[2]>x[0] and x[2]>x[1] and x[2]>120:
                count = count+1
                blink(redPin)
                time.sleep(1)
                a1= 3.142*radius*radius
                a2= cv2.contourArea(contours[i])
                if a2/a1>.75:
                    k=0
                elif a2/a1<=.5:
                    k=1
                else:
                    k=2
                    
    img=cv2.imread("Plantation.png",cv2.IMREAD_UNCHANGED)
    print k
    img1=cv2.imread(s[k],cv2.IMREAD_UNCHANGED)
    if pzc==1:
        ##############################zone=-------A###############333
        w2=30
        h2=60
        y2=240
        x2=340
        overlay_image = cv2.resize(img1,(w2,h2))#overlaying
        for i in range(0,count):
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
            x2=x2+50
        #####################################################3
        cv2.imshow("check",img)
        cv2.waitKey(0)
    elif pzc==2:
        ########################zone----B#####################
        w2=25
        h2=50
        y2=175
        x2=120
        overlay_image = cv2.resize(img1,(w2,h2))#overlaying
        img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>1:
            y2=y2+2
            x2=x2+50
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count > 2:
            y2=y2+40
            x2=x2-80
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>3:
            x2=x2+50
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        #############################################################
    elif pzc==3:
        #########################zone-----C#########################
        w2=25
        h2=50
        y2=140
        x2=290
        overlay_image = cv2.resize(img1,(w2,h2))#overlaying
        img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>1:
            x2=x2+60
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>2:
            y2=y2+20
            x2=x2-90
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>3:
            y2=y2-3
            x2=x2+60
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        ######################################################################
    elif pzc==4:
        ####################zone---D#################
        #print img.shape
        w2=20
        h2=40
        y2=165
        x2=520
        overlay_image = cv2.resize(img1,(w2,h2))#overlaying
        img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>1:
            y2=y2+2
            x2=x2+30
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>2:
            y2=y2+2
            x2=x2+30
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        if count>3:
            y2=y2+2
            x2=x2+30
            img[y2:y2+h2,x2:x2+w2,:] = blend_transparent(img[y2:y2+h2,x2:x2+w2,:], overlay_image)
        ################################################
            
    elif pzc==5:
        blink(redPin)
        time.sleep(1)
        blink(redPin)
        time.sleep(1)
        blink(redPin)
        time.sleep(1)
        blink(redPin)
        time.sleep(1)


stopwork(1)








        

