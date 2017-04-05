import numpy as np
import sys
import cv2
import PersonRecog
import time
import math
import MySQLdb as mysql

# This code has several inputs:
'''
1. ID of the video server
2. ID of the camera
3. year of the video
4. month of the vidoe
5. day of the video
6. ID of the video seperates, starts from 0
7. current time of the day, counted in sec
'''

class Pedestrian:

    # Initialize pedestrian
    def __init__(self, cur, frame):
        self.direction = [0, 0] # The walking direction vector of pedestrian
        self.frame_cur = frame # Current frame number
        self.frame_start = frame # The frame when a pedestrian apears in the frame
        self.pos_current = cur # Current position of the pedestrian in the frame
        self.pos_start = cur # The position when a pedestrian first apears in a frame
        self.pos_history = [] # Position history of a

        self.pos_history.append(cur) # Initialize pos_history
        self.direction = [0, 0] # Initialize direction vector

    # Renew the parameters of a pedestrian
    def renew(self, pos, frame):
        self.pos_current = pos
        self.direction[0] = self.pos_current[0] - self.pos_start[0] # Renew direction
        self.direction[1] = self.pos_current[1] - self.pos_start[1] # Renew direction
        self.pos_history.append(pos)
        self.frame_cur = frame

# Caculate Distance
def distance(x, y):
    return math.sqrt((x[0] - y[0]) * (x[0] - y[0]) + (x[1] - y[1]) * (x[1] - y[1]))


#----------------------To Process One Vidoe--------------------------#

# Set real time and date of this video

STAR_TIME = "2015-10-20 0:0:0"
timeArray = time.strptime(STAR_TIME, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))

# Add the current time
timeStamp = timeStamp + int(sys.argv[7])

zeroStart = timeStamp

'''
# Set start time and end time of this video
(hour_start, minute_start, sec_start) = (0, 0, 0)
(hour_end, minute_end, sec_end) = (3, 9, 23)
'''

# Get time
time_start = time.time()
# Read video


if int(sys.argv[6]) != 0:
    print '/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '_' + sys.argv[6] + '.mp4'
    cap = cv2.VideoCapture('/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '_' + sys.argv[6] + '.mp4')
else:
    print '/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '.mp4'
    cap = cv2.VideoCapture('/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '.mp4')

# Get property of Video
frames_fps = cap.get(cv2.CAP_PROP_FPS)
frames_counts = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print "The Total frame of the video is " + str(frames_counts)
print "The FPS of the video is " + str(frames_fps)

# Set start frame and end frame
start_frame = 0
end_frame = frames_counts

'''
start_frame = PersonRecog.get_frame_index(hour_start, minute_start, sec_start)
end_frame = PersonRecog.get_frame_index(hour_end, minute_end, sec_end)
'''

'''
ret, img = cap.read()
sp = img.shape
door = img[100:280, 200:650]
cv2.imshow('frame', door)

'''
conn = mysql.connect(host='localhost', user='root', passwd='cfins622')
cur = conn.cursor()
cur.execute("""create database if not exists ZC""")
conn.select_db('ZC')


def get_direction(dir):
    if dir[1] < 0:
        return 1
    else:
        return 0

lost_track_distance = 18
leave_indicator = 15
mini_move_distance = 8

def renew_list(list, points, frame, count):
    # If there is no pedestrain before this frame
    if len(list) == 0:
        # If there is no pedestrian detected in this frame
        if len(points) == 0:
            return [list, count]
        else:
            # Add new pedestrian in to list
            for p in points:
                person = Pedestrian(p, frame)
                list.append(person)
            return [list, count]
    else:
        i = 0
        # Traverse the current list of pedestrian to see if a pedestrian has left the region
        #print len(list)
        while i < len(list):
            # dif indicates the frames passed after the last renewal of a pedestrian
            dif = frame - list[i].frame_cur
            # print dif
            if dif > leave_indicator:
                # If the position of pedestrian has not been updated in 10 frames
                # We may have a reason to believe that the pedestrian has left the region
                dir = list[i].direction
                # print dir
                # If the distance between the position of apearance and the position of leave
                # is longer than a threshold, we confirm that the pedestrian left the region
                if math.sqrt(dir[0]*dir[0] + dir[1]*dir[1]) > mini_move_distance:
                    w = get_direction(dir)
                    count[w] += 1 
                # Else it may only be noise. Delete the false pedestrain
                del list[i]
            i += 1
        # If in the current frame, we have detected the pedestrian
        if len(points) != 0:
            j = 0
            ped_cur = len(list)
            ind = [0] * ped_cur
            # For every pedestrian in the list,
            # traverse the current list points that are detected in this frame
            # to find the nearest point and the distance between them.
            # If the distance is smaller than certain threshold,
            # we believe the pedestrain moves to this point
            while j < ped_cur:
                mini = 1000
                k = 0
                while k < len(points):
                    temp = distance(list[j].pos_current, points[k])
                    if temp < mini:
                        mini = temp
                        ind[j] = k
                    k += 1
                if mini < lost_track_distance:
                    list[j].renew(points[ind[j]], frame) # Renew the position of pedestrian.
                    del points[ind[j]] # This point has been tracked, so delete it.
                j += 1
            # After the traversal, if there are points left, we consider them as new arrival
            if len(points) > 0:
                for p in points:
                    person = Pedestrian(p, frame)
                    list.append(person)
            return [list, count]
        else:
            return [list, count]

people_list = []
count = [0] * 2

current_frame = start_frame
print start_frame

frames_fps = cap.get(cv2.CAP_PROP_FPS)
frames_counts = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print frames_counts
print frames_fps

#cv2.imshow('frame', img[int(sys.argv[1]):int(sys.argv[2]), int(sys.argv[3]):int(sys.argv[4])])
# Press q to abort program
while True:
    temp_count = []
    ret, img = cap.read()
    #sp = img.shape
    door = img[100:250, 500:630]
    #print 'width: %d \nheight: %d \nnumber: %d' %(sp[0],sp[1],sp[2])
    track_points = PersonRecog.people_track(door)
    # print track_points
    people_list, count = renew_list(people_list, track_points, current_frame, count)
    current_frame = current_frame + 1
    # Store to data base every 25 frames (per sec)
    if current_frame % 25 == 1:
        # Formating
        timeStamp += 1
        timeArray = time.localtime(timeStamp)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        #print "***********"
        #print formatTime
        value = [timeStamp, count[0], count[1], formatTime, zeroStart]
        # Restore
        cur.execute("insert into F1_" + sys.argv[1] + "_" + sys.argv[2] + " values(%s, %s, %s, %s, %s)", value)
        conn.commit()
    #cv2.imshow('frame', door)
    #print track_points
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # cv2.destroyAllWindows()
        cap.release
        break
    # Stop processing when reach the end frame of the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_frame:
        cap.release
        break
cap.release
cv2.destroyAllWindows()

