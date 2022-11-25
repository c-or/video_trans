import cv2
from moviepy.editor import *
from multiprocessing import cpu_count
import os
from tqdm import tqdm
from moviepy.video.io.preview import preview
from moviepy.video.tools.drawing import circle

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
    # audio.write_audiofile('test.mp3')


def sub_video(name,seg,gap):
    clip = VideoFileClip(name)
    duration, size = clip.duration, clip.size
    print(duration)
    step = int(duration/seg)
    loc = 0
    i = 0
    while loc<duration-1:
        i += 1
        loc = step*i
        clip1 = clip.cutout(loc,loc+gap)
        clip = clip1
    # preview(clip)
    duration = clip.duration
    print(duration)
    return clip

def modify_speed(clip,speed):
    """
    调整视频倍速
    :param clip: 视频切片
    :param speed: 速度倍数
    :return: 返回处理后的视频
    """
    clip1 = clip.fl_time(lambda t: t*speed,apply_to=['mask','audio'])
    clip1 = clip1.set_duration(clip.duration/speed)
    return clip1

def add_bkaudio(clip,factor):
    """
    在视频原声中混入白噪音
    :param clip: 需要混音的视频
    :param factor: 白噪声的音量系数
    """
    duration = clip.duration
    src_audio = clip.audio
    fps = src_audio.fps
    audio_clip = AudioFileClip('./bksound/51miz-S276571-754C2178.mp3')
    audio_clip = afx.audio_loop(audio_clip,duration=duration)
    audio_clip = audio_clip.volumex(factor)
    mix_audio = CompositeAudioClip([src_audio,audio_clip])
    mix_audio = mix_audio.set_fps(fps)
    clip = clip.set_audio(mix_audio)
    return clip
    # clip.write_videofile('test1.mp4',threads=16)
    # mix_audio.write_audiofile('test.mp3',fps=fps)


if __name__ == '__main__':
    name = r'D:\py_project\TikTokDownload\Download\post\张非人\2022-11-08 19.05.03农村田间做个蒜蓉猪肺培根卷_大片猪肺真的美味解馋_DOU_小助手__抖音小助手_#抖音美食创作者_#户外美食.mp4'
    clip = sub_video(name,20,0.1)
    # print(clip.duration)
    # # clip.write_videofile('test.mp4',threads=4)
    # clip = modify_speed(clip,0.9)
    # print(clip.duration)
    # clip.write_videofile('test1.mp4',threads=4)
    # clip.close()
    # 遮罩应该是一个类似于基座的东西，将视频放在上面，视频的可见范围就会随着基座的变化而变化
    # 而不是一个类似蒙版一样放在放在上面的东西
    clip = add_bkaudio(clip,1)
    clip = clip.fx(vfx.colorx,1.1).fx(vfx.fadein,5).fx(vfx.fadeout,5)
    # clip.write_videofile('test1.mp4',threads=8)
    # VideoClip().without_audio
    clip_mask = clip.copy().rotate(180).set_opacity(0.2).without_audio()
    clip = CompositeVideoClip([clip,clip_mask])
    clip.write_videofile('test1.mp4',threads=8)


