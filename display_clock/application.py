import tkinter
from datetime import datetime
from random import randint
from time import sleep

from utils.threading import Manager


def draw_time(canvas: tkinter.Canvas):
    colors = [
        ("#ff0505", "#05ff05"),
        ("#ff05de", "#deff05"),
        ("#b005ff", "#ffda05"),
        ("#2605ff", "#ff9305"),
        ("#05fff7", "#ff4405"),
        ("#000000", "#ffffff"),
    ]
    previous_color_index = -1
    color_index = randint(0, len(colors) - 1)
    while True:
        canvas.delete("all")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        while color_index == previous_color_index:
            color_index = randint(0, len(colors) - 1)
        base_color_index = randint(0, 1)
        previous_color_index = color_index
        canvas_color = colors[color_index][base_color_index]
        text_color = colors[color_index][abs(base_color_index - 1)]
        canvas.configure(bg=canvas_color)
        canvas.create_text(
            5, 15, anchor=tkinter.W, font=("Purisa", 18), text=now, fill=text_color
        )
        sleep(0.5)


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
