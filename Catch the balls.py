from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, ttk

canvas_width = 900
canvas_height = 500

root = Tk()
root.title("Catch The Ball")
c = Canvas(root, width=canvas_width, height=canvas_height, background="azure2")
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="peru", width=0)
c.create_oval(-100, -100, 130, 130, fill='medium aquamarine', width=0)
c.pack()

color_cycle = cycle(["blue", "green", "pink", "orange", "cyan"])
egg_width = 55
egg_height = 60
egg_score = 10
egg_speed = 100
egg_interval = 3000
difficulty = 1
catcher_color = "white"
catcher_width = 200
catcher_height = 0
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height -30
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2, start=100, extent=400, style="pieslice", outline=catcher_color, width=3)
game_font = font.nametofont("TkHeadingFont")

game_font.config(size=15)




score = 0
score_text = c.create_text(10, 20, anchor="nw", font=game_font, fill="IndianRed4", text="Score: "+ str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width-890, 50, anchor="nw", font=game_font, fill="IndianRed4", text="Lives: "+ str(lives_remaining))

eggs = []

def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x+egg_width, y+egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))

def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)
root.mainloop()