class GridWorld:
    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y

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


if __name__ == '__main__':
    gw = GridWorld(10, 10)
    gw.set_value(2, 4, 1)
    gw.set_value(8, 8, 1)
    print(gw)
