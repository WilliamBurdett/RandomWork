import tkinter
from datetime import datetime
from time import sleep

from utils.threading import Manager


def draw_time(canvas: tkinter.Canvas):
    black = "#fff"
    white = "#000"
    black_bg = True
    while True:
        canvas.delete("all")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if black_bg is True:
            black_bg = False
            canvas_color = white
            text_color = black
        else:
            black_bg = True
            canvas_color = black
            text_color = white
        canvas.configure(bg=canvas_color)
        canvas.create_text(
            5, 15, anchor=tkinter.W, font=("Purisa", 18), text=now, fill=text_color
        )
        sleep(1)


def main():
    queue_manager = Manager()
    top = tkinter.Tk()
    top.configure(bg="black")
    canvas = tkinter.Canvas(
        top,
        bg="white",
        width=230,
        height=30,
    )
    canvas.configure(bg="black")
    queue_manager.put((draw_time, {"canvas": canvas}))

    canvas.grid()
    top.mainloop()


if __name__ == "__main__":
    main()
