from ffmpeg_record_mul import start_record
import subprocess
import time
from threading import Thread
from detect_monitor import enum_display_monitors
import os
import shutil


def move_txt_files():
    # 当前目录
    current_directory = os.getcwd()
    # 目标目录
    save_directory = './save'
    
    # 如果目标目录不存在，创建它
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # 遍历当前目录下的所有文件
    for filename in os.listdir(current_directory):
        # 仅处理 .txt 文件
        if filename.endswith('.txt'):
            # 源文件路径
            source_file = os.path.join(current_directory, filename)
            # 目标文件路径
            destination_file = os.path.join(save_directory, filename)
            
            # 移动文件
            shutil.move(source_file, destination_file)
            print(f'Moved: {filename}')

    # print("All .txt files have been moved to './SAVE'.")


def main():
    monitors = enum_display_monitors()

    # 启动 show_color_block.exe
    show_color_process = subprocess.Popen(["config_file\show_color.exe"])
    
    # 启动录屏的线程
    record_thread = Thread(target=start_record, args=(monitors,))
    record_thread.start()

    # 等待录屏线程完成
    record_thread.join()

    # 等待 show_color.exe 完成
    show_color_process.wait()

if __name__ == "__main__":
    exe_path = r"config_file\keycastow.exe"
    process = subprocess.Popen(exe_path)
    time.sleep(0.5)
    print("Keyboard&mouse listening started!")
    main()
    process.terminate()
    move_txt_files()
