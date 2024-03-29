import card as card_m
from itertools import groupby
import copy
from enum import Enum


class Winner(Enum):
    NONE = 0
    COLORS = 1
    DOTS = 2
    TIE = 3


class Board:
    """ Class with all the necessary information and methods for the board """

    def __init__(self, num_rows, num_cols, board=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.matrix = [[card_m.emptyPoint for j in range(num_cols)] for i in range(num_rows)]
        self.point_counter_rows, self.point_counter_cols = [], []
        if board is None:
            self.winner = Winner.NONE
            self.last_card_played = None
            self.point_counter_rows = [0 for i in range(num_rows)]
            self.point_counter_cols = [0 for i in range(num_cols)]
        else:
            self.winner = board.winner
            self.last_card_played = copy.deepcopy(board.last_card_played)
            for counter in board.point_counter_rows:
                self.point_counter_rows.append(counter)
            for counter in board.point_counter_cols:
                self.point_counter_cols.append(counter)
            for i in range(num_rows):
                for j in range(num_cols):
                    if board.matrix[i][j] is not card_m.emptyPoint and self.matrix[i][j] is card_m.emptyPoint:
                        card = copy.deepcopy(board.matrix[i][j].card)
                        self.matrix[card.p1.y_coord][card.p1.x_coord] = card.p1
                        self.matrix[card.p2.y_coord][card.p2.x_coord] = card.p2

    def __deepcopy__(self, memodict={}):
        return Board(self.num_rows, self.num_cols, self)

    def print_board(self):
        """ Prints the game board """
        y = self.num_rows
        for row in reversed(range(1, self.num_rows + 1)):
            y -= 1
            print("\n" + str(row), end='')
            for x in range(self.num_cols):
                if self.matrix[y][x] is card_m.emptyPoint:
                    print("\t_", end='')
                # elif self.matrix[y][x].card == self.last_card_played:
                #     print("\tL" + self.matrix[y][x].value, end='')
                else:
                    print("\t" + self.matrix[y][x].value, end='')
        print("\n\n\tA\tB\tC\tD\tE\tF\tG\tH")

    def place_card(self, card):
        """Places a specific point in the board"""
        x = card.p1.x_coord
        y = card.p1.y_coord
        self.matrix[y][x] = card.p1
        self.point_counter_cols[x] += 1
        self.point_counter_rows[y] += 1
        x = card.p2.x_coord
        y = card.p2.y_coord
        self.matrix[y][x] = card.p2
        self.point_counter_cols[x] += 1
        self.point_counter_rows[y] += 1
        self.last_card_played = card

    def remove_card(self, card):
        x = card.p1.x_coord
        y = card.p1.y_coord
        self.matrix[y][x] = card_m.emptyPoint
        self.point_counter_cols[x] -= 1
        self.point_counter_rows[y] -= 1
        x = card.p2.x_coord
        y = card.p2.y_coord
        self.matrix[y][x] = card_m.emptyPoint
        self.point_counter_cols[x] -= 1
        self.point_counter_rows[y] -= 1

    def validate_move(self, card, is_ai_move=False):
        """ Validate a regular move"""
        is_valid_move = True
        x1 = card.p1.x_coord
        y1 = card.p1.y_coord
        x2 = card.p2.x_coord
        y2 = card.p2.y_coord

        # verifying if it is in our board range
        if 0 <= x1 < self.num_cols and 0 <= y1 < self.num_rows and 0 <= x2 < self.num_cols and 0 <= y2 < self.num_rows:
            # verifying if there is already a card in the desired position
            # if card is placed in the first row, we verify ONLY if x1 and x2 are inside the board range
            if self.matrix[y1][x1] is not card_m.emptyPoint or self.matrix[y2][x2] is not card_m.emptyPoint:
                is_valid_move = False
            elif y1 > 0:
                if card.is_horizontal:
                    # verifying if there is blank space under the desired placement of the horizontal card
                    if self.matrix[y1-1][x1] is card_m.emptyPoint or self.matrix[y2-1][x2] is card_m.emptyPoint:
                        is_valid_move = False
                else:
                    # verifying if there is blank space under the desired placement of the vertical card
                    if self.matrix[y1 - 1][x1] is card_m.emptyPoint:
                        is_valid_move = False
            if is_ai_move and y1 == 0 and self.point_counter_rows[y1] > 0:
                if card.is_horizontal:
                    if x1 == 0:
                        if self.matrix[y2][x2 + 1] is card_m.emptyPoint:
                            is_valid_move = False
                    elif x2 == self.num_cols - 1:
                        if self.matrix[y1][x1-1] is card_m.emptyPoint:
                            is_valid_move = False
                    elif self.matrix[y1][x1-1] is card_m.emptyPoint and self.matrix[y2][x2 + 1] is card_m.emptyPoint:
                        is_valid_move = False
                else:
                    if x1 == 0:
                        if self.matrix[y1][x1 + 1] is card_m.emptyPoint:
                            is_valid_move = False
                    elif x1 == self.num_cols - 1:
                        if self.matrix[y1][x1-1] is card_m.emptyPoint:
                            is_valid_move = False
                    elif self.matrix[y1][x1-1] is card_m.emptyPoint and self.matrix[y1][x1 + 1] is card_m.emptyPoint:
                        is_valid_move = False
        else:
            is_valid_move = False
        return is_valid_move

    def validate_remove(self, placed_card, remove_card=False):
        if placed_card is not None and placed_card != self.last_card_played:
            is_valid_remove = True
            x1 = placed_card.p1.x_coord
            y1 = placed_card.p1.y_coord
            x2 = placed_card.p2.x_coord
            y2 = placed_card.p2.y_coord

            # verifying if the card is not in the last row
            if y2 < self.num_rows - 1:
                if placed_card.is_horizontal:
                    # verify if there is any card above for horizontally placed card
                    if self.matrix[y1 + 1][x1] is not card_m.emptyPoint or \
                            self.matrix[y2 + 1][x2] is not card_m.emptyPoint:
                        is_valid_remove = False
                else:
                    # verify if there is any card above
                    if self.matrix[y2 + 1][x2] is not card_m.emptyPoint:
                        is_valid_remove = False
        else:
            is_valid_remove = False
        if remove_card and is_valid_remove:
            self.remove_card(placed_card)
        return is_valid_remove

    def place_recycling_move(self, placed_card, new_card):
        """ Validate a recycling move"""

        if new_card is not None and placed_card != new_card:
            if self.validate_remove(placed_card):
                x1 = placed_card.p1.x_coord
                y1 = placed_card.p1.y_coord
                x2 = placed_card.p2.x_coord
                y2 = placed_card.p2.y_coord

                self.matrix[y1][x1] = card_m.emptyPoint
                self.matrix[y2][x2] = card_m.emptyPoint
                is_valid_move = self.validate_move(new_card)
                # restore the points if the move cannot be made
                if not is_valid_move:
                    self.matrix[y1][x1] = placed_card.p1
                    self.matrix[y2][x2] = placed_card.p2
                else:
                    self.remove_card(placed_card)
                    self.place_card(new_card)
            else:
                is_valid_move = False
        else:
            is_valid_move = False
        return is_valid_move

    def verify_winning_state(self):
        occurrence_winner = Winner.NONE
        rows_colors, rows_dots, cols_colors, cols_dots, \
        diag_front_colors, diag_front_dots, diag_back_colors, diag_back_dots = [], [], [], [], [], [], [], []
        max_points_height = self.num_rows
        for i in range(max_points_height):
            # if there are no points on the row, we stop
            if self.point_counter_rows[i] == 0:
                max_points_height = i
                break
            rows_colors.append('')
            rows_dots.append('')

        for i in range(self.num_cols):
            cols_colors.append('')
            cols_dots.append('')

        for i in range(max_points_height + self.num_cols - 1):
            diag_front_colors.append('')
            diag_front_dots.append('')

        for i in range(len(diag_front_colors)):
            diag_back_colors.append('')
            diag_back_dots.append('')

        min_diag = -max_points_height + 1

        for y in range(max_points_height):
            # if there are no points on the row, we stop
            if self.point_counter_rows[y] == 0:
                break
            for x in range(self.num_cols):
                rows_colors[y] += self.matrix[y][x].color
                rows_dots[y] += self.matrix[y][x].dot
                cols_colors[x] += self.matrix[y][x].color
                cols_dots[x] += self.matrix[y][x].dot
                diag_front_colors[x + y] += self.matrix[y][x].color
                diag_front_dots[x + y] += self.matrix[y][x].dot
                diag_back_colors[-min_diag + x - y] += self.matrix[y][x].color
                diag_back_dots[-min_diag + x - y] += self.matrix[y][x].dot

        arrays_of_colors_and_dots = [rows_colors, rows_dots, cols_colors, cols_dots, diag_front_colors,
                                     diag_front_dots, diag_back_colors, diag_back_dots]
        # running this outside the loop to be able to pass the True for is_row attribute
        occurrence_winner = verify_occurences(arrays_of_colors_and_dots[0],
                                              arrays_of_colors_and_dots[1], occurrence_winner)
        for i in range(2, len(arrays_of_colors_and_dots), 2):
            if occurrence_winner == Winner.TIE:
                return occurrence_winner
            occurrence_winner = verify_occurences(arrays_of_colors_and_dots[i],
                                                  arrays_of_colors_and_dots[i + 1], occurrence_winner)
        return occurrence_winner


def verify_occurences(colors_list, dots_list, occurrence_winner):
    for i in range(len(colors_list)):
        occurrences_colors = [(k, len(list(g))) for k, g in groupby(colors_list[i])]
        occurrences_dots = [(k, len(list(g))) for k, g in groupby(dots_list[i])]
        # verifying if any consecutive colors
        for occurrence in occurrences_colors:
            if occurrence[0] != card_m.emptyPoint.value and occurrence[1] >= 4:
                if occurrence_winner == Winner.DOTS:
                    occurrence_winner = Winner.TIE
                    # if we already have a tie, we stop verifying any further
                    break
                else:
                    occurrence_winner = Winner.COLORS
                break  # we found a winner so we stop searching for it
        # verifying if any consecutive dots
        for occurrence in occurrences_dots:
            if occurrence[0] != card_m.emptyPoint.value and occurrence[1] >= 4:
                if occurrence_winner == Winner.COLORS:
                    occurrence_winner = Winner.TIE
                    # if we already have a tie, we stop verifying any further
                    break
                else:
                    occurrence_winner = Winner.DOTS
                break  # we found a winner so we stop searching for it
        # if we already have a tie, we stop verifying any further
        if occurrence_winner == Winner.TIE:
            break
    return occurrence_winner