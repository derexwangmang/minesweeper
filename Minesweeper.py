import pygame
import numpy as np
import random

pygame.init()

# Window Information
DISPLAY_WIDTH = 603     # Includes margins (creates black outline outside of grid)
DISPLAY_HEIGHT = 603    # Includes margins (creates black outline outside of grid)
BOTTOM_TEXT_SPACING = 75
DIMENSIONS = [DISPLAY_WIDTH, DISPLAY_HEIGHT + BOTTOM_TEXT_SPACING]
screen = pygame.display.set_mode(DIMENSIONS)

# Initializes title
pygame.display.set_caption("Minesweeper")

# Initializes font
pygame.font.init()

# Clock
clock = pygame.time.Clock()

# Load images
flag_image = pygame.image.load('images/flag.png')
mine_image = pygame.image.load('images/mine.jpg')

# Color Constants
BLACK = pygame.Color('#000000')
GREEN = pygame.Color('#00FF00')
BLUE = pygame.Color('#0000FF')
WHITE = pygame.Color('#FFFFFF')

# Grid States
CLEAR = 0
UNTOUCHED = 9
FLAG = 10
MINE = -1

# Difficulty Levels
EASY = "EASY"
MEDIUM = "MEDIUM"
HARD = "HARD"

# Font Sizes
FONT_SMALL = 26
FONT_MEDIUM = 35
FONT_LARGE = 52


class Minesweeper:
    def __init__(self):
        # Develops starting screen, which allows the user to decide difficulty
        self.__start_screen()

        if self.difficulty == EASY:
            self.scale = 1
            self.my_font = pygame.font.SysFont('Arial', FONT_LARGE)
        elif self.difficulty == MEDIUM:
            self.scale = 2 / 3
            self.my_font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        else:
            self.scale = 0.5
            self.my_font = pygame.font.SysFont('Arial', FONT_SMALL)

        # Sets width, height, margins, grids, number of mines and flags based on difficulty level
        self.width = int(60 * self.scale)
        self.height = int(60 * self.scale)
        self.margins = 3
        self.user_grid = np.full((int((DIMENSIONS[1] - BOTTOM_TEXT_SPACING) / self.height),
                                  int(DIMENSIONS[0] / self.width)),
                                 UNTOUCHED)
        self.hidden_grid = np.array(self.user_grid)
        self.cleared_grid = np.array(self.user_grid)
        self.num_mines = len(self.user_grid) * len(self.user_grid[0]) * 1 / 6
        self.flag_count = len(self.user_grid) * len(self.user_grid[0]) * 1 / 6

        # Sets flag and mine image size
        self.flag_image = pygame.transform.scale(flag_image, (self.width - self.margins,
                                                              self.height - self.margins))
        self.mine_image = pygame.transform.scale(mine_image, (self.width - self.margins,
                                                              self.height - self.margins))

        self.draw()

    # Start screen
    def __start_screen(self):
        text_surface_easy = pygame.font.SysFont('Arial', FONT_LARGE).render(EASY, False, BLACK)
        start_coords_easy = self.find_start_coords(text_surface_easy, 1 / 4)
        button_easy = self.button_surface(text_surface_easy, start_coords_easy)

        text_surface_medium = pygame.font.SysFont('Arial', FONT_LARGE).render(MEDIUM, False, BLACK)
        start_coords_medium = self.find_start_coords(text_surface_medium, 2 / 4)
        button_medium = self.button_surface(text_surface_medium, start_coords_medium)

        text_surface_hard = pygame.font.SysFont('Arial', FONT_LARGE).render(HARD, False, BLACK)
        start_coords_hard = self.find_start_coords(text_surface_hard, 3 / 4)
        button_hard = self.button_surface(text_surface_hard, start_coords_hard)

        self.difficulty = None

        while self.difficulty is None:
            pygame.draw.rect(screen, GREEN, button_easy)
            screen.blit(text_surface_easy,
                        (start_coords_easy[0], start_coords_easy[1]))

            pygame.draw.rect(screen, GREEN, button_medium)
            screen.blit(text_surface_medium,
                        (start_coords_medium[0], start_coords_medium[1]))

            pygame.draw.rect(screen, GREEN, button_hard)
            screen.blit(text_surface_hard,
                        (start_coords_hard[0], start_coords_hard[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_easy.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        self.difficulty = EASY
                    elif button_medium.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        self.difficulty = MEDIUM
                    elif button_hard.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        self.difficulty = HARD

            pygame.display.flip()

    def draw(self):
        # Victory / Loss condition
        mine_triggered = False
        matching_boards = False

        # Initialization of hidden board condition
        first_click = True

        # Bottom Text Font
        bottom_text_font = pygame.font.SysFont('Arial', FONT_LARGE)

        while not mine_triggered and not matching_boards:
            screen.fill(BLACK)

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Converts screen coordinates to grid coordinates
                    column = int(pos[0] / self.width)
                    row = int(pos[1] / self.height)

                    if 0 <= row < len(self.user_grid) and 0 <= column < (len(self.user_grid[0])):
                        # User left clicks UNTOUCHED position
                        if event.button == 1 and self.user_grid[row][column] == UNTOUCHED:
                            # Creates a hidden board, which the user board is compared to
                            if first_click:
                                self.__create_hidden_board(row, column)
                                self.user_grid[row][column] = self.hidden_grid[row][column]
                                first_click = False
                            else:
                                self.user_grid[row][column] = self.hidden_grid[row][column]
                                if self.user_grid[row][column] == MINE:
                                    mine_triggered = True
                                    break
                                if self.hidden_grid[row][column] == CLEAR:
                                    self.__clear_surrounding_squares(row, column)
                        # User right clicks
                        # Plants a flag if there is not one present, or removes if there is one
                        elif event.button == 3:
                            if self.user_grid[row][column] == UNTOUCHED and self.flag_count > 0:
                                self.user_grid[row][column] = FLAG
                                self.flag_count -= 1
                            elif self.user_grid[row][column] == FLAG:
                                self.user_grid[row][column] = UNTOUCHED
                                self.flag_count += 1

            for r, c in np.ndindex(self.user_grid.shape):
                if self.user_grid[r][c] != MINE:
                    if self.user_grid[r][c] == UNTOUCHED:
                        color = GREEN
                    else:
                        color = BLUE

                    if self.user_grid[r][c] != FLAG:
                        pygame.draw.rect(screen,
                                         color,
                                         pygame.Rect(self.width * c + self.margins,
                                                     self.height * r + self.margins,
                                                     self.width - self.margins,
                                                     self.height - self.margins))
                    else:
                        screen.blit(self.flag_image, (self.width * c + self.margins,
                                                      self.height * r + self.margins))

                    if self.user_grid[r][c] != CLEAR and self.user_grid[r][c] != UNTOUCHED and \
                            self.user_grid[r][c] != FLAG:
                        text_surface_num = self.my_font.render(str(self.user_grid[r][c]), False, WHITE)
                        screen.blit(text_surface_num,
                                    (int(
                                        self.width * c + self.width / 2 - text_surface_num.get_width() / 2
                                        + self.margins),
                                     int(
                                         self.height * r + self.height / 2 - text_surface_num.get_height() / 2
                                         + self.margins)))

            text_surface_flags = bottom_text_font.render("Flags: {0}".format(int(self.flag_count)), False, GREEN)
            pygame.draw.rect(screen,
                             BLACK,
                             [int(DIMENSIONS[0] / 2 - text_surface_flags.get_width() / 2),
                              int((DIMENSIONS[1] + (
                                      DIMENSIONS[1] - BOTTOM_TEXT_SPACING)) / 2 - text_surface_flags.get_height() / 2),
                              text_surface_flags.get_width(),
                              text_surface_flags.get_height()])
            screen.blit(text_surface_flags,
                        (int(DIMENSIONS[0] / 2 - text_surface_flags.get_width() / 2),
                         int((DIMENSIONS[1] + (
                                 DIMENSIONS[1] - BOTTOM_TEXT_SPACING)) / 2 - text_surface_flags.get_height() / 2)))

            if not first_click:
                temp = True

                for r, c in np.ndindex(self.user_grid.shape):
                    if self.hidden_grid[r][c] != MINE:
                        temp = (self.user_grid[r][c] == self.hidden_grid[r][c])
                        if not temp:
                            break

                if temp:
                    matching_boards = True

            # Displays 60 frames a second
            clock.tick(60)
            pygame.display.flip()

        if mine_triggered:
            self.__display_defeat()
        else:
            self.__display_victory()

    # Develops the computer board, which is compared to the user board
    def __create_hidden_board(self, row_index, column_index):
        for i in range(int(self.num_mines)):
            mine_created = False
            while not mine_created:
                x = random.randint(0, len(self.hidden_grid) - 1)
                y = random.randint(0, len(self.hidden_grid[0]) - 1)
                if self.hidden_grid[x][y] == UNTOUCHED:
                    self.hidden_grid[x][y] = MINE
                    mine_created = True
                if row_index - 1 <= x <= row_index + 1 and column_index - 1 <= y <= column_index + 1:
                    self.hidden_grid[x][y] = CLEAR
                    mine_created = False
        for ix, iy in np.ndindex(self.hidden_grid.shape):
            if self.hidden_grid[ix][iy] != MINE:
                self.hidden_grid[ix][iy] = self.__count_adjacent_mines(ix, iy)
        self.__clear_surrounding_squares(row_index, column_index)

    # Counts the number of adjacent mines
    def __count_adjacent_mines(self, given_row, given_column):
        adjacent_mines = 0
        for ii in range(given_row - 1, given_row + 2):
            for jj in range(given_column - 1, given_column + 2):
                if 0 <= ii < len(self.hidden_grid) and 0 <= jj < len(self.hidden_grid[0]):
                    if self.hidden_grid[ii][jj] == MINE:
                        if ii == given_row and jj == given_column:
                            adjacent_mines += 0
                        else:
                            adjacent_mines += 1
        return adjacent_mines

    # Recursively clears the surrounding squares that have no mines
    def __clear_surrounding_squares(self, r_index, c_index):
        if self.user_grid[r_index][c_index] == FLAG:
            self.flag_count += 1
        self.user_grid[r_index][c_index] = self.hidden_grid[r_index][c_index]
        if self.hidden_grid[r_index][c_index] == CLEAR:
            for i in range(r_index - 1, r_index + 2):
                for j in range(c_index - 1, c_index + 2):
                    if 0 <= i < len(self.hidden_grid) and 0 <= j < len(self.hidden_grid[0]) and \
                            self.cleared_grid[i][j] == UNTOUCHED:
                        self.cleared_grid[i][j] = CLEAR
                        self.__clear_surrounding_squares(i, j)

    # Victory Screen
    def __display_victory(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            for r, c in np.ndindex(self.hidden_grid.shape):
                if self.hidden_grid[r][c] == MINE:
                    screen.blit(self.mine_image, (self.width * c + self.margins,
                                                  self.height * r + self.margins))

            text_surface_victory = self.my_font.render("CONGRATULATIONS!", False, WHITE)
            pygame.draw.rect(screen,
                             BLACK,
                             [int(DIMENSIONS[0] / 2 - text_surface_victory.get_width() / 2),
                              int((DIMENSIONS[1] - BOTTOM_TEXT_SPACING) / 2 - text_surface_victory.get_height() / 2),
                              text_surface_victory.get_width(),
                              text_surface_victory.get_height()])
            screen.blit(text_surface_victory, (int(DIMENSIONS[0] / 2 - text_surface_victory.get_width() / 2),
                                               int((DIMENSIONS[1] - BOTTOM_TEXT_SPACING) / 2
                                                   - text_surface_victory.get_height() / 2)))
            clock.tick(60)
            pygame.display.flip()

    # Defeat Screen
    def __display_defeat(self):
        # Defeat Screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            for r, c in np.ndindex(self.hidden_grid.shape):
                if self.hidden_grid[r][c] == MINE:
                    screen.blit(self.mine_image, (self.width * c + self.margins,
                                                  self.height * r + self.margins))
                else:
                    if self.hidden_grid[r][c] != CLEAR and self.hidden_grid[r][c] != UNTOUCHED and \
                            self.hidden_grid[r][c] != FLAG:
                        text_surface_num = self.my_font.render(str(self.hidden_grid[r][c]), False, WHITE)
                        screen.blit(text_surface_num,
                                    (int(self.width * c + self.width / 2 - text_surface_num.get_width() / 2
                                         + self.margins),
                                     int(self.height * r + self.height / 2 - text_surface_num.get_height() / 2
                                         + self.margins)))

            text_surface_defeat = self.my_font.render("GAME OVER", False, WHITE)
            pygame.draw.rect(screen,
                             BLACK,
                             [int(DIMENSIONS[0] / 2 - text_surface_defeat.get_width() / 2),
                              int((DIMENSIONS[1] - BOTTOM_TEXT_SPACING) / 2 - text_surface_defeat.get_height() / 2),
                              text_surface_defeat.get_width(),
                              text_surface_defeat.get_height()])
            screen.blit(text_surface_defeat, (int(DIMENSIONS[0] / 2 - text_surface_defeat.get_width() / 2),
                                              int((DIMENSIONS[1] - BOTTOM_TEXT_SPACING) / 2
                                                  - text_surface_defeat.get_height() / 2)))

            clock.tick(60)
            pygame.display.flip()

    @staticmethod
    def find_start_coords(txt_surf, height_scaling):
        return [int(DIMENSIONS[0] / 2 - txt_surf.get_width() / 2),
                int(DIMENSIONS[1] * height_scaling - txt_surf.get_height() / 2)]

    @staticmethod
    def button_surface(txt_surf, start_coords):
        button_spacing = 75
        return pygame.Rect(button_spacing,
                           int(start_coords[1]),
                           int(DIMENSIONS[0] - 2 * button_spacing),
                           int(txt_surf.get_height()))


if __name__ == "__main__":
    Minesweeper()
