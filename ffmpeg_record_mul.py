import subprocess
import keyboard
import datetime
import threading
import tkinter as tk
import time
from detect_monitor import enum_display_monitors
import os


def find_time():
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return time_stamp

time_stamp = find_time()


def display_time(running):
    def show_time():
        if not running.is_set():
            return  # Exit if the running flag is False
        # Create the window only when showing the time
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.geometry("150x30+0+0")  # Small window at the top-left corner

        time_label = tk.Label(root, font=("Arial", 16), fg='black')
        time_label.pack()

        current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Time accurate to milliseconds
        time_label.config(text=current_time)

        root.after(1000, root.destroy)

        # Run the window's main loop
        root.mainloop()

    def update_time():
        if running.is_set():
            show_time()
            # Schedule to show time every minute
            threading.Timer(30, update_time).start()

    # Start the time update process
    update_time()


def record_screen(monitor, output_filename, fps=60):
    ffmpeg_path = r"config_file\ffmpeg\bin\ffmpeg.exe"
    cmd = [
        ffmpeg_path,
        '-filter_complex', 'ddagrab=0,hwdownload,format=bgra',
        '-c:v', 'libx264',
        '-crf', '20',
        '-r', '60',
        output_filename
    ]
    return subprocess.Popen(cmd)

# Start the FFmpeg process
def start_record(monitors):
    running = threading.Event()
    running.set()

    # Start the time display thread 
    time_display_thread = threading.Thread(target=display_time, args=(running,))
    time_display_thread.start()
    time_stamp = find_time()
    monitors = enum_display_monitors()
    print(monitors)
    save_directory = './save'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    processes = []
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    for i, monitor in enumerate(monitors):
        monitor_idx = monitor["monitor_index"]
        left = monitor["left"]
        top = monitor["top"]
        right = monitor["right"]
        bottom = monitor["bottom"]
        # print(monitor)
        output_filename = f'./save/l{left}_r{right}_t{top}_b{bottom}_{time_stamp}.mkv'
        # Define the FFmpeg command for each monitor
        ffmpeg_command = [
            'ffmpeg',
            '-filter_complex', f'ddagrab= {str(monitor_idx)},hwdownload,format=bgra',
            '-c:v', 'libx264',
            '-crf', '20',
            '-r', '60',
            '-y',  # Overwrite existing files
            output_filename
        ]
        process = subprocess.Popen(ffmpeg_command)
        processes.append(process)
        print(f"Recording started on monitor {i + 1}. Output: {output_filename}")

    print("Recording started on all monitors. Press 'Print Screen' key to stop.")

    # Listen for the 'Print Screen' key press
    try:
        keyboard.wait('ctrl+f7')
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        running.clear()
        # Terminate all FFmpeg processes
        for process in processes:
            process.terminate()
            process.wait()
        print(f"Recording stopped and saved for all monitors.")
        # stitch_videos(monitors, timestamp)



import subprocess

# def stitch_videos(monitors, timestamp):
#     max_right = max(monitor['right'] for monitor in monitors)
#     max_bottom = max(monitor['bottom'] for monitor in monitors)
#     canvas_width = max_right
#     canvas_height = max_bottom
#     input_files = ""
#     overlay_commands = ""
#     for i, monitor in enumerate(monitors):
#         input_files += f" -i monitor_{monitor['monitor_index']+1}_{time_stamp}.mkv"
#         if i == 0:
#             overlay_commands += f"[0:v]pad={canvas_width}:{canvas_height}[base];"
#         else:
#             overlay_commands += f"[base][{i}:v]overlay={monitor['left']}:{monitor['top']}[base];"
#         # Finalize the command
#     overlay_commands = overlay_commands.rstrip(";")  # Remove the last semicolon
#     command = f"ffmpeg{input_files} -filter_complex \"{overlay_commands}\" -map \"[base]\" out_{time_stamp}.mkv"
#     # cmd = f"ffmpeg {inputs} -filter_complex \"{filter_complex}\" -y {output_file}"
#     subprocess.call(command, shell=True)
#     print("DONE!")
