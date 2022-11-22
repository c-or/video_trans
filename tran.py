import cv2
from moviepy.editor import *

def clip_video(name):
    cap = cv2.VideoCapture(name)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(frame_count,fps)
    step = int(frame_count/10)
    i,j = 0,0
    flag = True
    for _ in range(int(frame_count)):
        j += 1
        _,img=cap.read()
        cv2.imwrite('./pic/image{}.jpg'.format(i),img)
    return frame_count

def imgToVideo(clips):
    video_clips = []
    for a in range(clips):
        video = VideoFileClip('./pic/image{}.jpg'.format(a))
        video_clips.append(video)
    final_video = concatenate(video_clips)
    final_video.write_videofile('test.mp4',fps=60,threads=4)

def imgToVideoForDel(clips,step):


if __name__ == '__main__':
    name = '2022-11-21 16.45.11.mp4'
    clips = clip_video(name)
    imgToVideo(clips)