import board as board_m
import card as card_m


class Game:
    """ Stores all the date related to the game"""

    # a constructor to initialize the game
    def __init__(self):
        self.cards_count = 24
        self.moves_max = 60
        self.moves_left = 60

        self.game_mode_AI = False

        self.is_player1_color_option = None
        self.is_current_player1 = True
        self.player1_name = "Player1"
        self.player2_name = "Player2"
        self.is_file_input = False
        self.winner_found = False


letterConversion = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}


def try_parse_int(s):
    try:
        return int(s)
    except ValueError:
        return -1


def get_yes_no_input(message):
    answer = input(message + " (y/n)")
    if answer == 'y' or answer == 'Y':
        return True
    else:
        return False


def get_input_as_list(message=""):
    if game.is_file_input:
        index = game.moves_max - game.moves_left
        if index < len(file_input_list):
            input_s = file_input_list[index]
        else:
            input_s = ''
        print(input_s, end='')
    else:
        input_s = input(message)
    input_s = input_s.strip().upper().split(" ")
    return input_s


def validate_and_parse_move(inputs):
    """ inputs: a list of strings """
    is_valid_move_string = False
    # if regular move AND input size is correct AND first input is 0 and card rotation in range
    # and letter exist and Y-coord in range it is valid
    input_length = len(inputs)
    if input_length == 4:
        # regular move starts with a 0 as input
        if game.cards_count != 0 and inputs[0] == '0' and inputs[2] in letterConversion:
            inputs[1] = try_parse_int(inputs[1])  # card position(state)
            inputs[2] = letterConversion[inputs[2]]  # 1st point current X coordinate
            inputs[3] = try_parse_int(inputs[3])  # 1st point current y coordinate
            # verifying valid card position and if y coordinate is inside board boundaries
            if 0 < inputs[1] < 9 and 0 < inputs[3] <= board.num_rows:
                is_valid_move_string = True

    elif input_length == 7:
        # validation of x coordinates for points to be recycled
        if inputs[0] in letterConversion and inputs[2] in letterConversion:
            inputs[0] = letterConversion[inputs[0]]  # 1st point current x coordinate
            inputs[2] = letterConversion[inputs[2]]  # 2nd point current x coordinate
            inputs[1] = try_parse_int(inputs[1])  # 1st point current y coordinate
            inputs[3] = try_parse_int(inputs[3])  # 2st point current y coordinate
            # validation of y coordinates for points to be recycled
            if 0 < inputs[1] <= board.num_rows and 0 < inputs[3] <= board.num_rows:
                inputs[4] = try_parse_int(inputs[4])  # card position(state)
                inputs[6] = try_parse_int(inputs[6])  # 1st point new y coordinate
                # verifying valid card position and if x and y coordinates are inside board boundaries
                if 0 < inputs[4] < 9 and 0 < inputs[6] < board.num_rows and inputs[5] in letterConversion:
                    inputs[5] = letterConversion[inputs[5]]  # 1st point new x coordinate
                    is_valid_move_string = True
    return is_valid_move_string


def get_valid_input(message=""):
    input_list = get_input_as_list(message)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = validate_and_parse_move(input_list)
        if not is_valid_input:
            if game.is_file_input:
                game.is_file_input = False
                print("Next moves will be done in manual mode.")
            input_list = get_input_as_list("Input not valid, try again: ")
        else:
            return input_list


def place_card_from_input():
    is_valid_move = False
    input_list = get_valid_input()
    while not is_valid_move:
        if game.cards_count != 0:  # if true, it is a regular move
            x1 = input_list[2]
            y1 = input_list[3] - 1
            card = card_m.get_card(input_list[1], x1, y1)
            if board.validate_move(card):
                is_valid_move = True
        else:  # this is a recycling move
            x1 = input_list[0]
            y1 = input_list[1] - 1
            x2 = input_list[2]
            y2 = input_list[3] - 1
            # verifying if the points belong to the same card
            if board.board[y1][x1].card == board.board[y2][x2].card:
                placed_card = board.board[y1][x1].card
                new_x1 = input_list[5]
                new_y1 = input_list[6] - 1
                card = card_m.get_card(input_list[4], new_x1, new_y1)
                if placed_card == game.last_card_played:
                    print(" *** You can't recycle the last-played card ***")
                elif board.validate_recycling_move(placed_card, card):
                    is_valid_move = True
                elif placed_card == card:
                    print(" *** You must change card's rotation, position or both ***")
        if not is_valid_move:
            if game.is_file_input:
                game.is_file_input = False
                print("Next moves will be done in manual mode.")
            input_list = get_valid_input("Input not valid, try again: ")
        else:
            board.place_card(card)
            game.last_card_played = card
            if game.cards_count > 0:
                game.cards_count -= 1


play_again = True
print("Welcome to this awesome game")

while play_again:

    game = Game()
    board = board_m.Board(12, 8)
    game.is_file_input = get_yes_no_input("Read moves from file?")

    if game.is_file_input:
        read_file = open("input.txt", "r")
        file_input_list = read_file.readlines()
        read_file.close()

    game.player1_name = input("Player1, tell me your name: ")

    print("Ok " + game.player1_name + ", you have two options:")
    print("\t1: to play COLOURS\n\t2: to play DOTS")

    game.is_player1_color_option = input("Tell me you choice: ")

    # is_AI_play = get_yes_no_input("Do you want to challenge the AI?")

    while game.is_player1_color_option != '1' and game.is_player1_color_option != '2':
        game.is_player1_color_option = input("Your choice is not valid, try again: ")

    if game.is_player1_color_option == '1':
        game.is_player1_color_option = True
    else:
        game.is_player1_color_option = False

    game.player2_name = input("Player2, tell me your name: ")
    if game.is_player1_color_option:
        print(game.player2_name + ", you have no choice but to play DOTS")
    else:
        print(game.player2_name + ", you have no choice but to play COLOURS")

    print("\nExample of valid moves:\n\tRegular Move: '0 5 H 1' or '0 5 h 1' "
          "\n\tRecycling move: 'F 2 F 3 3 A 2' or 'f 2 f 3 3 a 2'")
    input("\nPress ENTER.....")

    board.print_board()
    card_m.print_cards()

    while not game.winner_found and game.moves_left >= 0:
        print("\nTurn: " + str(game.moves_max - game.moves_left + 1) + "/" + str(game.moves_max)
              + "\t Cards left: " + str(game.cards_count))
        if game.is_current_player1:
            print(game.player1_name + "'s turn: ", end='')
        else:
            print(game.player2_name + "'s turn: ", end='')

        place_card_from_input()
        board.print_board()
        card_m.print_cards()
        winner = board.verify_winning_state()

        if winner == board_m.Winner.NONE:
            game.is_current_player1 = not game.is_current_player1
        elif winner == board_m.Winner.COLORS or winner == board_m.Winner.DOTS:
            game.winner_found = True
        elif winner == board_m.Winner.TIE:
            game.moves_left = 0
        game.moves_left -= 1
    print("=================================")
    if not game.winner_found:
        print("Game ended with a tie")
    elif winner == board_m.Winner.COLORS:  # colors won
        if game.is_player1_color_option:
            print("Congratulations " + game.player1_name + ", you WON !!!")
        else:
            print("Congratulations " + game.player2_name + ", you WON !!!")
    elif winner == board_m.Winner.DOTS:  # dots won
        if game.is_player1_color_option:
            print("Congratulations " + game.player2_name + ", you WON !!!")
        else:
            print("Congratulations " + game.player1_name + ", you WON !!!")
    print("=================================")

    play_again = get_yes_no_input("\nDo you want to play one more time?")