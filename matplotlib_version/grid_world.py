import math
import matplotlib.pyplot as plt
from matplotlib import patches
from typing import Union


class Ray:
    def __init__(self, start_x: int, start_y: int, angle_degrees: Union[int, float],
                 length: Union[int, float, None] = None):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle_degrees
        self.length = length


class GridWorld:

    cell_borders_color = "grey"
    cell_value_colors = {1: "black"}

    def __init__(self, cell_amount_x: int, cell_amount_y: int, cell_size: int = 1000):
        self.cell_amount_x = cell_amount_x
        self.cell_amount_y = cell_amount_y
        self.cell_size = cell_size

        # Initialize grid
        self.grid = [[0 for _ in range(self.cell_amount_x)] for _ in range(self.cell_amount_y)]
        self.rays = []

    def __str__(self):
        return_str = ""
        for row in self.grid:
            row_str = "  ".join([str(val) for val in row])
            return_str += row_str + "\n"
        return return_str

    def get_value(self, pos_x: int, pos_y: int):
        return self.grid[pos_y][pos_x]

    def set_value(self, pos_x: int, pos_y: int, value: int):
        self.grid[pos_y][pos_x] = value
        print(f"[GRID] Cell x={pos_x}, y={pos_y} set to {value}.")

    def set_value_line(self, start_x, start_y, length, orientation, value):
        for i in range(length):
            if orientation == "h":
                self.set_value(start_x + i, start_y, value)
            elif orientation == "v":
                self.set_value(start_x, start_y + i, value)

    def set_value_border(self, value):
        self.set_value_line(0, 0, self.cell_amount_x, "h", value)
        self.set_value_line(0, self.cell_amount_y - 1, self.cell_amount_x, "h", value)
        self.set_value_line(self.cell_amount_x - 1, 0, self.cell_amount_y, "v", value)
        self.set_value_line(0, 0, self.cell_amount_y, "v", value)

    def set_value_block(self, start_x, start_y, length_x, length_y, value):
        for i in range(length_y):
            self.set_value_line(start_x, start_y + i, length_x, "h", value)

    def add_ray(self, start_x, start_y, angle_degrees, length=None):
        new_ray = Ray(start_x, start_y, angle_degrees, length)
        self.rays.append(new_ray)

    def plot(self, size: int = 5, show_cell_borders: bool = True, show_cell_states: bool = True, show_rays: bool = True):

        fig, ax = plt.subplots(figsize=(int(size * (self.cell_amount_x / self.cell_amount_y)), size))

        if show_cell_states:
            for y_index, x_row in enumerate(self.grid):
                for x_index, cell_value in enumerate(x_row):
                    if cell_value != 0:
                        ax.add_patch(patches.Rectangle((x_index * self.cell_size - 1, y_index * self.cell_size - 1),
                                                       self.cell_size, self.cell_size,
                                                       color=GridWorld.cell_value_colors[cell_value]))

        if show_cell_borders:
            for i in range(self.cell_amount_y + 1):
                plt.axhline(i * self.cell_size, color=GridWorld.cell_borders_color, linestyle="dashed", linewidth="1")

            for i in range(self.cell_amount_x + 1):
                plt.axvline(i * self.cell_size, color=GridWorld.cell_borders_color, linestyle="dashed", linewidth="1")

        if show_rays:
            for ray in self.rays:
                pass  # TODO
        
        plt.xlim(0, self.cell_amount_x * self.cell_size)
        plt.ylim(0, self.cell_amount_y * self.cell_size)

        ax.xaxis.tick_top()
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal')

        return fig


if __name__ == '__main__':
    gw = GridWorld(15, 10)

    gw.set_value_border(1)
    gw.set_value_block(1, 1, 5, 3, 1)
    gw.set_value_block(10, 4, 2, 5, 1)
    gw.set_value_block(4, 7, 4, 2, 1)
    gw.set_value(7, 6, 1)

    gw.add_ray(1800, 3200, 45)

    print(gw)
    gw.plot()
    plt.show()
