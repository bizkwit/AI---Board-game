import card as card_m
from itertools import groupby

num_rows = 12
num_cols = 8
board = [[card_m.Point("_", "_") for j in range(num_cols)] for i in range(num_rows)]
letterConversion = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}

"""Prints the game board """
def print_board():
    y = num_rows
    for row in reversed(range(1, num_rows + 1)):
        y -= 1
        print("\n" + str(row), end='')
        for x in range(num_cols):
            if board[y][x].value == "_":
                print("\t_", end='')
            else:
                print("\t" + board[y][x].value, end='')
    print("\n\tA\tB\tC\tD\tE\tF\tG\tH")


def place_card(card):
    """Places a specific point in the board"""
    x = card.p1.x_coord
    y = card.p1.y_coord
    board[y][x] = card.p1
    x = card.p2.x_coord
    y = card.p2.y_coord
    board[y][x] = card.p2


def validate_move(card):
    """ Validate a regular move"""
    is_valid_move = True
    x1 = card.p1.x_coord
    y1 = card.p1.y_coord
    x2 = card.p2.x_coord
    y2 = card.p2.y_coord

    # verifying if it is in our board range
    if 0 <= x1 < num_cols and 0 <= y1 < num_rows and 0 <= x2 < num_cols and 0 <= y2 < num_rows:

        # verifying if there is already a card in the desired position
        if board[y1][x1].value != "_" or board[y2][x2].value != "_":
            is_valid_move = False
        # if card is placed in the first row, we verify ONLY if x1 and x2 are inside the board range
        elif y1 == 0:
            if 0 > x1 >= board.size:
                is_valid_move = False
            elif y2 == y1 and 0 > x2 >= board.size:
                    is_valid_move = False
        elif card.is_horizontal:
            # verifying if there is blank space under the desired placement of the horizontal card
            if board[y1-1][x1].value == "_" or board[y2-1][x2].value == "_":
                is_valid_move = False
        else:
            # verifying if there is blank space under the desired placement of the vertical card
            if board[y1-1][x1].value == "_":
                is_valid_move = False
    else:
        is_valid_move = False
    return is_valid_move


def validate_recycling_move(card, new_card):
    """ Validate a recycling move"""
    if card is not None:
        is_valid_remove = True
        x1 = card.p1.x_coord
        y1 = card.p1.y_coord
        x2 = card.p2.x_coord
        y2 = card.p2.y_coord

        # verifying if the card is not in the last row
        if y2 < num_rows - 1:
            if card.is_horizontal:
                # verify if there is any card above for horizontally placed card
                if board[y2+1][x1].value != "_":
                    is_valid_remove = False
            else:
                # verify if there is any card above
                if y2 < num_rows-1 and board[y2+1][x2] != "_":
                    is_valid_remove = False

        if is_valid_remove:
            board[y1][x1] = card_m.Point("_", "_")
            board[y2][x2] = card_m.Point("_", "_")
            is_valid_move = validate_move(new_card)
            # restore the points if the move cannot be made
            if not is_valid_move:
                board[y1][x1] = card.p1
                board[y2][x2] = card.p2
        else:
            is_valid_move = False
    else:
        is_valid_move = False
    return is_valid_move


def verify_winning_state(is_player1_color_option):
    max_col = len(board[0])
    max_row = len(board)
    rows = [[] for i in range(max_row)]
    cols = [[] for i in range(max_col)]
    diag_front = [[] for i in range(max_row + max_col - 1)]
    diag_back = [[] for i in range(len(diag_front))]
    min_diag = -num_rows + 1

    for y in range(num_rows):
        for x in range(num_cols):
            rows[y].append(board[y][x].value)
            cols[x].append(board[y][x].value)
            diag_front[x + y].append(board[y][x].value)
            diag_back[-min_diag + x - y].append(board[y][x].value)


    for row in rows:
            #occurrences_row = [(k, sum(1 for i in g)) for k, g in groupby(row)]
        str1 = ''.join(row)
        str2 = str1.replace('R', '')
        str3 = str2.replace('W', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == True:
                    print("Consecutive " + arrays[0] + " found in a row. Color player, you lost the game. Dots player you win!")
                if is_player1_color_option == False:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a row. Dots player, you won the game.")
                return True

    for column in cols:
        str1 = ''.join(column)
        str2 = str1.replace('R', '')
        str3 = str2.replace('W', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == True:
                    print("Consecutive " + arrays[0] + " found in a column. Color player, you lost the game. Dots player you win!")
                if is_player1_color_option == False:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a column. Dots player, you won the game.")
                return True

    for diagonal in diag_front:
        str1 = ''.join(diagonal)
        str2 = str1.replace('R', '')
        str3 = str2.replace('W', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == True:
                    print("Consecutive " + arrays[0] + " found in a diagonal. Color player, you lost the game. Dots player you win!")
                if is_player1_color_option == False:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a diagonal. Dots player, you won the game.")
                return True

    for diagonal in diag_back:
        str1 = ''.join(diagonal)
        str2 = str1.replace('R', '')
        str3 = str2.replace('W', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == True:
                    print("Consecutive " + arrays[0] + " found in a diagonal. Color player, you lost the game. Dots player you win!")
                if is_player1_color_option == False:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a diagonal. Dots player, you won the game.")
                return True

    for row in rows:
        #occurrences_row = [(k, sum(1 for i in g)) for k, g in groupby(row)]
        str1 = ''.join(row)
        str2 = str1.replace('*', '')
        str3 = str2.replace('o', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == False:
                    print("Consecutive " + arrays[0] + " found in a row. Dots player, you lost the game. Color player you win!")
                if is_player1_color_option == True:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a row. Color player, you won the game.")
                return True

    for column in cols:
        str1 = ''.join(column)
        str2 = str1.replace('*', '')
        str3 = str2.replace('o', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == False:
                    print("Consecutive " + arrays[0] + " found in a column. Dots player, you lost the game. Color player you win")
                if is_player1_color_option == True:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a column. Color player, you won the game.")
                return True

    for diagonal in diag_front:
        str1 = ''.join(diagonal)
        str2 = str1.replace('*', '')
        str3 = str2.replace('o', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == False:
                    print("Consecutive " + arrays[0] + " found in a diagonal. Dots player, you lost the game. Color player you win")
                if is_player1_color_option == True:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a diagonal. Color player, you won the game.")
                return True

    for diagonal in diag_back:
        str1 = ''.join(diagonal)
        str2 = str1.replace('*', '')
        str3 = str2.replace('o', '')
        str4 = str3.replace('_', '')

        occurrences = [(k, len(list(g))) for k, g in groupby(str4)]

        for arrays in occurrences:
            if arrays[1] == 4:
                if is_player1_color_option == False:
                    print("Consecutive " + arrays[0] + " found in a diagonal. Dots player, you lost the game. Color player you win")
                if is_player1_color_option == True:
                    print("Congratulation! Consecutive " + arrays[0] + " found in a diagonal. Color player, you won the game.")
                return True

    return False
