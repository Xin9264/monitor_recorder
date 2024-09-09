from ffmpeg_record_mul import start_record
import subprocess
import time
from threading import Thread, Event
from detect_monitor import get_all_monitors_resolutions
from ffmpeg_record_mul import find_time
import os
from move_file import move_txt_files_from_previous_directory
import tkinter as tk

script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)

stop_event = Event()
def stop_recording_from_gui(root):
    stop_event.set()
    time.sleep(3)
    root.destroy()


def create_gui():
    root = tk.Tk()
    root.title("Recording Controller")

    stop_button = tk.Button(root, text="Stop Recording", command=lambda: stop_recording_from_gui(root))
    stop_button.pack(pady=20)

    root.mainloop()

def main(time_stamp):
    monitors = get_all_monitors_resolutions()

    record_thread = Thread(target=start_record, args=(monitors, time_stamp, stop_event))
    record_thread.start()
    show_color_process = subprocess.Popen(["config_file\show_color.exe"])
    show_color_process.wait()
    create_gui()
    record_thread.join()


if __name__ == "__main__":
    time_stamp = find_time()
    save_directory = f'./save/{time_stamp}'
    exe_path = r"config_file\keycastow.exe"
    process = subprocess.Popen(exe_path)
    time.sleep(0.5)
    print("Keyboard&mouse listening started!")
    # show_color_process = subprocess.Popen(["config_file\show_color.exe"])
    main(time_stamp)
    time.sleep(1)

    
    # show_color_process.wait()
    process.terminate()
    # move_txt_files(time_stamp)
    # move_txt_files_from_previous_directory()