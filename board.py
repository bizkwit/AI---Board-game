import card as card_m
from itertools import groupby
from enum import Enum


class Winner(Enum):
    NONE = 0
    COLORS = 1
    DOTS = 2
    TIE = 3


class Board:
    """ Class with all the necessary information and methods for the board """

    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = [[card_m.Point("_", "_") for j in range(num_cols)] for i in range(num_rows)]

    def print_board(self):
        """ Prints the game board """
        y = self.num_rows
        for row in reversed(range(1, self.num_rows + 1)):
            y -= 1
            print("\n" + str(row), end='')
            for x in range(self.num_cols):
                if self.board[y][x].value == "_":
                    print("\t_", end='')
                else:
                    print("\t" + self.board[y][x].value, end='')
        print("\n\n\tA\tB\tC\tD\tE\tF\tG\tH")

    def place_card(self, card):
        """Places a specific point in the board"""
        x = card.p1.x_coord
        y = card.p1.y_coord
        self.board[y][x] = card.p1
        x = card.p2.x_coord
        y = card.p2.y_coord
        self.board[y][x] = card.p2

    def validate_move(self, card):
        """ Validate a regular move"""
        is_valid_move = True
        x1 = card.p1.x_coord
        y1 = card.p1.y_coord
        x2 = card.p2.x_coord
        y2 = card.p2.y_coord

        # verifying if it is in our board range
        if 0 <= x1 < self.num_cols and 0 <= y1 < self.num_rows and 0 <= x2 < self.num_cols and 0 <= y2 < self.num_rows:

            # verifying if there is already a card in the desired position
            if self.board[y1][x1].value != "_" or self.board[y2][x2].value != "_":
                is_valid_move = False
            # if card is placed in the first row, we verify ONLY if x1 and x2 are inside the board range
            elif y1 == 0:
                if 0 > x1 >= self.board.size:
                    is_valid_move = False
                elif y2 == y1 and 0 > x2 >= self.board.size:
                        is_valid_move = False
            elif card.is_horizontal:
                # verifying if there is blank space under the desired placement of the horizontal card
                if self.board[y1-1][x1].value == "_" or self.board[y2-1][x2].value == "_":
                    is_valid_move = False
            else:
                # verifying if there is blank space under the desired placement of the vertical card
                if self.board[y1-1][x1].value == "_":
                    is_valid_move = False
        else:
            is_valid_move = False
        return is_valid_move

    def validate_recycling_move(self, card, new_card):
        """ Validate a recycling move"""
        if card is not None and new_card is not None\
                and card != new_card:
            is_valid_remove = True
            x1 = card.p1.x_coord
            y1 = card.p1.y_coord
            x2 = card.p2.x_coord
            y2 = card.p2.y_coord

            # verifying if the card is not in the last row
            if y2 < self.num_rows - 1:
                if card.is_horizontal:
                    # verify if there is any card above for horizontally placed card
                    if self.board[y2+1][x1].value != "_":
                        is_valid_remove = False
                else:
                    # verify if there is any card above
                    if y2 < self.num_rows-1 and self.board[y2+1][x2].value != "_":
                        is_valid_remove = False

            if is_valid_remove:
                self.board[y1][x1] = card_m.Point("_", "_")
                self.board[y2][x2] = card_m.Point("_", "_")
                is_valid_move = self.validate_move(new_card)
                # restore the points if the move cannot be made
                if not is_valid_move:
                    self.board[y1][x1] = card.p1
                    self.board[y2][x2] = card.p2
            else:
                is_valid_move = False
        else:
            is_valid_move = False
        return is_valid_move

    def verify_winning_state(self):
        occurrence_winner = Winner.NONE
        rows_colors, rows_dots, cols_colors, cols_dots, \
        diag_front_colors, diag_front_dots, diag_back_colors, diag_back_dots = [], [], [], [], [], [], [], []

        for i in range(self.num_rows):
            rows_colors.append('')
            rows_dots.append('')

        for i in range(self.num_cols):
            cols_colors.append('')
            cols_dots.append('')

        for i in range(self.num_rows + self.num_cols - 1):
            diag_front_colors.append('')
            diag_front_dots.append('')

        for i in range(len(diag_front_colors)):
            diag_back_colors.append('')
            diag_back_dots.append('')

        min_diag = -self.num_rows + 1

        for y in range(self.num_rows):
            for x in range(self.num_cols):
                rows_colors[y] += self.board[y][x].color
                rows_dots[y] += self.board[y][x].dot
                cols_colors[x] += self.board[y][x].color
                cols_dots[x] += self.board[y][x].dot
                diag_front_colors[x + y] += self.board[y][x].color
                diag_front_dots[x + y] += self.board[y][x].dot
                diag_back_colors[-min_diag + x - y] += self.board[y][x].color
                diag_back_dots[-min_diag + x - y] += self.board[y][x].dot

        arrays_of_colors_and_dots = [rows_colors, rows_dots, cols_colors, cols_dots, diag_front_colors,
                                    diag_front_dots, diag_back_colors, diag_back_dots]
        # running this outside the loop to be able to pass the True for is_row attribute
        occurrence_winner = verify_occurences(arrays_of_colors_and_dots[0],
                                              arrays_of_colors_and_dots[1], occurrence_winner, True)
        for i in range(2, len(arrays_of_colors_and_dots), 2):
            if occurrence_winner == Winner.TIE:
                return occurrence_winner
            occurrence_winner = verify_occurences(arrays_of_colors_and_dots[i],
                                                  arrays_of_colors_and_dots[i+1], occurrence_winner)
        return occurrence_winner


def verify_occurences(colors_list, dots_list, occurrence_winner, is_rows=False):
        for i in range(len(colors_list)):
            occurrences_colors = [(k, len(list(g))) for k, g in groupby(colors_list[i])]
            occurrences_dots = [(k, len(list(g))) for k, g in groupby(dots_list[i])]
            # verifying if any consecutive colors
            for arrays in occurrences_colors:
                if arrays[0] != "_" and arrays[1] >= 4:
                    if occurrence_winner == Winner.DOTS:
                        occurrence_winner = Winner.TIE
                        # if we already have a tie, we stop verifying any further
                        return occurrence_winner
                    else:
                        occurrence_winner = Winner.COLORS
                    break
            # verifying if any consecutive dots
            for arrays in occurrences_dots:
                if arrays[0] != "_" and arrays[1] >= 4:
                    if occurrence_winner == Winner.COLORS:
                        occurrence_winner = Winner.TIE
                        # if we already have a tie, we stop verifying any further
                        return occurrence_winner
                    else:
                        occurrence_winner = Winner.DOTS
                    break
            # if we already have a tie or if there are no more card on a row, we stop verifying any further
            if occurrence_winner == Winner.TIE or \
                    is_rows and len(occurrences_colors) == 1 and occurrences_colors[0][0] == "_":
                break
        return occurrence_winner
