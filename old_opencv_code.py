import cv2
import os
import numpy as np
import math
from math import sqrt
#import matplotlib.pyplot as plt #USE THIS TO PLOT TRAJECTORY OF BALLS, AND TO PLOT THE ANGLE BETWEEN VECTORS
#import PIL.Image as Image

import numpy as np
import cv2

orange = [0, 165, 255] #BGR values
blue = [255, 0, 0] #BGR values
#green = [0, 255, 0] #BGR values
pink = [203, 192, 255] #BGR values
#FROM COMPUTERVISIONENG HSV GITHUB
def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    return lowerLimit, upperLimit
    #FROM COMPUTERVSIONENG HSV GITHUB 

print("This is testing and practice for OpenCV\n Firstly, lets try to load an image")
#image = cv2.imread('three_balls.png')
print("Current directory:", os.getcwd())
print("Image exists:", os.path.exists('s_dog2.png'))
image = cv2.imread('s_dog2.png')
#image = cv2.imread('"C:/Users/david/Java Workspace/s_dog.png"')


lowerLimO, upperLim = get_limits(orange)
#changing fom blue to green
#lowerLimB, upperLim2 = get_limits(blue)
lowerLimB = np.array([90, 50, 50], dtype=np.uint8)
upperLim2 = np.array([140, 255, 255], dtype=np.uint8)
print("Blue lower limit: ", lowerLimB)
print("Blue upper limit: ", upperLim2)
lowerLimP, upperLim3 = get_limits(pink)


#cv2.rectangle(image,(300,300),(500,600),(0,0,255),2) #draw a rectangle on the image

if image is None: 
    print("Could not read image")
else:
    print("Image loaded successfully, now converting to hsv")
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV image",hsv_image)
    maskO = cv2.inRange(hsv_image, lowerLimO, upperLim)
    maskB = cv2.inRange(hsv_image, lowerLimB, upperLim2)
    maskP = cv2.inRange(hsv_image, lowerLimP, upperLim3)
    combo_image = cv2.bitwise_or(maskO, maskB)
    combo_image = cv2.bitwise_or(combo_image, maskP)
  #  cv2.imshow("Orange mask",maskO)
  #  cv2.imshow("Blue mask",maskB)
  #  cv2.imshow("Pink mask", maskP)
  #  cv2.imshow("masks combined",combo_image)

    print("image shape: rows, columns, color channels: " + str(image.shape)) #this returns a tuple of the number of rows, columns, and channels (if the image is color)
    
    
    print("image size: " + str(image.size)) #this returns the total number of pixels in the image (rows * columns * channels)
    
    print("image data type: " + str(image.dtype)) #this returns the data type of the image (e.g., uint8 for 8-bit images)
    
    cv2.imshow("Image loading...",image)

# BLURRING AND GRAYSCALE
   # img_blur = cv2.blur(image,(7,7))
    img_gaussian = cv2.GaussianBlur(image,(7,7),0)
    # The 0 is the standard deviation in the X direction. If it is 0, then it is calculated from the kernel size.
    #cv2.imshow("Gaussian blur",img_gaussian)

   # img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img_gaussian, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Grayscale",img_gray)
    #cv2.imshow("Blurrrrr",img_blur)
#thresh
    ret, thresh = cv2.threshold(combo_image,100,255,cv2.THRESH_BINARY)
    cv2.imshow("Threshold Using Combo Image",thresh)
    #ret, thresh = cv2.threshold(img_gray,90,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    #print("hierarchy is: "+str(hierarchy[0].toList()))
    # what does this do? I think it finds the contours of the image, and returns them as a list of points. 
    # The hierarchy is a list of lists, where each list contains the indices of the contours that are nested within the current contour.
    xcenterarray = []
    ycenterarray = []
    for cnt in contours:
        print("Contour area: " + str(cv2.contourArea(cnt)))
        #if cv2.contourArea(cnt) > 100: #filter out small contours
        if cv2.contourArea(cnt) > 50 and cv2.contourArea(cnt) < 250:
                                #WAS > 200
            print(cv2.contourArea(cnt))
            cv2.drawContours(image, [cnt], 0, (0,255,0), 3) #draw the contours on the image

            x1,y1,w,h = cv2.boundingRect(cnt) #get the bounding box of the contour
            cv2.rectangle(image,(x1,y1),(x1+w,y1+h),(255,0,0),2) #draw the bounding box on the image
            xcenter = x1 + w/2
            ycenter = y1 + h/2
            
            #bad hard code
           # if xcenter != 130.5:
            xcenterarray+= [xcenter]
            ycenterarray+= [ycenter]
            
            print("xcenter: " + str(xcenter) + " ycenter: " + str(ycenter))
    print(xcenterarray)
    print(ycenterarray)
    #bad hard code
    
    x1 = xcenterarray[0]
    y1 = ycenterarray[0]
    x2 = xcenterarray[1]
    y2 = ycenterarray[1]
    x3 = xcenterarray[2]
    y3 = ycenterarray[2]
#v2 is nonsense?
    v1 = np.array([x2-x1,y2-y1])
    v2 = np.array([x3-x2,y3-y2])
    cv2.arrowedLine(image,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),2) #draw an arrow from point 1 to point 2
    cv2.arrowedLine(image,(int(x2),int(y2)),(int(x3),int(y3)),(0,0,255),2) #draw an arrow from point 2 to point 3


    magnitude_v1 = sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = sqrt(v2[0]**2 + v2[1]**2)
    dot_product = np.dot(v1,v2)

    angle = np.arccos(dot_product/(magnitude_v1*magnitude_v2))
    angle_degrees = np.degrees(angle)
    print("Angle in degrees",angle_degrees)

    for i in range(len(xcenterarray)):
       cv2.circle(image,(int(xcenterarray[i]),int(ycenterarray[i])),5,(0,255,0),-1) #draw a circle at the center of the contour
        
    cv2.imshow("Threshold",thresh)
    cv2.imshow("Image loading...",image)
   

    cv2.waitKey(0) # waitKey is used to say wait for a key press BEFORE you immediately close the window. 
    #The argument is time in ms, for how long the window will remain open with no key press
    #waitKey(0) means wait indefinetly
    cv2.destroyAllWindows() #after waitKey returns true, i suppose, the opened window is closed. 
    #This is a good practice to avoid memory leaks and other issues.
# Toggle video test here

#CODE FROM CLAUDE
lowerGreen = np.array([40, 60, 40])
upperGreen = np.array([85, 255, 255])

kernel = np.ones((5, 5), np.uint8)
open_k  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
close_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))  # roughly marker diameter

def get_sleeve_roi(hsv_image, grow_px=12, min_sleeve_area=1500):
    green = cv2.inRange(hsv_image, lowerGreen, upperGreen)
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, open_k)
    green = cv2.morphologyEx(green, cv2.MORPH_CLOSE, close_k)     # one pass, marker-sized

    contours, _ = cv2.findContours(green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) > min_sleeve_area]
    roi = np.zeros_like(green)
    if not contours:
        return roi
    sleeve = max(contours, key=cv2.contourArea)
    cv2.drawContours(roi, [sleeve], -1, 255, thickness=cv2.FILLED)  # no hull
    if grow_px > 0:
        roi = cv2.dilate(roi, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (2*grow_px+1, 2*grow_px+1)))
    return roi

# def find_marker(mask, min_area=60, max_area=350):
#     """Return (cx, cy) of the largest valid contour in a single-color mask, or None."""
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = [c for c in contours if min_area < cv2.contourArea(c) < max_area]
#     if not contours:
#         return None
#     c = max(contours, key=cv2.contourArea)
#     x, y, w, h = cv2.boundingRect(c)
#     return (x + w/2, y + h/2)

#video = cv2.VideoCapture('dog_vid2.mp4')
# while True:
#     ret, frame = video.read()
#     if not ret:
#         break

    # hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # roi = get_sleeve_roi(hsv_image)

    # # color masks, each restricted to the sleeve region
    # maskO = cv2.bitwise_and(cv2.inRange(hsv_image, lowerLimO, upperLim),  roi)
    # maskB = cv2.bitwise_and(cv2.inRange(hsv_image, lowerLimB, upperLim2), roi)
    # maskP = cv2.bitwise_and(cv2.inRange(hsv_image, lowerLimP, upperLim3), roi)

    # # clean each mask a little
    # maskO, maskB, maskP = [cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel) for m in (maskO, maskB, maskP)]

#CODE FROM CLAUDE END

test_vid = True
if test_vid:
    #now lets load a video and display it frame by frame
    print("Lets try to load a video and display it in a window")
    video = cv2.VideoCapture('dog_vid2.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output = cv2.VideoWriter("output_vid.mp4",fourcc,30.0,(frame_width, frame_height))
    output2 = cv2.VideoWriter("output_masked.mp4",fourcc,30.0,(frame_width, frame_height),isColor=False)
    ret = True
    while ret:
        ret, frame = video.read()
        #ret says if we have read a new frame. aka, is the video over
        if ret:

            #CLAUDE CODE
            hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            roi = get_sleeve_roi(hsv_image)
            
            # color masks, each restricted to the sleeve region
            maskO = cv2.bitwise_and(cv2.inRange(hsv_image, lowerLimO, upperLim),  roi)
            maskB = cv2.bitwise_and(cv2.inRange(hsv_image, lowerLimB, upperLim2), roi)
            maskP = cv2.bitwise_and(cv2.inRange(hsv_image, lowerLimP, upperLim3), roi)
            
            # clean each mask a little
            maskO, maskB, maskP = [cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel) for m in (maskO, maskB, maskP)]
            #CLAUDE CODE END

            print("Reading video frame")
           #hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #create masks for each color in video frame
           # cv2.imshow("HSV image",hsv_image)
           # maskO = cv2.inRange(hsv_image, lowerLimO, upperLim)
            #maskB = cv2.inRange(hsv_image, lowerLimB, upperLim2)
           # maskP = cv2.inRange(hsv_image, lowerLimP, upperLim3)
            combo_image = cv2.bitwise_or(maskO, maskB)
            combo_image = cv2.bitwise_or(combo_image, maskP)
            annotated = frame.copy()
    
            roi_contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(annotated, roi_contours, -1, (0, 255, 0), 1)
        #now make a threshold image using the masked version of the current frame
            ret2, thresh = cv2.threshold(combo_image,100,255,cv2.THRESH_BINARY)
        #cv2.imshow("Threshold Using Combo Image",thresh)
        #ret, thresh = cv2.threshold(img_gray,90,255,cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        #print("hierarchy is: "+str(hierarchy[0].toList()))
        # what does this do? I think it finds the contours of the image, and returns them as a list of points. 
        # The hierarchy is a list of lists, where each list contains the indices of the contours that are nested within the current contour.
            xcenterarray = []
            ycenterarray = []
            for cnt in contours:
                print("Contour area: " + str(cv2.contourArea(cnt)))
            #if cv2.contourArea(cnt) > 100: #filter out small contours
                if cv2.contourArea(cnt) > 60 and cv2.contourArea(cnt) < 300:
                    #this is actually pretty close. It just picks up some unwanted colors
                    # and the colors are lost on a few frames
                    #now, I need ot make a better array value capture system
                                                    #WAS > 200
                    print(cv2.contourArea(cnt))
                    cv2.drawContours(combo_image, [cnt], 0, (0,255,0), 3) #draw the contours on the image
                    
                    x1,y1,w,h = cv2.boundingRect(cnt) #get the bounding box of the contour
                    cv2.rectangle(combo_image,(x1,y1),(x1+w,y1+h),(255,0,0),2) #draw the bounding box on the image
                    xcenter = x1 + w/2
                    ycenter = y1 + h/2
                                
                #bad hard code
               
                    xcenterarray+= [xcenter]
                    ycenterarray+= [ycenter]
                                
                    print("xcenter: " + str(xcenter) + " ycenter: " + str(ycenter))
                    print(xcenterarray)
                    print(ycenterarray)
                        #bad hard code
                if len(xcenterarray) == 3 and len(ycenterarray) == 3:     
                    x1 = xcenterarray[0]
                    y1 = ycenterarray[0]
                    x2 = xcenterarray[1]
                    y2 = ycenterarray[1]
                    x3 = xcenterarray[2]
                    y3 = ycenterarray[2]
        #v2 is nonsense?
                    v1 = np.array([x2-x1,y2-y1])
                    v2 = np.array([x3-x2,y3-y2])
                    cv2.arrowedLine(combo_image,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),2) #draw an arrow from point 1 to point 2
                    cv2.arrowedLine(combo_image,(int(x2),int(y2)),(int(x3),int(y3)),(0,0,255),2) #draw an arrow from point 2 to point 3
                    cv2.arrowedLine(annotated,(int(x2),int(y2)),(int(x3),int(y3)),(0,0,255),2)
                    
                    magnitude_v1 = sqrt(v1[0]**2 + v1[1]**2)
                    magnitude_v2 = sqrt(v2[0]**2 + v2[1]**2)
                    dot_product = np.dot(v1,v2)
        
                    angle = np.arccos(dot_product/(magnitude_v1*magnitude_v2))
                    angle_degrees = np.degrees(angle)
                    if angle_degrees < 100 :#HARD CODED, BECASUE DOG LEG SHOULDNT EXCEED 
                        cv2.putText(
                            annotated,
                            "Joint angle: " + str(round(angle_degrees, 1)),
                            (int(x2), int(y2)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 255),
                            2,
                            cv2.LINE_AA
                        )
                    print("Angle in degrees (VIDEO)",angle_degrees)
                    for i in range(len(xcenterarray)):
                        cv2.circle(combo_image,(int(xcenterarray[i]),int(ycenterarray[i])),5,(0,255,0),-1) #draw a circle at the center of the contour
                        cv2.circle(hsv_image,(int(xcenterarray[i]),int(ycenterarray[i])),5,(0,255,0),-1)
                        cv2.circle(annotated,(int(xcenterarray[i]),int(ycenterarray[i])),5,(0,255,0),-1)
            output.write(annotated)
            output2.write(combo_image)
            cv2.imshow('combovideo',combo_image)
            cv2.imshow('REGION OF INTEREST? annotated', annotated)
            cv2.waitKey(50) #wait 33 ms, which is 1/30fps
            

video.release() #release the video capture object
#cv2.destroyAllWindows() #close the window
        #Release memory and resources used by the video capture object and close any OpenCV windows that were opened. This is important to avoid memory leaks and other issues when working with videos in OpenCV.

#Now, lets read from the webcam
#print("Now we will read from camera")
webTest = False
if webTest:
    webcam = cv2.VideoCapture(0) #default camera
    while True:
        ret,frame = webcam.read()
        cv2.imshow('webcam',frame)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    #Webcam data will loop until user wants video capture to end by pressing q
    webcam.release()
cv2.destroyAllWindows()

