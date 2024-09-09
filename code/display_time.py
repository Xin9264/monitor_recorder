import tkinter as tk
import datetime
import threading

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
display_time()