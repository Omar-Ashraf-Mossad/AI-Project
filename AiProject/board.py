from PIL import ImageGrab
import pyautogui

# YOU MAY NEED TO CHANGE THESE VALUES BASED ON YOUR SCREEN SIZE
LEFT = 600
TOP = 255
RIGHT = 1323
BOTTOM = 875

EMPTY = 0
RED = 1
BLUE = 2


class Board:
    def __init__(self) -> None:
        self.board = [[EMPTY for i in range(7)] for j in range(6)]

    def print_grid(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY:
                    print("*", end=" \t")
                elif grid[i][j] == RED:
                    print("R", end=" \t")
                elif grid[i][j] == BLUE:
                    print("B", end=" \t")
            print("\n")

    def _convert_grid_to_color(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j][0] > 100 and grid[i][j][0] < 230:
                    grid[i][j] = RED
                elif grid[i][j][0] > 0 and grid[i][j][0] < 100:
                    grid[i][j] = BLUE
                else:
                    grid[i][j] = EMPTY
        return grid

    def _get_grid_cordinates(self):
        startCord = (51.65, 51.643)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 103
                y = startCord[1] + j * 103
                cordArr.append((x, y))
        return cordArr

    def _transpose_grid(self, grid):
        return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    def _capture_image(self):
        image = ImageGrab.grab()
        cropedImage = image.crop((LEFT, TOP, RIGHT, BOTTOM))
        # cropedImage.show()
        return cropedImage

    def _convert_image_to_grid(self, image):
        pixels = [[] for i in range(7)]
        i = 0
        for index, cord in enumerate(self._get_grid_cordinates()):
            pixel = image.getpixel(cord)
            if index % 6 == 0 and index != 0:
                i += 1
            pixels[i].append(pixel)
        return pixels

    def _get_grid(self):
        cropedImage = self._capture_image()
        pixels = self._convert_image_to_grid(cropedImage)
        #cropedImage.show()
        grid = self._transpose_grid(pixels)
        return grid

    def _check_if_game_end(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY and self.board[i][j] != EMPTY:
                    return True
        return False

    def get_game_grid(self):
        game_grid = self._get_grid()
        new_grid = self._convert_grid_to_color(game_grid)
        is_game_end = self._check_if_game_end(new_grid)
        self.board = new_grid
        return (self.board, is_game_end)

    def select_column(self, column):
        cord = self._get_grid_cordinates()[0]
        pyautogui.click(
            cord[1] * column * 2 + LEFT + cord[1],
            cord[0] + TOP,
        )
    
    def is_full(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY:
                    return False
        return True

    def get_token(self, grid, row, column):
        return grid[row][column]

    def get_heuristic(self, grid, player):
        score = 0
        for row in range(6):
            for col in range(7):
                if self.get_token(grid, row, col) == player:
                    score += self.get_score(grid, player, row, col)
                elif self.get_token(grid, row, col) != EMPTY:
                    score -= self.get_score(grid, RED if player == BLUE else BLUE, row, col)
        return score

    def get_score(self, grid, player, row, col):
        score = 0
        for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]: 
            score += self.get_direction_score(grid, player, row, col, direction)
        return score

    def get_direction_score(self, grid, player, row, col, direction):
        dr, dc = direction
        score = 0
        oponent = BLUE if player == RED else RED
        for i in range(1, 4):
            r = row + i * dr
            c = col + i * dc
            if r < 0 or c < 0 or r >= 6 or c >= 7 or self.get_token(grid, r, c)==oponent:
                return 0
                
            if self.get_token(grid,r,c)==player:
                score += 1
            if self.get_token(grid,r,c)==EMPTY:
                next_row = self.get_next_row(grid,c)
                score += 1 / (abs(r-next_row)+2)

            if score==3:
                score = score * 100
        return score
    
    def is_valid_column(self, grid, column):
        if grid[0][column] == EMPTY:
            return True
        return False

    def insert_token(self, grid, column, row, player):
        grid[row][column] = player

    def remove_token(self, grid, column, row):
        grid[row][column] = EMPTY

    def get_next_row(self, grid, column):
        for i in range(len(grid)-1, -1, -1):
            if grid[i][column]==EMPTY:
                return i
    
    def is_winning_state(self, grid, player):
        result = False
        for row in range(6):
            for col in range(7):
                if self.get_token(grid, row, col) == player:
                    result = self.check_connect_4(grid, player, row, col)
                elif self.get_token(grid, row, col) != EMPTY:
                    result = self.check_connect_4(grid, RED if player == BLUE else BLUE, row, col)
                
                if result == True:
                    return True
        return False

    def check_connect_4(self, grid, player, row, col):
        for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]: 
            if self.check_direction(grid, player, row, col, direction)==True:
                return True
        return False

    def check_direction(self, grid, player, row, col, direction):
        dr, dc = direction
        oponent = BLUE if player == RED else RED
        for i in range(1, 4):
            r = row + i * dr
            c = col + i * dc
            if r < 0 or c < 0 or r >= 6 or c >= 7 or self.get_token(grid, r, c)!=player:
                return False

        return True

    def minimax(self, grid, depth, player):
        if depth == 0 or self.is_winning_state(grid,player) or self.is_full(grid):
            return None, self.get_heuristic(grid,player)

        best_column = None
        best_value = -1000 if player == RED else 1000
        for column in range(0,7):
            if self.is_valid_column(grid,column):
                row = self.get_next_row(grid,column)
                self.insert_token(grid, column, row, player)
                _, value = self.minimax(grid, depth - 1, BLUE if player == RED else RED)
                self.remove_token(grid, column, row)
                if player == RED and value > best_value:
                    best_column = column
                    best_value = value
                elif player == BLUE and value < best_value:
                    best_column = column
                    best_value = value

        return best_column, best_value