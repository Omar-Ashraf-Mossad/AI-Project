from board import Board
import time
import tkinter as tk
from threading import Thread
import random

# GAME LINK
# http://kevinshannon.com/connect4/

EMPTY = 0
RED = 1
BLUE = 2

root = tk.Tk()
root.geometry("400x200")

root.configure(bg='tomato')
option_var = tk.StringVar(root)
option_var2 = tk.StringVar(root)
option_var3 = tk.StringVar(root)

Levels=['Easy', 'Medium', 'Hard']

Methods = ['MinMax', 'Alpha Beta Pruning']
Versus = ['Site Ai', 'Random Computer']

def start():
    Method = option_var2.get()
    Depth =option_var.get()

    if Depth not in Levels:
        return
    if Method not in Methods:
        return

    if option_var3.get() not in Versus:
        return

    if Depth == Levels[0]:
        Depth = 1

    if Depth == Levels[1]:
        Depth = 4

    if Depth == Levels[2]:
        Depth = 5


    if Method == Methods[0]:
        Method = "minimax"
    else:
        Method = "alphabeta"

    random1 = False
    if option_var3.get() == Versus[1]:
        random1 = True

    board = Board()
    time.sleep(5)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        print("RECIEVED: ")
        board.print_grid(game_board)
        print("\n")
        print("--------------------")
        column = 0
        if game_end:
            break
        if Method == "minimax":
            column, _ = board.minimax(game_board, Depth, RED)
        else:
            column, _ = board.AlphaBetaPruning(game_board, Depth, RED,-1000000,1000000)

        board.select_column(column)

        if random1:
            random_column = random.randint(0, 6)

            while not board.is_valid_column(game_board,random_column) and not board.is_full(game_board):
                random_column = random.randint(0, 6)

            board.select_column(random_column)

        time.sleep(2)

def startThread():
    new_thread = Thread(target=start)
    new_thread.start()






option_var.set("Difficulity")

option_menu1 = tk.OptionMenu(root, option_var,*Levels )
option_menu1.config(bg="grey")
option_menu1.pack()
option_menu1.config(bg="dark sea green",fg="Black")
option_menu1.pack(side= 'right',expand=True)

option_var2.set("Algorithm")

option_menu2 = tk.OptionMenu(root, option_var2, *Methods )
option_menu2.config(bg="grey")

option_menu2.pack()
option_menu2.config(bg="dark sea green",fg="Black")
option_menu2.pack(side= 'left',expand=True)

option_var3.set("Play against")

option_menu3 = tk.OptionMenu(root, option_var3, *Versus )
option_menu3.config(bg="grey")

option_menu3.pack()
option_menu3.config(bg="dark sea green",fg="Black")
option_menu3.pack(side= 'left',expand=True)

button = tk.Button(root,width=5, text="Start", command=lambda:startThread(), bg="lime", fg="black")
button.place(x=180,y=120)
root.mainloop()




