import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def validate_video_file(video_file):
    # 检查文件是否存在
    if not os.path.exists(video_file):
        print(f"Video file {video_file} does not exist.")
        return False
    
    # 检查文件大小是否合理（大于 0 字节）
    file_size = os.path.getsize(video_file)
    if file_size == 0:
        print(f"Video file {video_file} is empty.")
        return False
    print(f"Video file size: {file_size} bytes.")
    
    # 使用 ffprobe 检查视频时长
    try:
        result = subprocess.run(
            ['.\\config_file\\ffmpeg\\bin\\ffprobe.exe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration = float(result.stdout.decode('utf-8').strip())
        print(f"Video duration: {duration} seconds.")
        if duration == 0:
            print(f"Video file {video_file} has zero duration.")
            return False
    except Exception as e:
        print(f"Error checking video duration: {e}")
        return False

    # 使用 ffprobe 检查视频分辨率
    try:
        result = subprocess.run(
            ['.\\config_file\\ffmpeg\\bin\\ffprobe.exe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', video_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        resolution = result.stdout.decode('utf-8').strip()
        print(f"Video resolution: {resolution}")
        if not resolution:
            print(f"Failed to get resolution for {video_file}.")
            return False
    except Exception as e:
        print(f"Error checking video resolution: {e}")
        return False
    
    # 使用 ffprobe 检查视频帧率
    try:
        result = subprocess.run(
            ['.\\config_file\\ffmpeg\\bin\\ffprobe.exe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', video_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        frame_rate = result.stdout.decode('utf-8').strip()
        print(f"Video frame rate: {frame_rate} fps")
        if not frame_rate:
            print(f"Failed to get frame rate for {video_file}.")
            return False
    except Exception as e:
        print(f"Error checking video frame rate: {e}")
        return False

    # 使用 ffprobe 检查视频编码格式
    try:
        result = subprocess.run(
            ['.\\config_file\\ffmpeg\\bin\\ffprobe.exe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', video_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        codec = result.stdout.decode('utf-8').strip()
        print(f"Video codec: {codec}")
        if not codec:
            print(f"Failed to get codec for {video_file}.")
            return False
    except Exception as e:
        print(f"Error checking video codec: {e}")
        return False
    
    print(f"Video file {video_file} seems to be valid.")
    return True

def show_error_message():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showerror("Validation Failed", "Video file validation failed.")
    root.destroy()

# # 示例：验证录制的文件是否完整
# video_file = ".\\save\\2024-09-04_17-47-29\\l0_r1920_t0_b1080_2024-09-04_17-47-29.mkv"  # 替换为录制后生成的视频文件路径
# if not validate_video_file(video_file):
#     print("Video file validation passed.")
# else:
#     show_error_message()
