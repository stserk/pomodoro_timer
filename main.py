from tkinter import *
import math
import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound("sound.wav")

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#379777"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="25:00")
    timer_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0

    start_button.config(state=NORMAL)

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    sound.play()  # Play sound when reps change
    window.attributes('-topmost', 1)  # Make the window hover above all others
    window.attributes('-topmost', 0)  # Disable topmost after setting it
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)

    start_button.config(state=DISABLED)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down,count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✅"
        check_marks.config(text=marks)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

tomato = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato)

timer_text = canvas.create_text(100, 130, text="25:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


timer_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

start_button = Button(text="START", highlightthickness=0, bg = GREEN, fg = YELLOW, command=start_timer, font=(FONT_NAME, 10, "bold"))
start_button.grid(column=0, row=2)

reset_button = Button(text="RESET", highlightthickness=0, bg = RED, fg = YELLOW, font=(FONT_NAME, 10, "bold"), command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 14, "bold"))
check_marks.grid(column=1, row=3)



window.mainloop()