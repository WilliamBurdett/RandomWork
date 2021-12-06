import tkinter
from typing import Dict

from utils.threading import Manager

GRID_SIZE = 100
CELL_SIZE = 10


class Cell:
    def __init__(self, x_location: int, y_location: int):
        self.filled = False
        self.head = False
        self.x_location = x_location
        self.y_location = y_location


def draw_cells(cells: Dict[str, Cell], canvas: tkinter.Canvas) -> None:
    canvas.delete("all")
    for cell in cells.values():
        x_start = cell.x_location * CELL_SIZE
        x_end = x_start - 1
        y_start = cell.y_location * CELL_SIZE
        y_end = y_start - 1
        canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="red")


def clear(canvas: tkinter.Canvas) -> None:
    canvas.delete("all")


def main():
    queue_manager = Manager()
    cells: Dict[str, Cell] = {}
    for x_location in range(GRID_SIZE):
        for y_location in range(GRID_SIZE):
            cells[f"{x_location},{y_location}"] = Cell(x_location, y_location)
    top = tkinter.Tk()

    canvas = tkinter.Canvas(
        top,
        bg="white",
        height=GRID_SIZE * CELL_SIZE + 3,
        width=GRID_SIZE * CELL_SIZE + 3,
    )
    for i in range(2000):
        queue_manager.put((draw_cells, {"canvas": canvas}))
    canvas.grid()
    top.mainloop()


if __name__ == "__main__":
    main()
