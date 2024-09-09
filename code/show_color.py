import tkinter as tk
from threading import Thread, Event
from detect_monitor import enum_display_monitors

close_event = Event()

def show_color_block_on_monitor(monitor, root):
    def on_key_press(event):
        if event.keysym in ('Control_L', 'Control_R'):
            close_event.set()
            root.quit()

    block_width, block_height = 800, 450

    monitor_width = monitor['right'] - monitor['left']
    monitor_height = monitor['bottom'] - monitor['top']
    
    x_position = int(monitor['left'] + (monitor_width - block_width) / 2)
    y_position = int(monitor['top'] + (monitor_height - block_height) / 2)

    window = tk.Toplevel(root)
    window.geometry(f"{block_width}x{block_height}+{x_position}+{y_position}")
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    canvas = tk.Canvas(window, width=block_width, height=block_height)
    canvas.pack()

    rgb_color = (173, 216, 230)
    color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
    label = tk.Label(window, text="先用鼠标点我，然后按下ctrl", font=("等线", 24), bg=color, fg='black')
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    canvas.create_rectangle(0, 0, block_width, block_height, fill=color, outline=color)

    window.bind("<Control_L>", on_key_press)
    window.bind("<Control_R>", on_key_press)

    def check_close_event():
        if close_event.is_set():
            window.destroy()
        else:
            window.after(100, check_close_event)

    window.after(100, check_close_event)

def show_color_block():
    monitors = enum_display_monitors()
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    for monitor in monitors:
        show_color_block_on_monitor(monitor, root)

    root.mainloop()

if __name__ == "__main__":
    show_color_block()
