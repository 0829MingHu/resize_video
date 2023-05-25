# -*- coding: UTF-8 –*-
import os
import subprocess
import datetime
from enum import Enum
from tqdm import tqdm

# 对视频操作的枚举
class FFmpegOperatorEnum(Enum):
    Modify_Video_Resolution = 0
    Modify_Video_BitRate = 1
    Modify_Video_FrameRate = 2


class FFmpegBatchConversionVideo:
    m_TotalConversionFiles = 0
    m_TotalFiles = 0
    m_SupportVideoFormat = ['.mp4','.avi']
    m_FFmpegOperatorEnum = None

    m_Video_Resolution = ''
    m_Video_BitRate = ''
    m_Video_FrameRate = ''

    def __init__(self,videoformat = ['.mp4','.avi'],ffmpegOperatorEnum = FFmpegOperatorEnum.Modify_Video_Resolution):
        self.m_SupportVideoFormat = videoformat
        self.m_FFmpegOperatorEnum = ffmpegOperatorEnum
        pass

    def ConvertBatchVideos(self,inputPath,outputPath):
        if not os.path.isdir(outputPath):
            os.mkdir(outputPath)

        #for files in os.listdir(inputPath):
        for files in tqdm(os.listdir(inputPath)): #增加tqdm进度条
            input_name = os.path.join(inputPath,files)
            output_name = os.path.join(outputPath,files)

            # 如果输入路径为文件
            if os.path.isfile(input_name):
                dirPath = (os.path.abspath(os.path.dirname(output_name)))
                # 如果不存在输出文件夹则创建该文件夹
                if not os.path.isdir(dirPath):
                    os.mkdir(dirPath)
                # 判断输入视频的后缀名是否在支持的列表之中
                #if os.path.split(input_name)[-1].lower() in self.m_SupportVideoFormat:
                if input_name.split('.')[1].lower() in self.m_SupportVideoFormat:
                    # 修改视频分辨率
                    if self.m_FFmpegOperatorEnum == FFmpegOperatorEnum.Modify_Video_Resolution:
                        self.ModifyVideoResolution(input_name,output_name)
                    # 修改视频码率
                    elif self.m_FFmpegOperatorEnum == FFmpegOperatorEnum.Modify_Video_BitRate:
                        self.ModifyVideoBitRate(input_name,output_name)
                    # 修改视频帧率
                    elif self.m_FFmpegOperatorEnum == FFmpegOperatorEnum.Modify_Video_FrameRate:
                        self.ModifyVideoFrameRate(input_name,output_name)
                    else:
                        pass
                self.m_TotalFiles += 1

            # 如果输入路径为文件夹
            else:
                # 如果输出文件夹不存在则创建文件夹
                if not os.path.isdir(output_name):
                    os.mkdir(output_name)
                # 递归
                self.ConvertBatchVideos(input_name,output_name)

    def ModifyVideoResolution(self,videoin,videoout):
        t_ffmpegcmdline = 'ffmpeg -i "{}"  -vf scale={} -threads 4 "{}" -hide_banner'.format(videoin,self.m_Video_Resolution ,videoout)
        returncode =subprocess.Popen(t_ffmpegcmdline, shell=True)
        self.m_TotalConversionFiles += 1

    def ModifyVideoBitRate(self,videoin,videoout):
        t_ffmpegcmdline = 'ffmpeg -i "{}"  -b:v {} -threads 4 "{}" -hide_banner'.format(videoin, self.m_Video_BitRate ,videoout)
        returncode = subprocess.call(t_ffmpegcmdline)
        self.m_TotalConversionFiles += 1

    def ModifyVideoFrameRate(self,videoin,videoout):
        t_ffmpegcmdline = 'ffmpeg -r {} -i "{}"  -threads 4 "{}" -hide_banner'.format(self.m_Video_FrameRate,videoin, videoout)
        returncode = subprocess.call(t_ffmpegcmdline)
        self.m_TotalConversionFiles += 1

if __name__ == '__main__':
    inputDir = r'/home/chenj0g/medicnet/dataset/videos'
    outputDir = r'/home/chenj0g/medicnet/dataset/resize_videos'

    # 记录转换总时间
    opeartion_start_time = datetime.datetime.now()

    # 批量修改视频帧率
    # ffmpegBatchConversionVideo = FFmpegBatchConversionVideo(['mp4','avi'],ffmpegOperatorEnum=FFmpegOperatorEnum.Modify_Video_FrameRate)
    # ffmpegBatchConversionVideo.m_Video_FrameRate = '60'
    # ffmpegBatchConversionVideo.ConvertBatchVideos(inputDir,outputDir)

    # 批量修改视频码率
    # ffmpegBatchConversionVideo = FFmpegBatchConversionVideo(['mp4','avi'],ffmpegOperatorEnum=FFmpegOperatorEnum.Modify_Video_BitRate)
    # ffmpegBatchConversionVideo.m_Video_BitRate = '10000k'
    # ffmpegBatchConversionVideo.ConvertBatchVideos(inputDir,outputDir)

    # 批量修改视频分辨率
    ffmpegBatchConversionVideo = FFmpegBatchConversionVideo(['mp4','avi'],ffmpegOperatorEnum=FFmpegOperatorEnum.Modify_Video_Resolution)
    ffmpegBatchConversionVideo.m_Video_Resolution = '256:256'
    ffmpegBatchConversionVideo.ConvertBatchVideos(inputDir,outputDir)

    opeartion_end_time = datetime.datetime.now()
    opeartion_duration = opeartion_end_time - opeartion_start_time

    print('转换完成，共有视频文件{}个，转换视频文件{}个，共耗时{}'.format(ffmpegBatchConversionVideo.m_TotalFiles,ffmpegBatchConversionVideo.m_TotalConversionFiles,opeartion_duration))

