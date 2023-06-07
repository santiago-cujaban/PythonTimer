from tkinter import *

app = Tk()
app.geometry('180x50')
app.attributes('-alpha', 0.95) # Transparency
app.attributes('-topmost', True) # Always On Top
app.resizable(False, False) # is Resizable
app.overrideredirect(True) # Remove title bar

def move_window(event):
    # Move window to mouse position
    app.geometry(f'+{event.x_root}+{event.y_root}')

def window_color_change():
    # Change bg color if timer is working
    if timerLabel['text'] == '00:00:00':
        timerLabel.config(bg='red')
        app.configure(bg='red')
    else:
        timerLabel.config(bg='green')
        app.configure(bg='green')

timerLabel = Label(app, text='00:00:00', font=("Consolas bold",20))


timerLabel.pack()
window_color_change()
app.bind('<B1-Motion>', move_window)
app.bind('<Escape>', lambda x: app.quit()) # Quits on ESC being pressed
app.mainloop()