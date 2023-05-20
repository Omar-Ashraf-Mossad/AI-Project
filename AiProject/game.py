from board import Board
import time
import random

# GAME LINK
# http://kevinshannon.com/connect4/

EMPTY = 0
RED = 1
BLUE = 2


def start(Method, Depth):
    board = Board()
    time.sleep(5)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()
        
        # FOR DEBUG PURPO   SES
        print("RECIEVED: ")
        board.print_grid(game_board)
        print("\n")
        print("--------------------")
        if game_end:
            break
        if Method == min:
            column, _ = board.AlphaBetaPruning(game_board, Depth, RED, -10000, 10000)
        board.select_column(column)
        time.sleep(2)

def main():
    import tkinter as tk

    def option_selected():
        selected_value = option_var.get()
        selected_value2 = option_var2.get()

        print("Selected Difficulity:", selected_value)
        print("Selected Algorithm:", selected_value2)

    root = tk.Tk()
    root.geometry("400x200")
    root.title("Connect 4")

    root.configure(bg='firebrick')
    option_var = tk.StringVar(root)
    option_var.set("Difficulity")

    option_menu1 = tk.OptionMenu(root, option_var, "Easy", "Medium", "Hard")
    option_menu1.config(bg="grey")
    option_menu1.pack()

    option_var2 = tk.StringVar(root)
    option_var2.set("Algorithm")

    option_menu2 = tk.OptionMenu(root, option_var2, "MinMax", "Alpha Beta Pruning")
    option_menu2.config(bg="grey")
    option_menu2.pack()

    button = tk.Button(root, text="Start", command=option_selected, bg="lime", fg="black")
    button.pack()

    root.mainloop()

if __name__ == "__main__":
     main()