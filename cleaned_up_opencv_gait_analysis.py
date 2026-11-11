import cv2
import os
import numpy as np
import math
from math import sqrt
#import matplotlib.pyplot as plt #USE THIS TO PLOT TRAJECTORY OF BALLS, AND TO PLOT THE ANGLE BETWEEN VECTORS
#import PIL.Image as Image

import numpy as np
import cv2



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
print("Video exists:", os.path.exists('dog_gait_front_rignt_markers.mp4'))
#image = cv2.imread('s_dog2.png')
#image = cv2.imread('"C:/Users/david/Java Workspace/s_dog.png"')

orange = [0, 165, 255] #BGR values
blue = [255, 0, 0] #BGR values
green = [0, 255, 0] #BGR values
yellow = [0, 255, 255] #BGR values
red = [0, 0, 255] #BGR values
pink = [203, 192, 255] #BGR values

# Get upper in lower limits/range for each color defined above
lower_lim_orange, upper_lim_orange = get_limits(orange)
lower_lim_blue, upper_lim_blue = get_limits(blue)
lower_lim_yellow, upper_lim_yellow = get_limits(yellow)
lower_lim_red, upper_lim_red = get_limits(red)
lower_lim_pink, upper_lim_pink = get_limits(pink)

lower_lim_green, upper_lim_green = get_limits(green)

#CODE FROM CLAUDE
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

def find_marker_center(mask, min_area=60,max_area=800):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = [c for c in contours if cv2.contourArea(c) > min_area and cv2.contourArea(c) < max_area]

    if not contours:
        return None

    # Use largest detected contour
    cnt = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(cnt)

    center = (int(x + w/2), int(y + h/2))

    return center

# Create display windows
cv2.namedWindow("annotated", cv2.WINDOW_NORMAL)
cv2.resizeWindow("annotated", 1280, 720)

cv2.namedWindow("combovideo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("combovideo", 1280, 720)




test_vid = True
if test_vid:
    #now lets load a video and display it frame by frame
    #create video object 
    video = cv2.VideoCapture('dog_gait_front_right_markers.mp4')

    #necessary information for writing to a video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output = cv2.VideoWriter("output_vid.mp4",fourcc,30.0,(frame_width, frame_height))
    output2 = cv2.VideoWriter("output_masked.mp4",fourcc,30.0,(frame_width, frame_height),isColor=False)

    #xcenterarray = []
    #ycenterarray = []
    blue_path = []
    red_path = []
    yellow_path = []

    ret = True
    while ret:
        ret, frame = video.read()
        #ret says if we have read a new frame. aka, is the video over
        if ret:

            #CLAUDE CODE
            hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #roi = get_sleeve_roi(hsv_image)
            
            # color masks, each restricted to the sleeve region
            #maskY = cv2.bitwise_and(cv2.inRange(hsv_image, lower_lim_yellow, upper_lim_yellow),hsv_image)
            #maskB = cv2.bitwise_and(cv2.inRange(hsv_image, lower_lim_blue, upper_lim_blue))
            #maskR = cv2.bitwise_and(cv2.inRange(hsv_image, lower_lim_red, upper_lim_red))
            
            maskY = cv2.inRange(hsv_image, lower_lim_yellow, upper_lim_yellow)
            maskB = cv2.inRange(hsv_image, lower_lim_blue, upper_lim_blue)
            maskR = cv2.inRange(hsv_image, lower_lim_red, upper_lim_red)

            # clean each mask a little
            maskY, maskB, maskR = [cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel) for m in (maskY, maskB, maskR)]

           

            print("Reading video frame")
           #create masks for each color in video frame
           # cv2.imshow("HSV image",hsv_image)
           
            combo_image = cv2.bitwise_or(maskY, maskB)
            combo_image = cv2.bitwise_or(combo_image, maskR)
            annotated = frame.copy()

            blue_center = find_marker_center(maskB)
            red_center = find_marker_center(maskR)
            yellow_center = find_marker_center(maskY)

            # Draw markers on original frame
            for center, color in [
                (blue_center, (255, 0, 0)),
                (red_center, (0, 0, 255)),
                (yellow_center, (0, 255, 255))
            ]:

                if center is not None:
                    cv2.circle(annotated, center, 6, color, -1)

            # roi_contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            

            #now make a threshold image using the masked version of the current frame
            ret2, thresh = cv2.threshold(combo_image,100,255,cv2.THRESH_BINARY)

            cv2.imshow("Threshold Using Combo Image",thresh)
            #ret, thresh = cv2.threshold(img_gray,90,255,cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
            cv2.drawContours(annotated,contours,-1, (0, 255, 0), 1)
        #print("hierarchy is: "+str(hierarchy[0].toList()))
     
        # The hierarchy is a list of lists, where each list contains the indices of the contours that are nested within the current contour.
            
            for cnt in contours:
                print("Contour area: " + str(cv2.contourArea(cnt)))
            #if cv2.contourArea(cnt) > 100: #filter out small contours
                if cv2.contourArea(cnt) > 60 and cv2.contourArea(cnt) < 800: #filter out small contours and large contours
                
                    print(cv2.contourArea(cnt))
                    cv2.drawContours(combo_image, [cnt], 0, (0,255,0), 3) #draw the contours on the image
                    
                    x1,y1,w,h = cv2.boundingRect(cnt) #get the bounding box of the contour
                    cv2.rectangle(combo_image,(x1,y1),(x1+w,y1+h),(255,0,0),2) #draw the bounding box on the image
                
                    
# Only calculate angle if all three markers are detected
                if (blue_center is not None and
                    red_center is not None and
                    yellow_center is not None):

                    blue_path.append(blue_center)
                    red_path.append(red_center)
                    yellow_path.append(yellow_center)

                    # get coordinates
                    x1, y1 = blue_center
                    x2, y2 = red_center
                    x3, y3 = yellow_center

                    # Calculate vectors
                    # Both vectors originate at the middle joint
                    v1 = np.array([x1-x2, y1-y2])
                    v2 = np.array([x3-x2, y3-y2])

                    # Calculate vector magnitudes
                    magnitude_v1 = np.linalg.norm(v1)
                    magnitude_v2 = np.linalg.norm(v2)

                    if magnitude_v1 > 0 and magnitude_v2 > 0:

                        # Calculate angle using dot product
                        dot_product = np.dot(v1, v2)

                        cosine = dot_product / (magnitude_v1 * magnitude_v2)

                        # Prevent floating-point errors
                        cosine = np.clip(cosine, -1.0, 1.0)

                        angle = np.arccos(cosine)
                        angle_degrees = np.degrees(angle)

                        # Display angle on annotated video
                        if angle_degrees > 70:
                            cv2.putText(
                                annotated,
                                "Joint angle: " + str(round(angle_degrees, 2)),
                                (int(x2), int(y2)),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0, 255, 255),
                                2,
                                cv2.LINE_AA
                            )

                        print("Angle in degrees:", angle_degrees)

                        # Draw vectors on annotated video
                        cv2.arrowedLine(
                        annotated,
                        (int(x2), int(y2)),
                        (int(x1), int(y1)),
                        (255, 0, 0),
                        2
                        )

                        cv2.arrowedLine(
                        annotated,
                        (int(x2), int(y2)),
                        (int(x3), int(y3)),
                        (0, 0, 255),
                        2
                        )

                    print("Blue center:", blue_center)
                    print("Red center:", red_center)
                    print("Yellow center:", yellow_center)
                        #bad hard code
               
                    if angle_degrees > 70 :#HARD CODED, BECASUE DOG LEG SHOULDNT EXCEED 
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
                    
# Draw historical marker positions as green circles

                for point in blue_path:
                    cv2.circle(
                        annotated,
                        point,
                        3,
                        (0, 255, 0),
                        -1
                    )

                for point in red_path:
                    cv2.circle(
                        annotated,
                        point,
                        3,
                        (0, 255, 0),
                        -1
                    )

                for point in yellow_path:
                    cv2.circle(
                        annotated,
                        point,
                        3,
                        (0, 255, 0),
                        -1
                    )

            output.write(annotated)
            output2.write(combo_image)

            cv2.imshow('combovideo',combo_image)
            cv2.imshow('annotated', annotated)
            # Press ESC to stop playback
            if cv2.waitKey(33) & 0xFF == 27:
                break

            #cv2.waitKey(33) #wait 33 ms, which is 1/30fps
            
print("Done with video")
print("Releasing video capture object and closing windows...")

video.release() #release the video capture object
cv2.destroyAllWindows() #close the window

