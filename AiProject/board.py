from PIL import ImageGrab
import pyautogui


""" Omar's Coordination
LEFT = 433
TOP = 190
RIGHT = 934
BOTTOM = 615

startCord = (35.42,35.786)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 70.83
                y = startCord[1] + j * 71.57
                cordArr.append((x, y))
"""

# YOU MAY NEED TO CHANGE THESE VALUES BASED ON YOUR SCREEN SIZE
LEFT = 433
TOP = 190
RIGHT = 934
BOTTOM = 615


EMPTY = 0
RED = 1
BLUE = 2

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
        startCord = (35.42, 35.786)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 70.83
                y = startCord[1] + j * 71.57
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
        print("SElected Column", column, "------------------------------")

    
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
        # print(player,"Turn")

        for col in range(7):
            if not self.is_valid_column(grid, col):
                continue
            for row in range(6):
                if self.get_token(grid,row,col) != EMPTY:
                    break

                score += self.get_score(grid, RED, row, col,player)
                score -= self.get_score(grid, BLUE, row, col,player)

        flag, color = self.is_winning_state(grid, player)

        if flag and color == RED:
            return score+9999
        elif flag and color != RED:
            return score-9999

        return score

    def get_score(self, grid, player, row, col,turn):
        score = -100000
        max = score

        for direction in [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]:
            score1 = self.get_direction_score(grid, player, row, col, direction, turn)

            if row + 1 <= 5 and self.get_token(grid, row + 1, col) == EMPTY and score1 != 0:
                score1 -= 2
            score += score1

        return score

    def get_direction_score(self, grid, player, row, col, direction,turn):
        dr, dc = direction

        score = 0
        if player == RED:
            enemy = BLUE
        else:
            enemy = RED

        count = 0
        # Count The number of Connected Tokens
        for i in range(1, 4):
            r = row + i * dr
            c = col + i * dc

           # print("HERE", r, c)
            if r < 0 or c < 0 or r >= 6 or c >= 7 or self.get_token(grid, r, c) == enemy or self.get_token(grid, r,c) == EMPTY:
                break
            count = i

# Give scores to chains
        if (count == 3):
            if player == turn:
                score = 100
            else:
                score = 80
        elif count == 2:
            score = 20

        elif count == 1:
            score = 2

#########################
        # token in opposite direction
        r = row - dr
        c = col - dc

# Case There is an empty space and in that direction there is only 1 or 2 tokens and in the opposite no place to put a token or it is an enemy token means that there can't be a 4 token chain here
        if r < 0 or c < 0 or r >= 6 or c >= 7 or self.get_token(grid, r, c) != player:
            if count != 3:
                rstop = row + (count + 1) * dr
                cstop = col + (count + 1) * dc
                if rstop < 0 or cstop < 0 or rstop >= 6 or cstop >= 7 or self.get_token(grid, rstop, cstop) != EMPTY:
                    return 0
            return score
# No Player tokens in this direction so dont care about previous token it will be calculated in the loop
        if count == 0:
            return 0

        score2 = 0
# the second token in the opposite direction
        rn = row - 2 * dr
        cn = col - 2 * dc

        count2 = 0

 # May be 2 in direction and one in the opposite
        if count == 2 and self.get_token(grid, r, c) == player:
            if (player == turn):
                score2 = 100
            else:
                score2 = 80
            return max(score, score2)
            # there is two tokens the same color in the opposite direction
        if not (rn < 0 or cn < 0 or rn >= 6 or cn >= 7 or self.get_token(grid, rn, cn) != player):
            count2 = 2

        if count2 == 2 and count == 1:
            score2 = 0
        else:
            score2 = 10
            # May be 2 in direction and one in the opposite

        return max(score, score2)
    
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
                    return True, self.get_token(grid, row, col)
        return False ,self.get_token(grid, row, col)

    def check_connect_4(self, grid, player, row, col):
        for direction in [(0, 1), (1, 0), (1, 1), (1, -1),(0,-1),(-1,0),(-1,-1),(-1,1)]:
            if self.check_direction(grid, player, row, col, direction) == True:
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

        flag,color = self.is_winning_state(grid,player)
        if depth == 0 or self.is_full(grid) or flag:
            return None, self.get_heuristic(grid,player)

        best_column = None
        best_value = -1000000 if player == RED else 1000000
        for column in range(0,7):
            if self.is_valid_column(grid,column):
                row = self.get_next_row(grid,column)
                self.insert_token(grid, column, row, player)
                _, value = self.minimax(grid, depth - 1, BLUE if player == RED else RED)
                self.print_grid(grid)
                print("score ",value)
                self.remove_token(grid, column, row)
                if player == RED and value > best_value:
                    best_column = column
                    best_value = value
                elif player == BLUE and value < best_value:
                    best_column = column
                    best_value = value
        print("------------------------")
        return  best_column,best_value
    
    def AlphaBetaPruning(self, grid, depth, player,alpha,beta):
        flag,color = self.is_winning_state(grid,player)
        #Cutooftest
        if depth == 0 or self.is_full(grid) or flag:
            return None, self.get_heuristic(grid,player)

        minV=1000000
        maxV = -1000000

        best_column = None
        for column in range(0,7):
            #Generate Child State
            if self.is_valid_column(grid,column):
                row = self.get_next_row(grid,column)
                self.insert_token(grid, column, row, player)
                _, value = self.AlphaBetaPruning(grid, depth - 1, BLUE if player == RED else RED,alpha,beta)
                self.print_grid(grid)
                print("score ",value)
                self.remove_token(grid, column, row)

                #Max Operation
                if player == RED:
                    if value>maxV:
                        best_column = column
                        maxV = value

                    if maxV>= beta:
                        return best_column,maxV

                    alpha = max(maxV,alpha)

                #MinOperation
                elif player == BLUE:
                    if value<minV:
                        best_column = column
                        minV = value

                    if minV<= alpha:
                        return best_column,minV
                    beta = min(minV,value)
        print("------------------------")
        if player == RED:
            return best_column, maxV
        else:
            return best_column, minV
    
    
