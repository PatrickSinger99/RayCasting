import math
import matplotlib.pyplot as plt
from matplotlib import patches, lines
from typing import Union, Type


class Ray:
    def __init__(self, start_x: int, start_y: int, angle_degrees: Union[int, float]):
        # Start Parameters
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle_degrees % 360  # Limit to 360 degrees

        # Calculated Parameters
        self.horizontal_grid_collisions = []
        self.vertical_grid_collisions = []
        self.collision_coord_x = None  # Collision coordiante
        self.collision_coord_y = None  # Collision coordiante
        self.collided_cell_x = None  # Cell position in grid
        self.collided_cell_y = None  # Cell position in grid

    # TODO TEMP
    def calculate_direction(self, distance=1):
        angle_radians = math.radians(self.angle)
        new_x = self.start_x + distance * math.cos(angle_radians)
        new_y = self.start_y + distance * math.sin(angle_radians)
        return new_x, new_y

    def calculate_grid_collision(self, grid_class_object):

        # Reset calculated parameters
        self.horizontal_grid_collisions = []
        self.vertical_grid_collisions = []
        self.collision_coord_x = None  # Collision coordiante
        self.collision_coord_y = None  # Collision coordiante
        self.collided_cell_x = None  # Cell position in grid
        self.collided_cell_y = None  # Cell position in grid

        # Precalculate sine and cosine
        cosine_angle = math.cos(math.radians(self.angle))
        sine_angle = math.sin(math.radians(self.angle))

        # Determine line type (pointing upwards or downwards)
        if self.angle > 180:
            upwards_direction = True
        else:
            upwards_direction = False

        # Calculate the next horizontal border
        cell_size = grid_class_object.cell_size

        """Get coordinates of first collision with horizontal grid border"""

        if upwards_direction:
            next_horizontal_border = math.floor(self.start_y / cell_size) * cell_size
        else:
            next_horizontal_border = math.ceil(self.start_y / cell_size) * cell_size

        # Use next horizontal border to calculate distance to it (opposite) and derive adjacent after
        opposite = next_horizontal_border - self.start_y  # Gegenkathete
        adjacent = opposite / sine_angle  # Ankathete

        # With adjacent, calculate the x coordinate of the grid collision (y coordinate is simply the horizontal border)
        if upwards_direction:
            first_horizontal_grid_collision = (self.start_x - adjacent * cosine_angle, next_horizontal_border)
        else:
            first_horizontal_grid_collision = (self.start_x + adjacent * cosine_angle, next_horizontal_border)

        """Get subsequent horizontal grid collisions (From now on always full cell steps)"""

        current_x, current_y = first_horizontal_grid_collision
        full_cell_horizontal_collision_x_length = cell_size / sine_angle  # opposite calculation

        # Calculate world boundaries
        y_boundary = grid_class_object.cell_amount_y * cell_size
        x_boundary = grid_class_object.cell_amount_x * cell_size

        # Step through horizontal grid lines until a collision with a cell or the end of the world
        while 0 < current_y < y_boundary and 0 < current_x < x_boundary:

            # Check collision with cell
            cell_y_coord = int(current_y / cell_size) - (1 if upwards_direction else 0)
            cell_x_coord = math.floor(current_x / cell_size)

            if grid_class_object.get_value(cell_x_coord, cell_y_coord) != 0:

                # Save values for collision with cell
                self.collision_coord_x = current_x
                self.collision_coord_y = current_y
                self.collided_cell_x = cell_x_coord
                self.collided_cell_y = cell_y_coord
                break

            else:
                self.horizontal_grid_collisions.append((current_x, current_y))

            # Increment coordinates for collision check
            if upwards_direction:
                current_y -= cell_size
            else:
                current_y += cell_size
            current_x += full_cell_horizontal_collision_x_length * cosine_angle

    def BROKEN_calculate_grid_collision(self, grid_class_object):

        # Reset calculated parameters
        self.vertical_grid_collisions = []
        self.collision_coord_x = None  # Collision coordiante
        self.collision_coord_y = None  # Collision coordiante
        self.collided_cell_x = None  # Cell position in grid
        self.collided_cell_y = None  # Cell position in grid

        # Precalculate sine and cosine
        cosine_angle = math.cos(math.radians(self.angle))
        sine_angle = math.sin(math.radians(self.angle))

        # Determine line type (pointing upwards or downwards)
        if 90 < self.angle < 270:
            right_direction = True
        else:
            right_direction = False

        # Calculate the next horizontal border
        cell_size = grid_class_object.cell_size

        """Get coordinates of first collision with horizontal grid border"""

        if right_direction:
            next_vertical_border = math.floor(self.start_x / cell_size) * cell_size
        else:
            next_vertical_border = math.ceil(self.start_x / cell_size) * cell_size

        # Use next horizontal border to calculate distance to it (opposite) and derive adjacent after
        opposite = next_vertical_border - self.start_x  # Gegenkathete
        adjacent = opposite / sine_angle  # Ankathete

        # With adjacent, calculate the x coordinate of the grid collision (y coordinate is simply the horizontal border)
        if right_direction:
            first_vertical_grid_collision = (self.start_y - adjacent * cosine_angle, next_vertical_border)
        else:
            first_vertical_grid_collision = (self.start_y + adjacent * cosine_angle, next_vertical_border)

        """Get subsequent horizontal grid collisions (From now on always full cell steps)"""

        current_x, current_y = first_vertical_grid_collision
        full_cell_vertical_collision_x_length = cell_size / sine_angle  # opposite calculation

        # Calculate world boundaries
        y_boundary = grid_class_object.cell_amount_y * cell_size
        x_boundary = grid_class_object.cell_amount_x * cell_size

        # Step through horizontal grid lines until a collision with a cell or the end of the world
        while 0 < current_y < y_boundary and 0 < current_x < x_boundary:

            # Check collision with cell
            cell_y_coord = math.floor(current_y / cell_size)
            cell_x_coord = int(current_x / cell_size) - (1 if right_direction else 0)

            if grid_class_object.get_value(cell_x_coord, cell_y_coord) != 0:

                # Save values for collision with cell
                self.collision_coord_x = current_x
                self.collision_coord_y = current_y
                self.collided_cell_x = cell_x_coord
                self.collided_cell_y = cell_y_coord
                break

            else:
                self.vertical_grid_collisions.append((current_x, current_y))

            # Increment coordinates for collision check
            if right_direction:
                current_x -= cell_size
            else:
                current_x += cell_size
            current_y += full_cell_vertical_collision_x_length * cosine_angle


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

    def add_ray(self, start_x, start_y, angle_degrees):
        new_ray = Ray(start_x, start_y, angle_degrees)
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
                ray.calculate_grid_collision(grid_class_object=self)

                for x, y in ray.horizontal_grid_collisions:
                    ax.plot(x, y, marker='.', color="red")

                for x, y in ray.vertical_grid_collisions:
                    ax.plot(x, y, marker='.', color="red")

                if ray.collision_coord_x is not None:
                    ax.plot(ray.collision_coord_x, ray.collision_coord_y, marker='x', color="lime")
                    end_x, end_y = ray.collision_coord_x, ray.collision_coord_y
                    ax.add_line(lines.Line2D([ray.start_x, end_x], [ray.start_y, end_y]))


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



    for i in range(90):
        gw.add_ray(2800, 6200, 15 + 4 * i)

    """
    gw.add_ray(2800, 5200, 30)
    gw.add_ray(2800, 5200, 50)
    gw.add_ray(2800, 5200, 100)
    gw.add_ray(2800, 5200, 115)
    gw.add_ray(2800, 5200, 320)
    gw.add_ray(2800, 5200, 300)
    gw.add_ray(2800, 5200, 250)
    gw.add_ray(2800, 5200, 220)
    """


    print(gw)
    gw.plot()
    plt.show()
