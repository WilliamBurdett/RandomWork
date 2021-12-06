import tkinter
from random import randint
from typing import Dict, Tuple

from utils.threading import Manager

SCREEN_SIZE = 800
GRID_SIZE = 34
CELL_SIZE = int(SCREEN_SIZE / GRID_SIZE)
CELL_OFFSET = 1
FILL_COLOR = "red"
EMPTY_COLOR = "white"


class Cell:
    def __init__(self, x_location: int, y_location: int):
        self.filled = False
        self.head = False
        self.apple = False
        self.x_location = x_location
        self.y_location = y_location

    def get_canvas_location(self) -> Tuple[int, int, int, int]:

        x_start = self.x_location * CELL_SIZE + 2
        x_end = x_start + CELL_SIZE
        y_start = self.y_location * CELL_SIZE + 2
        y_end = y_start + CELL_SIZE
        return (x_start, y_start, x_end, y_end)

    @staticmethod
    def get_key(x_location: int, y_location: int) -> str:
        return f"{x_location},{y_location}"


def draw_cells(cells: Dict[str, Cell], canvas: tkinter.Canvas) -> None:
    canvas.delete("all")
    for cell in cells.values():
        if cell.filled is True:
            fill_color = FILL_COLOR
        else:
            fill_color = EMPTY_COLOR
        canvas.create_rectangle(*cell.get_canvas_location(), fill=fill_color)


def clear(canvas: tkinter.Canvas) -> None:
    canvas.delete("all")


def main():
    queue_manager = Manager()
    cells: Dict[str, Cell] = {}
    start_x_location = randint(0, GRID_SIZE)
    start_y_location = randint(0, GRID_SIZE)
    for x_location in range(GRID_SIZE):
        for y_location in range(GRID_SIZE):
            cells[f"{x_location},{y_location}"] = Cell(x_location, y_location)
    cells[Cell.get_key(start_x_location, start_y_location)].head = True
    cells[Cell.get_key(start_x_location, start_y_location)].filled = True

    top = tkinter.Tk()

    canvas = tkinter.Canvas(
        top,
        bg="white",
        height=GRID_SIZE * CELL_SIZE + 3,
        width=GRID_SIZE * CELL_SIZE + 3,
    )
    draw_cells(cells, canvas)
    # for i in range(2000):
    #     queue_manager.put((draw_cells, {"canvas": canvas}))

    canvas.grid()
    top.mainloop()


if __name__ == "__main__":
    main()
