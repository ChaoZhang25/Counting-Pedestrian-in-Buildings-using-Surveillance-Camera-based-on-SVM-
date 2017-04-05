import os
import sys
import cv2
import subprocess
from multiprocessing import Pool

# This code has several inputs:
'''
1. ID of the video server
2. ID of the camera
3. year of the video
4. month of the vidoe
5. day of the video
'''

#print sum([len(x) for _, _, x in os.walk(os.path.dirname("/home/chaoz/connect/Download_Files/2016/10/20/166.111.131.46/35/"))])
#print len([x for x in os.listdir(os.path.dirname("/home/chaoz/connect/Download_Files/2016/10/20/166.111.131.46/35/")) if os.path.isfile(x)])
for a, b, c in os.walk('/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/'):
    print c
num = len(c)

# Get the lenth of each video
video_len = [0] * num
v_id = 0

while(v_id < num):
    if v_id != 0:
        print '/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '_' + str(v_id) + '.mp4'
        cap = cv2.VideoCapture('/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '_' + str(v_id) + '.mp4')
    else:
        print '/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '.mp4'
        cap = cv2.VideoCapture('/home/chaoz/connect/Download_Files/' + sys.argv[3] + '/' + sys.argv[4] + '/'+ sys.argv[5] + '/' + '166.111.131.' + sys.argv[1] + '/' + sys.argv[2] + '/166.111.131.' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + sys.argv[4] + sys.argv[5] + '.mp4')
    frames_fps = cap.get(5)
    frames_counts = cap.get(7)
    video_len[v_id] = int(frames_counts / frames_fps)
    cap.release
    v_id = v_id + 1

print video_len

# Use multiprocess
def count_task(v_id):
    s_time = 0
    i = 0
    while(i < v_id):
        s_time = s_time + video_len[i]
        i = i + 1
    print s_time
    print "python count.py " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4] + " " + sys.argv[5] + " " + str(v_id)  + " " + str(s_time)
    retcode = subprocess.call("python count.py " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4] + " " + sys.argv[5] + " " + str(v_id)  + " " + str(s_time), shell = True)

pool = Pool(processes = num)
for i in range(num):
    pool.apply_async(count_task, (i, ))

print('Waiting for all subprocesses done...')
pool.close()
pool.join()
print('All subprocesses done.')

#count_task(1)
#retcode = subprocess.call("python 46-35.py 46 35 2016 10 20 5 1000", shell = True)
