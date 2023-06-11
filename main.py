from tkinter import *
import pygetwindow as pw

app = Tk()
app.geometry('180x50')
app.attributes('-alpha', 0.5) # Transparency
app.attributes('-topmost', True) # Always On Top
app.resizable(False, False) # Is Resizable
app.overrideredirect(True) # Removes title bar
context_menu = Menu(app, tearoff = 0)

programs = []
hours, minutes, seconds = 0,0,0
isActive:bool = False

# FUNCTIONS

def move_window(event):
    app.geometry(f'+{event.x_root-95}+{event.y_root-20}')

def set_timer_text(newText:str):
    timerLabel.config(text = newText)

def set_isActive(status:bool):
    global isActive
    isActive = status

def remove_program(name):
    programs.remove(name)
    context_menu.delete(name)

def add_program():
    pid = pw.getActiveWindowTitle()
    if pid not in programs and pid != 'tk' and pid != ' ' and pid != 'Task Switching':
        programs.append(pid)
        context_menu.add_command(label=pid, command = lambda: remove_program(pid))
    else:
        time_format()

def update_window_color():
    global isActive
    if not isActive:
        timerLabel.config(bg='red')
        app.configure(bg='red')
    else:
        timerLabel.config(bg='green')
        app.configure(bg='green')
    
    if timerLabel['text'] == 'Waiting':
        timerLabel.config(bg='blue')
        app.configure(bg='blue')
    
    app.after(100, update_window_color)

def time_format():
    global hours, minutes, seconds
    hours_str, minutes_str, seconds_str = '','',''
    seconds_str = f'0{seconds}' if seconds <= 9 else f'{seconds}'
    minutes_str = f'0{minutes}' if minutes <= 9 else f'{minutes}'
    hours_str = f'0{hours}' if hours <= 9 else f'{hours}'
    set_timer_text(f'{hours_str}:{minutes_str}:{seconds_str}')

def reset_clock():
    global hours, minutes, seconds
    hours = 0
    minutes = 0
    seconds = 0
    time_format()

def clock():
    global hours, minutes, seconds, isActive
    if isActive:
        if seconds == 59:
            seconds = 0
            if minutes == 59:
                minutes = 0
                hours += 1
            else: minutes += 1
        else: seconds += 1
        time_format()

def clock_verification():
    pid = pw.getActiveWindowTitle()
    if pid in programs:
        set_isActive(True)
    else:
        set_isActive(False)
    clock()
    app.after(1000, clock_verification)
    
# CONTEXT MENU
context_menu.add_command(label="Reset Time", command=reset_clock)
context_menu.add_command(label="Add Program", command= lambda: app.after(2500,add_program) and set_timer_text("Waiting"))
context_menu.add_command(label="Quit", command=app.quit)
context_menu.add_separator()

# TIMER
timerLabel = Label(app, text=f'00:00:00', font=("Consolas bold",20))
timerLabel.pack()

update_window_color()
clock_verification()
app.bind('<B1-Motion>', move_window)
app.bind('<Button-3>', lambda event: context_menu.post(event.x_root, event.y_root))
app.bind('<Escape>', lambda x: app.quit()) # Quit on ESC being pressed
app.mainloop()