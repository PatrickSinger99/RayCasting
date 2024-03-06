import math
import matplotlib.pyplot as plt
from matplotlib import patches, lines
from typing import Union, Type


class Ray:
    def __init__(self, start_x: int, start_y: int, angle_degrees: Union[int, float],
                 length: Union[int, float, None] = None):
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle_degrees
        self.length = length

    def calculate_direction(self, distance=1):
        angle_radians = math.radians(self.angle)
        new_x = self.start_x + distance * math.cos(angle_radians)
        new_y = self.start_y + distance * math.sin(angle_radians)
        return new_x, new_y

    def calculate_grid_collision(self, grid_class_object):  # TODO: Why is "grid: Type[GridWorld]" not working ??
        cosine_angle = math.cos(math.radians(self.angle))
        print(cosine_angle)
        horizontal_grid_collisions = []
        vertical_grid_collisions = []

        """Get coordinates of first collision with horizontal grid border"""

        # Calculate the next horizontal border
        cell_size = grid_class_object.cell_size
        next_horizontal_border = math.ceil(self.start_y / cell_size) * cell_size

        # Use next horizontal border to calculate distance to it (opposite) and derive adjacent after
        opposite = next_horizontal_border - self.start_y  # Gegenkathete
        adjacent = opposite / cosine_angle  # Ankathete

        # With adjacent, calculate the x coordinate of the grid collision (y coordinate is simply the horizontal border)
        first_horizontal_grid_collision = (self.start_x + adjacent, next_horizontal_border)
        horizontal_grid_collisions.append(first_horizontal_grid_collision)

        """Get subsequent horizontal grid collisions (From now on always full cell steps)"""
        current_x, current_y = first_horizontal_grid_collision
        full_cell_horizontal_collsion_x_length = cell_size / cosine_angle  # opposite calculation

        # Step through horizontal grid lines until a collision with a cell or the end of the world
        last_y_row = grid_class_object.cell_amount_y * cell_size
        while current_y < last_y_row:
            current_x, current_y = current_x + full_cell_horizontal_collsion_x_length, current_y + cell_size
            horizontal_grid_collisions.append((current_x, current_y))

        return horizontal_grid_collisions


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
                # TEST
                end_x, end_y = ray.calculate_direction(distance=100000)
                ax.add_line(lines.Line2D([ray.start_x, end_x], [ray.start_y, end_y]))

                coll_coord_list = ray.calculate_grid_collision(grid_class_object=self)
                print(coll_coord_list)
                for x, y in coll_coord_list:
                    ax.plot(x, y, marker='x', color="red")

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

    gw.add_ray(2800, 4200, 45)

    print(gw)
    gw.plot()
    plt.show()
