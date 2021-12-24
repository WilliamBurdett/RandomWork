import tkinter
from datetime import datetime
from time import sleep

from utils.threading import Manager


def draw_time(canvas: tkinter.Canvas):
    while True:
        canvas.delete("all")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        canvas.create_text(
            5, 15, anchor=tkinter.W, font=("Purisa", 18), text=now, fill="#fff"
        )
        sleep(5)


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
