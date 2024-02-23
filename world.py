import math


class GridWorld:
    def __init__(self, size_x: int, size_y: int, cell_size: int = 100):
        self.size_x = size_x
        self.size_y = size_y
        self.cell_size = cell_size

        # Initialize grid
        self.grid = [[0 for _ in range(self.size_x)] for _ in range(self.size_y)]

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

    def get_grid(self):
        return self.grid

    def toggle_value(self, pos_x: int, pos_y: int):
        if self.grid[pos_y][pos_x] == 0:
            self.set_value(pos_x, pos_y, 1)
        else:
            self.set_value(pos_x, pos_y, 0)

    def calc_distance(self, pos_x, pos_y, angle_degrees):
        tan_angle = math.tan(math.radians(angle_degrees))  # Convert angle to radians

        # Get horizontal intersection
        yn = math.ceil(pos_y) - pos_y  # y distance nearest y cell border
        xn = yn / tan_angle  # x distance nearest y cell border
        distance_n = (yn*2 + xn*2)**.5

        horizontal_intersection_x = pos_x + xn
        horizontal_intersection_y = int(pos_y + yn)   # Int bc always on border

        print(math.floor(horizontal_intersection_x), horizontal_intersection_y)
        print(distance_n)
        # Check collision
        if self.get_value(math.floor(horizontal_intersection_x), horizontal_intersection_y):

            print("col")

        return {"horizontal_intersection_x": horizontal_intersection_x,
                "horizontal_intersection_y": horizontal_intersection_y}


if __name__ == '__main__':
    gw = GridWorld(10, 10)
    gw.set_value(2, 4, 1)
    gw.set_value(8, 8, 1)
    gw.set_value(2, 2, 1)
    gw.set_value(3, 2, 1)
    print(gw)
    gw.calc_distance(1.5, 1.5, 45)
