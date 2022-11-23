import cv2
from moviepy.editor import *
from multiprocessing import cpu_count
import os
from tqdm import tqdm

def clip_video(name):
    """
    将视频按帧拆分
    :param name:视频路径
    :return: 返回总帧数
    """
    cap = cv2.VideoCapture(name)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 获取视频宽度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 获取视频高度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(frame_count,fps,width,height)
    step = int(frame_count/10)
    i = 0
    flag = True
    for _ in range(int(frame_count)):
        _,img=cap.read()
        cv2.imwrite('./pic/image{}.jpg'.format(i),img)
        i += 1
    # return int(frame_count)

def imgToVideo():
    """
    用来将一系列图片拼接成视频
    :return:
    :param clips:视频总帧数
    """
    # video_clips = []
    # for a in range(clips):
    #     video = VideoFileClip('./pic/image{}.jpg'.format(a))
    #     video_clips.append(video)
    final_video = concatenate(video_clips)
    final_video.write_videofile('test.mp4',fps=120,threads=cpu_count())
    # return video_clips
    image_folder_dir = "./pic/"
    fps = 60
    size = (1080,608)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4','v')
    image_list = sorted([name for name in os.listdir(image_folder_dir) if name.endswith('.jpg')])
    video = cv2.VideoWriter("./test.mp4", fourcc, fps, size, isColor=True)
    for image_name in tqdm(image_list):  # 遍历 image_list 中所有图像并添加进度条
        image_full_path = os.path.join(image_folder_dir, image_name)  # 获取图像的全路经
        image = cv2.imread(image_full_path)  # 读取图像
        image_resize = cv2.resize(image,size)
        video.write(image_resize)  # 将图像写入视频
    video.release()
def imgToVideoForDel(step):
    """
    随机去除一些帧图片后合并成视频，抽帧
    :param clips: 视频总帧数
    :param step: 抽帧步长
    """
    # for i in range(len(video_clips)):
    #     if i%step==0: video_clips.remove(i)
    # final_video = concatenate(video_clips)
    # final_video.write_videofile('test1.mp4', fps=30, threads=cpu_count())
    image_folder_dir = "./pic/"
    fps = 30
    size = (1080, 608)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    image_list = sorted([name for name in os.listdir(image_folder_dir) if name.endswith('.jpg')])
    video = cv2.VideoWriter("./test1.mp4", fourcc, fps, size, isColor=True)
    i = 0
    for image_name in tqdm(image_list):  # 遍历 image_list 中所有图像并添加进度条
        i += 1
        if i%step==0:
            continue
        image_full_path = os.path.join(image_folder_dir, image_name)  # 获取图像的全路经
        image = cv2.imread(image_full_path)  # 读取图像
        image_resize = cv2.resize(image, size)
        video.write(image_resize)  # 将图像写入视频
def fullTohalf():
    """
    全屏尺寸为1920*1080，对于全屏视频，将其转换成1080*608，也就是半屏
    空白部分再以黑色填充，或者使用视频蒙版填充
    """

def splitVoice(name):
    """
    若要分离音频中的人声与伴奏则使用如下命令
    python -m spleeter separate -p spleeter:2stems -o output test.mp3
    :param name:
    """
    video = VideoFileClip(name)
    audio = video.audio
    audio.write_audiofile('test.mp3')


if __name__ == '__main__':
    print(cpu_count())
    name = r'E:\PycharmProjects\TikTokDownload\Download\post\不会颠球\2022-04-04 21.25.57_听说被别人艾特看世界杯会获得三倍幸福___带你感受上世纪的足球魅力___世界杯的一幕幕经典画面你还记得吗__#历届世界杯主题曲_#经典_#2010世界杯__#卡塔尔世界杯_#足球的魅力_#音乐_#足球_.mp4'
    splitVoice(name)
    # clip_video(name)
    # imgToVideo()
    # imgToVideoForDel(10)