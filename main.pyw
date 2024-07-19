from tkinter import *
from tkinter import ttk
from threading import Thread
import keyboard, time
from ttkthemes import ThemedStyle

from tkinter.scrolledtext import ScrolledText

version = '1.4 Blix'

window = Tk()

window.title('HTexter v'+version)
window.geometry("650x300")
window.configure(background='#464646')

style = ThemedStyle(window)
style.set_theme("equilux")

# VARIABLES

str_delay = 3
write_delay = 20
delay = 100
WorkBool = False
repeat = IntVar()
mass = []

# SCRIPTS

def text_edit(event):
    global mass
    mass = text.get('1.0', END).split('\n')

def typing(delay, mass, WorkBool, write_delay):
    for set in mass[:len(mass)-1]:
            if WorkBool:
                if not set.startswith('#'):
                    keyboard.send('enter')
                    keyboard.write(set, write_delay/1000)
                    keyboard.send('enter')
                    time.sleep(delay/1000)
                else:
                    pass
            else:
                break

def texter_run():
    global delay, mass, str_delay, WorkBool, write_delay, repeat
    time.sleep(str_delay)
    if repeat.get() == 0:
        typing(delay, mass, WorkBool, write_delay)
    if repeat.get() == 1:
        while True:
            typing(delay, mass, WorkBool, write_delay)
            if repeat.get() == 0 or not WorkBool:
                break

def record_run():
    global recorded_macros
    window.withdraw()
    recorded_macros = keyboard.record("f5")
    del recorded_macros[-1]
    print(recorded_macros)
    window.deiconify()

def macros_run():
    global recorded_macros
    window.withdraw()
    time.sleep(.3)
    keyboard.play(recorded_macros)
    time.sleep(.3)
    window.deiconify()


# CALLBACKS
        
def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0

    if event.keycode==65 and  ctrl and event.keysym.lower() != "a": 
        event.widget.event_generate("<<SelectAll>>")

    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def delay_callback(P):
    if str.isdigit(P) or P == "":
        if len(P) <= 4 and len(P) >= 2:
            return True
        else:
            return False
    else:
        return False
    
def change_str_delay_callback(value):
    new_value = round(float(value))
    delay_sec_label["text"] = f'{new_value} сек'
    global str_delay
    str_delay = new_value

def change_delay_callback(value):
    new_value = round(float(value)/50)*50
    if new_value == 0:
        new_value = 10
    wait_label["text"] = f'{new_value} мс'
    global delay
    delay = new_value

def change_write_delay_callback(value):
    new_value = round(float(value)/5)*5
    if new_value == 0:
        new_value = 2
    write_delay_label["text"] = f'{round(1000/new_value)} символов в секунду'
    global write_delay
    write_delay = new_value

def start_callback():
    global WorkBool
    WorkBool = True
    thr = Thread(target=texter_run, daemon=True)
    thr.start()

def stop_callback():
    global WorkBool
    WorkBool = False

def record_callback():
    thr = Thread(target=record_run, daemon=True)
    thr.start()

def play_callback():
    thr = Thread(target=macros_run, daemon=True)
    thr.start()


vcmd = window.register(delay_callback)

# WIDGETS

version_label = ttk.Label(window, text=f'v{version}')
wait_label = ttk.Label(window, text='100 мс')
delay_sec_label = ttk.Label(window, text='3 сек')
wait_delay_label = ttk.Label(window, text='Интервал')
pause_label = ttk.Label(window, text='Пауза')
record_label = ttk.Label(window, text='Макросы')
write_delay_label = ttk.Label(window, text = '50 символов в секунду')

text = ScrolledText(window, width=50)

queue_progressbar = ttk.Progressbar(orient="horizontal")

pause_scale = ttk.Scale(window, orient=HORIZONTAL, from_=10.0, to=3000.0, value=100, command=change_delay_callback)
wait_delay_scale = ttk.Scale(window, orient=HORIZONTAL, from_=1.0, to=10.0, value=3, command=change_str_delay_callback)
write_delay_scale = ttk.Scale(window, orient=HORIZONTAL, from_=1.0, to=100.0, value=50, command=change_write_delay_callback)

start_button = ttk.Button(window, command = start_callback, text = "Запуск")
stop_button = ttk.Button(window, command = stop_callback, text = 'Стоп')
record_button = ttk.Button(window, command = record_callback, text = 'Запись (F5)')
play_button = ttk.Button(window, command = play_callback, text = 'Запуск')

repeat_checkbox = ttk.Checkbutton(window, text='Автоповтор', variable=repeat)

# PACKS

version_label.pack(side=BOTTOM ,anchor=SW) # Label version

# PLACES

pause_scale.place( # Pause scale
    x = 5,
    y = 25,
    width = 200
)

wait_label.place( # Label: % мс
    x = 160,
    y = 5
)

wait_delay_scale.place( # String delay Scale
    x = 5,
    y = 70,
    width = 200
)

delay_sec_label.place( # Label: % сек
    x = 160,
    y = 50
)

pause_label.place( # Label: Пауза
    x = 5,
    y = 50
)

wait_delay_label.place( # Label: Интервал
    x = 5,
    y = 5
)

write_delay_label.place( # Label: % символов в секунду
    x = 5,
    y = 100
)
write_delay_scale.place( # Write delay scale
    x = 5,
    y = 120,
    width = 200
)

repeat_checkbox.place( # Repeats check
    x = 5,
    y = 150
)

text.place( # Main text ScrolledText
    x = 210,
    y = 0,
    width = 440,
    height = 300
)

start_button.place( # Button: Запуск : start_callback
    x = 10,
    y = 185,
    width = 95
)

stop_button.place( # Button: Стоп : stop_callback
    x = 110,
    y = 185,
    width = 95
)

record_label.place( # Label: Макросы
    x = 5,
    y = 220
)

record_button.place( # Button: Запись : record_callback
    x = 20,
    y = 245
)

play_button.place( # Button: Запуск : play_callback
    x = 110,
    y = 245
)

# BINDS

window.bind_all("<Key>", _onKeyRelease, "+")

text.bind('<KeyRelease>', text_edit)

# LOOP

window.mainloop()