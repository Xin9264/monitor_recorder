import subprocess
import keyboard
import datetime
import threading
import tkinter as tk
import time
from detect_monitor import get_all_monitors_resolutions
import os
from evaluate_video import validate_video_file, show_error_message

def find_time():
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return time_stamp


def start_record(monitors, time_stamp, stop_event):
    running = threading.Event()
    running.set()

    monitors = get_all_monitors_resolutions()
    print(monitors)

    save_directory = os.path.join('..', 'save', time_stamp)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    processes = []
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_files = []
    for i, monitor in enumerate(monitors):
        monitor_idx = monitor["monitor_index"]
        left = monitor["left"]
        top = monitor["top"]
        right = monitor["right"]
        bottom = monitor["bottom"]
        output_filename = save_directory + f'/l{left}_t{top}_r{right}_b{bottom}_{time_stamp}.mp4'

        ffmpeg_command = (
            f'.\\config_file\\ffmpeg\\bin\\ffmpeg.exe '
            f'-filter_complex "ddagrab={str(monitor_idx)},hwdownload,format=bgra" '
            f'-pix_fmt yuv420p '  # 改变像素格式为更通用的 yuv420p
            f'-c:v libx264 -preset ultrafast -crf 24 -r 60 -y "{output_filename}"'
        )
        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, shell=True)
        processes.append(process)
        output_files.append(output_filename)
        print(f"Recording started on monitor {i + 1}. Output: {output_filename}")

    print("Recording started on all monitors. Press 'Print Screen' key to stop.")

    # stop_event = threading.Event()
    # stop_event.wait()
    # running.clear

    # Define a function to stop recording
    def stop_recording():
        stop_event.set()


    keyboard.add_hotkey('ctrl+alt+s', stop_recording)
    keyboard.add_hotkey('print_screen', stop_recording)
    keyboard.add_hotkey('win+j', stop_recording)

    # Wait for either of the keys to be pressed
    stop_event.wait()

    # After hotkey is pressed
    running.clear()

    # Terminate all FFmpeg processes
    for process in processes:
        process.stdin.write(b'q')
        process.stdin.flush()
        process.wait()
    for file in output_files:
        if not validate_video_file(file):
            show_error_message()

    print(f"Recording stopped and saved for all monitors.")

