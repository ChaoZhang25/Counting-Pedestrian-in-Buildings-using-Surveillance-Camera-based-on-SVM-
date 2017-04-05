# This is a module that is imported in other codes#
# This module is written to use opencv HOG library to detect pedestrian#
# Author: Zhang, Chao
# Last Modified Date: 04/08/2016

# This code requires the dependency of opencv python and numpy
import numpy as np
import cv2

FRAME_PER_SECOND = 25
TRESHOLD = 0.8

# To Test if rectangle q is inside of r
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

# To Draw the tracking points into frames, apend the point to a data structure.
def draw_detections(img, rects, thickness = 1):
    track_point = []
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        lt_x, lt_y = (x+pad_w, y+pad_h)
        rb_x, rb_y = (x+w-pad_w, y+h-pad_h)
        # Apend to track_point list
        track_point.append([(lt_x + rb_x) / 2, (lt_y + rb_y) / 2])
        # Uncomment below to show tracking points in the frames
        cv2.rectangle(img, ((lt_x + rb_x) / 2, ((lt_y + rb_y) / 2)), ((lt_x + rb_x) / 2 + 10, ((lt_y + rb_y) / 2 + 10)), (0, 255, 0), thickness)
    return track_point


# Using HOG Algorithms to track people
def people_track(frame):
    #Create HoG instance
    hog = cv2.HOGDescriptor()
    # Set SVM Detector
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    # Set Parameters
    found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.05)
    # Using a filter to get rid of wrong dectections
    found_filtered1 = []
    for i, v in enumerate(found):
        if w[i] > TRESHOLD:
            found_filtered1.append(v)
    # If a tracking point is inside another, eliminate it
    found_filtered2 = []
    for ri, r in enumerate(found_filtered1):
        for qi, q in enumerate(found_filtered1):
            if ri != qi and inside(r, q):
                break
            else:
                found_filtered2.append(r)
                break
    # Add points into tracking list
    track_point = draw_detections(frame, found_filtered2, 3)
    return track_point

# Transfer time to frame numbers
def get_frame_index(hour, minute, sec):
    return (hour * 3600 + minute * 60 + sec) * FRAME_PER_SECOND

# Transfer frame number to time
def get_time(frame_count):
    frame_count /= FRAME_PER_SECOND
    hour = frame_count / 3600
    minute = (frame_count - hour * 3600) / 60
    sec = (frame_count - hour * 3600 - minute * 60)
    return (hour, minute, sec)


def get_count(temp_count):
    mean = sum(temp_count) * 1.0 / len(temp_count)
    return int(round(mean))


#test = cv2.imread("TestFrame1.jpg")
#img = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
#num = people_count(img)
#cv2.imshow("frame", img)
#while(True):
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#cv2.destroyAllWindows()
