import pygame
from world import GridWorld


def run_game(screen_size_x: int, screen_size_y: int):

    # Initialize Pygame and set up the window
    pygame.init()
    pygame.font.init()
    debug_font = pygame.font.SysFont('Arial', 14)
    pygame.display.set_caption("Ray Casting")
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])

    # Create game loop variables
    done = False
    clock = pygame.time.Clock()
    delta_time_last_frame = 1

    # Create Game instance
    game = Game()

    """ MAIN GAME LOOP """

    while not done:

        done = game.process_events()
        game.display_frame(screen)

        # Display FPS
        text_surface = debug_font.render(f"FPS: {round(1 / delta_time_last_frame)}", False, (255, 255, 255))
        screen.blit(text_surface, (0, 700))

        # Display updated screen
        pygame.display.flip()

        # Tick game and save time this frame took to render
        delta_time_last_frame = clock.tick(60) / 1000


class Game:
    grid_cell_colors = {0: (255, 255, 255), 1: (0, 0, 0)}

    def __init__(self):

        # Initialize Buttons
        self.button_font = pygame.font.SysFont('Arial', 15)
        self.control_buttons = []
        self.grid_toggle_button = Button(10, 10, 100, 30, text="Hide Grid", font=self.button_font,
                                         on_click_function=self._on_toggle_grid)
        self.control_buttons.append(self.grid_toggle_button)

        # Initialize world grid
        self.show_world_grid = True  # Toggles display of grid on screen
        self.grid = GridWorld(10, 10)
        self.grid_cell_objects = self.initialize_grid(grid_size_x=400, grid_start_x=10,
                                                      grid_start_y=50, show_grid_lines=True)

    def process_events(self):
        """
        Process input events by the player
        """
        for event in pygame.event.get():

            # CASE: Game closed
            if event.type == pygame.QUIT:
                return True

            # CASE: Left Mouse button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_position = event.pos

                # Check collision with all grid cells
                if self.show_world_grid:
                    for cell in self.grid_cell_objects:
                        if cell["rect"].collidepoint(click_position):

                            # Change cell value and update cell color in grid_cell_objects list
                            self.grid.toggle_value(cell["row_index"], cell["col_index"])
                            cell["color"] = Game.grid_cell_colors[self.grid.get_value(cell["row_index"],
                                                                                      cell["col_index"])]
                            break

    def display_frame(self, screen):
        """
        Draw all current game objects to a screen
        :param screen: pygame screen to draw the game objects on
        """

        # Reset screen
        screen.fill((0, 0, 0))

        # Draw buttons
        for button in self.control_buttons:
            button.process(screen)

        # Draw cells for grid display
        if self.show_world_grid:
            for cell in self.grid_cell_objects:
                pygame.draw.rect(screen, cell["color"], cell["rect"])

    def initialize_grid(self, grid_size_x, grid_start_x=0, grid_start_y=0, show_grid_lines=False):
        """
        Creates pygame rect objects for every cell in the grid world.
        :param grid_size_x: pixel size of complete grid
        :param grid_start_x: x position on complete screen of grid start
        :param grid_start_y: y position on complete screen of grid start
        :param show_grid_lines: Leaves a one pixel gap between cells to show grid lines
        :return: List of dictionaries. One dictionary per cell. Includes rect object, color and grid indexes.
        """

        # Get inital values
        grid_state = self.grid.get_grid()
        cell_size = round(grid_size_x / len(grid_state[0]))
        grid_cell_objects = []  # Return list with cells information & objects

        # Iterate throug every cell state
        for row_index, row in enumerate(grid_state):
            for col_index, value in enumerate(row):

                # Determine parameters for cell to be drawn
                rect_pos_x = col_index * cell_size + grid_start_x
                rect_pos_y = row_index * cell_size + grid_start_y
                cell_draw_size = cell_size - (1 if show_grid_lines else 0)

                # Add cell rect object and info to return array
                grid_cell_objects.append({"rect": pygame.Rect(rect_pos_x, rect_pos_y, cell_draw_size, cell_draw_size),
                                          "color": Game.grid_cell_colors[value],
                                          "row_index": row_index,
                                          "col_index": col_index})

        # Return cell obj array
        return grid_cell_objects

    def _on_toggle_grid(self):
        """
        Toggle the grid display and update the toggle button text
        """
        if self.show_world_grid:
            self.show_world_grid = False
            self.grid_toggle_button.set_text("Show Grid")
            print("[GAME] Grid hidden.")
        else:
            self.show_world_grid = True
            self.grid_toggle_button.set_text("Hide Grid")
            print("[GAME] Grid shown.")




class Button:
    # Adapted from https://thepythoncode.com/article/make-a-button-using-pygame-in-python

    color = {
        'normal': '#ffffff',
        'hover': '#666666',
        'pressed': '#333333',
    }

    def __init__(self, x, y, width, height, text, font, on_click_function=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.font = font
        self.already_pressed = False

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_surf = font.render(text, True, (20, 20, 20))

    def process(self, screen):

        mouse_position = pygame.mouse.get_pos()
        self.button_surface.fill(Button.color['normal'])

        if self.button_rect.collidepoint(mouse_position):
            self.button_surface.fill(Button.color['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(Button.color['pressed'])

                if not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True

            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_surf, [
            self.button_rect.width/2 - self.button_surf.get_rect().width/2,
            self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])

        screen.blit(self.button_surface, self.button_rect)

    def set_text(self, text):
        self.button_surf = self.font.render(text, True, (20, 20, 20))


if __name__ == '__main__':
    run_game(1280, 720)
