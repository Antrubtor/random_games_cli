import os
import sys
import time
import random
if os.name == "nt":
    import msvcrt
if os.name == "posix":
    import tty
    import select
    import termios

board_size = (15, 30)
speed = 0.03

class Square:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y

def spawn_fruit(board):
    fruit = (random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1))
    while board[fruit[0]][fruit[1]] == 1:
        fruit = (random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1))
    board[fruit[0]][fruit[1]] = 2
    sys.stdout.write(f"\x1B[{fruit[0] + 1};{fruit[1] * 2 + 1}H🟥\n")     # change cursor position and print the fruit square

def move(x_move, y_move, snake, board):   # move / print / call spawn_fruit
    eat = False
    if snake[0].x + x_move >= board_size[0] or \
        snake[0].y + y_move >= board_size[1] or \
        snake[0].x <= 0 or snake[0].y <= 0 or \
        board[snake[0].x + x_move][snake[0].y + y_move] == 1:
        return True    # if the snake is dead
    if board[snake[0].x + x_move][snake[0].y + y_move] == 2:
        snake.append(Square(snake[-1].x, snake[-1].y))
        board[snake[-1].x][snake[-1].y] = 1
        for i in range(len(snake) - 2, 0, -1):
            snake[i].x = snake[i - 1].x
            snake[i].y = snake[i - 1].y
            board[snake[i].x][snake[i].y] = 1
        eat = True
    else:
        sys.stdout.write(f"\x1B[{snake[-1].x + 1};{snake[-1].y * 2 + 1}H🔲\n")   # change cursor position and print the map square
        board[snake[-1].x][snake[-1].y] = 0
        for i in range(len(snake) - 1, 0, -1):
            snake[i].x = snake[i - 1].x
            snake[i].y = snake[i - 1].y
            board[snake[i].x][snake[i].y] = 1

    board[snake[0].x + x_move][snake[0].y + y_move] = 1
    snake[0].x += x_move
    snake[0].y += y_move
    sys.stdout.write(f"\x1B[{snake[0].x + 1};{snake[0].y * 2 + 1}H🔳\n")     # change cursor position and print the snake square
    if eat:
        spawn_fruit(board)
    return False

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')

def main():
    clear_terminal()
    snake = [Square(board_size[0] // 2, board_size[1] // 2), Square(board_size[0] // 2, board_size[1] // 2 - 1)]
    fruit = (random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1))
    while fruit[0] == snake[0].x or fruit[1] == snake[0].y or fruit[0] == snake[1].x or fruit[1] == snake[1].y:
        fruit = (random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1))
    board = []
    for i in range(board_size[0]):
        board.append([])
        for j in range(board_size[1]):
            if (snake[0].x == i and snake[0].y == j) or (snake[1].x == i and snake[1].y == j):
                board[i].append(1)  # 1 = with snake
            elif fruit[0] == i and fruit[1] == j:
                board[i].append(2)  # 2 = with fruit
            else:
                board[i].append(0)  # 0 = without snake

    direction = "right"
    dict_direction = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    for i in range(board_size[0]):  # print the board
        for j in range(board_size[1]):
            box = board[i][j]
            if box == 1:
                sys.stdout.write('🔳')
            elif box == 2:
                sys.stdout.write('🟥')
            else:
                sys.stdout.write('🔲')
        sys.stdout.write('\n')
    while True:
        di = direction
        if os.name == 'nt':     # get the key pressed / windows
            time.sleep(speed)
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H':
                        di = "up"
                    elif key == b'P':
                        di = "down"
                    elif key == b'K':
                        di = "left"
                    elif key == b'M':
                        di = "right"
        elif os.name == 'posix':    # get the key pressed / linux or mac
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setcbreak(sys.stdin.fileno())
                time.sleep(speed)
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1)
                    if key == '\x1b':
                        sys.stdin.read(1)
                        key = sys.stdin.read(1)
                        if key == 'A':
                            di = "up"
                        elif key == 'B':
                            di = "down"
                        elif key == 'C':
                            di = "right"
                        elif key == 'D':
                            di = "left"
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        if di == "up" and direction != "down" or di == "down" and direction != "up" \
            or di == "left" and direction != "right" or di == "right" and direction != "left":
            direction = di

        state = move(*dict_direction[direction], snake, board)
        if state:
            sys.stdout.write(f"\x1B[{board_size[0] + 1};0H")
            sys.stdout.write(f"You are dead with a score of {len(snake) - 2}.\n")
            break

if __name__ == "__main__":
    while True:
        main()
        sys.stdout.write("If you want to start a new game press enter, and if you want to exit, press 'q': ")
        if input() == 'q':
            break