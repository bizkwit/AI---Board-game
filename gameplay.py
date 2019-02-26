import board as board_m
import card as card_m



class Game:
    """ Stores all the date related to the game"""

    # a constructor to initialize the game
    def __init__(self):
        self.cards_count = 24
        self.moves_max = 60
        self.moves_left = 60

        self.is_player1_color_option = None
        self.is_current_player1 = True
        self.player1_name = "Player1"
        self.player2_name = "Player2"
        self.is_file_input = False
        self.winner_found = False


#game = Game()


# def get_yes_no_input(message):
#     answer = input(message)
#     if answer == 'y' or answer == 'Y':
#         return True
#     else:
#         return False


#print("Welcome to this awesome game")

#game.is_file_input = get_yes_no_input("Read moves from file? (y/n)")

# if game.is_file_input:
#     read_file = open("input.txt", "r")
#     file_input_list = read_file.readlines()
#     read_file.close()


# game.player1_name = input("Player1, tell me your name: ")
#
# print("Ok " + game.player1_name + ", you have two options:")
# print("\t1: to play COLOURS\n\t2: to play DOTS")
#
#
# game.is_player1_color_option = input("Tell me you choice: ")
#
# # if debug:
# #     is_AI_play = False
# # else:
# #     is_AI_play = get_yes_no_input("Do you want to challenge the AI? (y/n)")

# while game.is_player1_color_option != '1' and game.is_player1_color_option != '2':
#     game.is_player1_color_option = input("Your choice is not valid, try again: ")
#
# if game.is_player1_color_option == '1':
#     game.is_player1_color_option = True
# else:
#     game.is_player1_color_option = False
#
#
# game.player2_name = input("Player2, tell me your name: ")
# if game.is_player1_color_option:
#     print(game.player2_name + ", you have no choice but to play DOTS")
# else:
#     print(game.player2_name + ", you have no choice but to play COLOURS")
#
# input("Press ENTER.....")
#
# board_m.print_board()
# card_m.print_cards()
# print("Example:\n\tRegular Move: 05H1 or 05h1 \n\tRecycling move: F2F33A2 or f2f33a2")


    def validate_move_string(self, input_s):
        is_valid_move_string = False
        # if regular move AND input size is correct AND first input is 0 and card rotation in range
        # and letter exist and Y-coord in range it is valid

        regular_move = self.cards_count != 0
        len_4 = len(input_s) == 4
        if len_4:
            char_0_zero = input_s[0] == '0'
            char_1_valid_num = 0 < int(input_s[1]) < 9
            char_2_valid_letter = input_s[2] in board_m.letterConversion
            char_3_valid_row = 0 < int(input_s[3]) <= board_m.num_rows

        len_7 = len(input_s) == 7
        if len_7:
            char_0_valid_letter = input_s[0] in board_m.letterConversion
            char_1_valid_row = 0 < int(input_s[1]) <= board_m.num_rows
            char_4_valid_col = 0 < int(input_s[4]) <= board_m.num_cols
            char_5_valid_letter = input_s[5] in board_m.letterConversion
            char_6_valid_row = 0 < int(input_s[6]) <= board_m.num_rows

        if (regular_move and len_4 and char_0_zero and char_1_valid_num and
                char_2_valid_letter and char_3_valid_row):
            is_valid_move_string = True
        elif (len_7 and char_0_valid_letter and char_1_valid_row and
              char_4_valid_col and char_5_valid_letter and char_6_valid_row):
            is_valid_move_string = True
        return is_valid_move_string

    def get_input_as_list(self, message=""):
        if self.is_file_input:
            read_file = open("input.txt", "r")
            file_input_list = read_file.readlines()
            read_file.close()
            index = self.moves_max - self.moves_left
            if index < len(file_input_list):
                input_s = file_input_list[index]
            else:
                input_s = ''
        else:
            input_s = input(message)
        input_s = input_s.strip().upper().split(" ")
        return input_s


    def get_valid_input(self, message=""):
        input_s = self.get_input_as_list(message)
        is_valid_input = False
        while not is_valid_input:
            is_valid_input = self.validate_move_string(input_s)
            if not is_valid_input:
                if self.is_file_input:
                    self.is_file_input = False
                    print("Input: is not valid.")
                    print("Next moves will be done in manual mode.")
                input_s = self.get_input_as_list("Input not valid, try again: ")
            else:
                return input_s


    def place_card_from_input(self):
        is_valid_move = False
        input_s = self.get_valid_input()
        while not is_valid_move:
            # if true, it means that it is a regular move
            if self.cards_count != 0:
                x1 = board_m.letterConversion[input_s[2]]
                y1 = int(input_s[3]) - 1
                card = card_m.get_card(int(input_s[1]), x1, y1)
                if board_m.validate_move(card):
                    is_valid_move = True
            # this is a recycling move
            else:
                x1 = board_m.letterConversion[input_s[0]]
                y1 = int(input_s[1]) - 1
                x2 = board_m.letterConversion[input_s[2]]
                y2 = int(input_s[3]) - 1
                #verifying if the points belong to the same card
                if board_m.board[y1][x1].card == board_m.board[y2][x2].card:
                    placed_card = board_m.board[y1][x1].card
                    new_x1 = board_m.letterConversion[input_s[5]]
                    new_y1 = int(input_s[6]) - 1
                    card = card_m.get_card(int(input_s[4]), new_x1, new_y1)
                    if placed_card != self.last_card_played and board_m.validate_recycling_move(placed_card, card):
                        is_valid_move = True
            if not is_valid_move:
                if self.is_file_input:
                    self.is_file_input = False
                    print("There is already a card in the location provided.")
                    print("Next moves will be done in manual mode.")
                input_s = self.get_valid_input("Input not valid, try again: ")
            else:
                board_m.place_card(card)
                self.last_card_played = card
                if self.cards_count > 0:
                    self.cards_count -= 1


# print(game.player1_name + ", make your first move: ", end='')
# while not game.winner_found and game.moves_left >= 0:
#     place_card_from_input()
#     state = board_m.verify_winning_state(game.is_player1_color_option)
#     if state == 0:
#         game.winner_found == False
#     elif state == 1:
#         game.winner_found == True
#         game.is_current_player1 = True
#     else:
#         game.winner_found == True
#         game.is_current_player1 = False
#
#     if game.is_current_player1:
#         if game.winner_found:
#             break
#         else:
#             game.is_current_player1 = False
#             print(game.player2_name + ": ", end='')
#     else:
#         if game.winner_found:
#             break
#         else:
#             game.is_current_player1 = True
#             print(game.player1_name + ": ", end='')
#     game.moves_left -= 1
#     board_m.print_board()
#     card_m.print_cards()
#     print("\nTurn: " + str(game.moves_max - game.moves_left) + "/" + str(game.moves_max)
#           + "\t Cards left: " + str(game.cards_count) + "\n")
#
# if not game.winner_found:
#     print("Game ended with a tie")
