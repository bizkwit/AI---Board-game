import board as board_m
import card as card_m
import gameplay as gp

game = gp.Game()

print("Welcome to this awesome game")

def get_yes_no_input(message):
    answer = input(message)
    if answer == 'y' or answer == 'Y':
        return True
    else:
        return False

game.is_file_input = get_yes_no_input("Read moves from file? (y/n)")

game.player1_name = input("Player1, tell me your name: ")

print("Ok " + game.player1_name + ", you have two options:")
print("\t1: to play COLOURS\n\t2: to play DOTS")


game.is_player1_color_option = input("Tell me you choice: ")

# if debug:
#     is_AI_play = False
# else:
#     is_AI_play = get_yes_no_input("Do you want to challenge the AI? (y/n)")

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

input("Press ENTER.....")

board_m.print_board()
card_m.print_cards()
print("Example:\n\tRegular Move: 05H1 or 05h1 \n\tRecycling move: F2F33A2 or f2f33a2")

print(game.player1_name + ", make your first move: ", end='')
while not game.winner_found and game.moves_left >= 0:
    game.place_card_from_input()
    state = board_m.verify_winning_state(game.is_player1_color_option)
    if state == 0:
        game.winner_found == False
    elif state == 1:
        game.winner_found == True
        game.is_current_player1 = True
    else:
        game.winner_found == True
        game.is_current_player1 = False

    if game.is_current_player1:
        if game.winner_found:
            break
        else:
            game.is_current_player1 = False
            print(game.player2_name + ": ", end='')
    else:
        if game.winner_found:
            break
        else:
            game.is_current_player1 = True
            print(game.player1_name + ": ", end='')
    game.moves_left -= 1
    board_m.print_board()
    card_m.print_cards()
    print("\nTurn: " + str(game.moves_max - game.moves_left) + "/" + str(game.moves_max)
          + "\t Cards left: " + str(game.cards_count) + "\n")

if not game.winner_found:
    print("Game ended with a tie")
