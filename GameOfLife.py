import os
import sys
import time
import random

speed = 0.3
board_size = (15, 30)
nb_cells = board_size[0] * board_size[1] // 8   # number of cells alive in the board to start the game

def init_board(board_size, nb_cells):
    board = [[0 for i in range(board_size[1])] for j in range(board_size[0])]
    for i in range(nb_cells):
        x = random.randint(0, board_size[0] - 1)
        y = random.randint(0, board_size[1] - 1)
        board[x][y] = 1
    return board

def check_neighbour(board, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0) or x + i < 0 or y + j < 0 or x + i >= board_size[0] or y + j >= board_size[1]:  # out of bounds
                continue
            if board[x + i][y + j] == 1:
                count += 1
    return count

def update_board(board):
    new_board = [[0 for i in range(board_size[1])] for j in range(board_size[0])]
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            count = check_neighbour(board, i, j)
            if board[i][j] == 1:
                if count < 2 or count > 3:
                    new_board[i][j] = 0
                else:
                    new_board[i][j] = 1
            else:
                if count == 3:
                    new_board[i][j] = 1
    stuck = True
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            if board[i][j] != new_board[i][j]:
                stuck = False
                if new_board[i][j] == 0:
                    sys.stdout.write(f"\x1B[{i + 1};{j * 2 + 1}H🔲\n")
                else:
                    sys.stdout.write(f"\x1B[{i + 1};{j * 2 + 1}H🔳\n")     # change cursor position and print the square
            board[i][j] = new_board[i][j]
    return stuck

def main():
    board = init_board(board_size, nb_cells)
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    for i in range(board_size[0]):  # print the board
        for j in range(board_size[1]):
            if board[i][j] == 0:
                sys.stdout.write("🔲")
            else:
                sys.stdout.write("🔳")
        sys.stdout.write("\n")

    while True:
        if update_board(board):
            break
        time.sleep(speed)

if __name__ == "__main__":
    while True:
        main()
        sys.stdout.write(f"\x1B[{board_size[0] + 1};0H")
        sys.stdout.write("To restart the game press enter, otherwise enter 'q' to exit: ")
        if input() == 'q':
            break