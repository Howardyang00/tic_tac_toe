import cv2
import numpy as np
import random

player_symbol = ''
bot_symbol = ''
board = [['', '', ''], ['', '', ''], ['', '', '']]
img = None

def create_blank_board():
    return np.ones((300, 300, 3), dtype=np.uint8) * 255

def coord_to_pixel(x, y):
    px = (x - 1) * 100 + 50
    py = (3 - y) * 100 + 50
    return (px, py)

def draw_grid(img):
    for i in range(1, 3):
        cv2.line(img, (i * 100, 0), (i * 100, 300), (0, 0, 0), 2)
        cv2.line(img, (0, i * 100), (300, i * 100), (0, 0, 0), 2)

def draw_symbol(img, symbol, x, y):
    center = coord_to_pixel(x, y)
    if symbol == 'O':
        cv2.circle(img, center, 40, (255, 0, 0), 2)
    elif symbol == 'X':
        cx, cy = center
        cv2.line(img, (cx - 40, cy - 40), (cx + 40, cy + 40), (0, 0, 255), 2)
        cv2.line(img, (cx - 40, cy + 40), (cx + 40, cy - 40), (0, 0, 255), 2)

def update_board_image():
    global img
    img = create_blank_board()
    draw_grid(img)
    for y in range(3):
        for x in range(3):
            symbol = board[y][x]
            if symbol != '':
                draw_symbol(img, symbol, x + 1, 3 - y)
    cv2.imshow('Tic Tac Toe', img)
    cv2.waitKey(500)

def rof():
    global player_symbol, bot_symbol
    outcome = random.choice(["player", "bot"])
    print(f"Coin toss result: {outcome}")
    if outcome == "player":
        player_symbol = "X"
        bot_symbol = "O"
        return "Player"
    else:
        player_symbol = "O"
        bot_symbol = "X"
        return "Bot"

def get_empty_cells():
    return [(x + 1, 3 - y) for y in range(3) for x in range(3) if board[y][x] == '']

def player_move(x, y):
    if board[3 - y][x - 1] == '':
        board[3 - y][x - 1] = player_symbol
        update_board_image()

def bot_move():
    empty_cells = get_empty_cells()
    if empty_cells:
        x, y = random.choice(empty_cells)
        board[3 - y][x - 1] = bot_symbol
        update_board_image()

def check_winner():
    for y in range(3):
        if board[y][0] == board[y][1] == board[y][2] != '':
            return board[y][0]
    for x in range(3):
        if board[0][x] == board[1][x] == board[2][x] != '':
            return board[0][x]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def reset_board():
    global board
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    update_board_image()

def main():
    reset_board()
    turn = rof()
    update_board_image()

    while True:
        winner = check_winner()
        if winner:
            print(f"Winner: {winner}")
            break
        elif not get_empty_cells():
            print("It's a draw!")
            break

        if turn == "Player":
            try:
                user_input = input("Enter your move (x y, e.g., 2 3): ")
                x, y = map(int, user_input.strip().split())
                if 1 <= x <= 3 and 1 <= y <= 3 and board[3 - y][x - 1] == '':
                    player_move(x, y)
                    turn = "Bot"
                else:
                    print("Invalid move. Try again.")
            except:
                print("Invalid input. Please enter two numbers, e.g., 2 3")
        else:
            print("Bot is making a move...")
            bot_move()
            turn = "Player"

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
