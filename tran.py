import random
import time
import cv2
from moviepy.editor import *
from multiprocessing import cpu_count
import os
from tqdm import tqdm
from moviepy.video.io.preview import preview
from moviepy.video.tools.drawing import circle
import youdao
import os
import itertools
import hashlib
import connector

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
    # print(duration)
    step = int(duration/seg)
    loc = 0
    i = 0
    while loc<duration-1:
        i += 1
        loc = step*i
        clip1 = clip.cutout(loc,loc+gap)
        clip = clip1
        duration = clip.duration
    # preview(clip)
    clip = clip.subclip(gap*2,clip.duration-gap*2)
    duration = clip.duration
    # print(duration)
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

def color(clip,rx,fade):
    clip = clip.fx(vfx.colorx,rx).fx(vfx.fadein,fade).fx(vfx.fadeout,fade)
    return clip

def add_mask(clip,text,size) -> VideoClip:
    clip_mask = (TextClip(text, fontsize=size)
                 # .set_position(lambda t: (150 * t, 50 * t))  # 随着时间移动
                 .set_position('center')  # 水印的位置
                 .set_duration(clip.duration)  # 水印持续时间
                 .set_opacity(0.1))
    clip = CompositeVideoClip([clip, clip_mask])
    return clip

def get_name(dir):
    path = dir
    file_name_list = os.listdir(path)
    file_name = str(file_name_list)
    file_names = file_name.replace("[", "").replace("]", "").replace("'", "").split(',')
    return file_names

def random_factor(num):

    seg = [20,30,40,50,60]
    gap = [0.06,0.08,0.1,0.12]
    speed = [0.9,0.95,1,1.05,1.1]
    volume = [0.2,0.3,0.4]
    rx = [0.95,1,1.05]
    fade = [2,3,4,5]
    text_size = [100,110,120,130,140,150]
    factors = list(itertools.product(seg,gap,speed,volume,rx,fade,text_size))
    # print(len(factors))
    factors = random.sample(factors,num)
    return factors

def mix_file_factor(files,num):
    file_factors = []
    for file in files:
        salt = time.time_ns()
        salt_parent_name = str(salt) + file
        # 有中文所以需要编码
        parent_name_md5 = hashlib.md5(salt_parent_name.encode()).hexdigest()
        factors = random_factor(num)
        a = [(file,parent_name_md5)]
        file_factors += list(itertools.product(a,factors))
    return file_factors

def db_insert(fields,data_list):
    db = connector.mysql_conn()
    db.insert('tk_video_info', fields, data_list)

def schedule(item,dir,dest_dir):
    try:
        file = item[0][0].strip()
        parent_name_md5 = item[0][1]
        path = dir+'\\'+file
        factors = item[1]

        suffix = '_'.join([str(x) for x in factors])
        tip = file.index('#')
        name_zh = file[19:tip]

        salt = time.time_ns()
        name_en = youdao.youdao(name_zh.replace('_',''))
        name = name_zh+suffix
        salt_child_name = str(salt)+name
        # 有中文所以需要编码
        child_name_md5 = hashlib.md5(salt_child_name.encode()).hexdigest()
        seg = factors[0]
        gap = factors[1]
        speed = factors[2]
        volume = factors[3]
        rx = factors[4]
        fade = factors[5]
        text_size = factors[6]
        text = time.strftime('%Y%m%d')
        clip = sub_video(path,seg,gap)
        clip = modify_speed(clip,speed)
        clip = add_bkaudio(clip,volume)
        clip = color(clip,rx,fade)
        clip = add_mask(clip,text,text_size)
        clip.write_videofile('./out/'+name+'.mp4')
        # now = time.strftime('%Y-%m-%d %H:%M:%S')
        meta_uuid = parent_name_md5
        uuid = child_name_md5
        meta_flag = 0
        operation_type = '美食'
        video_path = dest_dir+'\\'+name+'.mp4'
        title = name_en
        tags = 'food'
        description = None
        state = 1
        prority = 0
        data = [meta_uuid,uuid,meta_flag,operation_type,video_path,title,tags,description,state,prority]
        fields =['meta_uuid','uuid','meta_flag','operation_type','video_path','title','tags','description','state','priority']
        db_insert(fields,data)

        clip.close()
    except Exception as e:
        print(e)
        clip.close()


if __name__ == '__main__':
    dir = 'E:\PycharmProjects\TikTokDownload\Download\post\米其林🤏🏻未认证西点师'
    dest_dir = r'F:\creat_video\yanse\20221117\美食'
    files = get_name(dir)
    file_factors = mix_file_factor(files,50)
    # file_factors = zip_file_factor(file_factors,dir,dest_dir)
    for item in file_factors:
        schedule(item,dir,dest_dir)




