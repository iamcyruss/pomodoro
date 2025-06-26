
import tkinter as tk
from tkinter import messagebox

# Constants for the Pomodoro timer
WORK_MINUTES = 25
BREAK_MINUTES = 5
SECONDS = 60

# Global variables
timer_running = False
paused_time = None
timer = None
on_break = False  # Flag to indicate if the timer is currently on a break

# Functions for the Pomodoro timer
def start_timer():
    global timer_running, paused_time, on_break
    timer_running = True
    on_break = False
    if paused_time is not None:
        count_down(paused_time)
    else:
        count_down(WORK_MINUTES * SECONDS)
    
def pause_timer():
    global timer_running, paused_time
    timer_running = False
    paused_time = int(timer_label['text'].split(':')[0]) * 60 + int(timer_label['text'].split(':')[1])
    root.after_cancel(timer)

def stop_timer():
    global timer_running, paused_time, on_break
    timer_running = False
    paused_time = None
    on_break = False
    timer_label.config(text='25:00')
    root.after_cancel(timer)

def timer_complete():
    global on_break
    messagebox.showinfo("Time's up!", "Take a break!" if not on_break else "Break's over, time to work!")
    root.attributes('-topmost', True)  # Bring window to the foreground
    root.attributes('-topmost', False)
    if not on_break:
        on_break = True
        start_break()
    else:
        stop_timer()  # End of break, stop the timer and wait for manual restart

def start_break():
    global timer_running, on_break
    timer_running = True
    count_down(BREAK_MINUTES * SECONDS)

def count_down(count):
    global timer
    if timer_running:
        minutes, seconds = divmod(count, SECONDS)
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        if count > 0:
            timer = root.after(1000, count_down, count - 1)
        else:
            timer_complete()  # Timer complete, handle end of work or break

def close_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Pomodoro Timer")

# Timer label
timer_label = tk.Label(root, text="25:00", font=('Helvetica', 48))
timer_label.pack()

# Buttons
start_button = tk.Button(root, text="Start", command=start_timer)
start_button.pack(side=tk.LEFT)

pause_button = tk.Button(root, text="Pause", command=pause_timer)
pause_button.pack(side=tk.LEFT)

stop_button = tk.Button(root, text="Stop", command=stop_timer)
stop_button.pack(side=tk.LEFT)

close_button = tk.Button(root, text="Close", command=close_app)
close_button.pack(side=tk.LEFT)

# Run the Tkinter event loop
root.mainloop()
