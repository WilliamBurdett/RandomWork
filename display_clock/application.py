import tkinter
from datetime import datetime
from random import randint
from time import sleep
from typing import Tuple

from utils.threading import Manager


def int_to_hex(number: int) -> str:
    output = format(number, "x")
    if len(output) == 1:
        return f"0{output}"
    return output


def join_colors_to_hex(
    red: int,
    blue: int,
    green: int,
) -> str:
    return f"#{''.join([int_to_hex(red),int_to_hex(blue),int_to_hex(green)])}"


def generate_colors() -> Tuple[str, str]:
    bright_red = randint(155, 255)
    bright_blue = randint(155, 255)
    bright_green = randint(155, 255)
    dark_red = 255 - bright_red
    dark_blue = 255 - bright_blue
    dark_green = 255 - bright_green
    colors = (
        join_colors_to_hex(bright_red, bright_blue, bright_green),
        join_colors_to_hex(dark_red, dark_blue, dark_green),
    )
    return colors


def draw_time(canvas: tkinter.Canvas):
    base_color_switch = False
    while True:
        canvas.delete("all")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = generate_colors()
        base_color_switch = not base_color_switch

        canvas_color = colors[int(base_color_switch)]
        text_color = colors[int(not base_color_switch)]
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
