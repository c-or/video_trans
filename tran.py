import cv2
from moviepy.editor import *

cap = cv2.VideoCapture('2022-11-21 16.45.11.mp4')
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(frame_count,fps)
step = int(frame_count/10)
i,j = 0,0
flag = True
for _ in range(int(frame_count)):
    j += 1
    flag,img=cap.read()
    if j==10:
        j=0
        continue
    else:
        cv2.imwrite('./pic/image{}.jpg'.format(i),img)
        i += 1
video_clips = []
for a in range(i):
    video = VideoFileClip('./pic/image{}.jpg'.format(a))
    video_clips.append(video)
final_video = concatenate(video_clips)
final_video.write_videofile('test.mp4',fps=35,threads=4)