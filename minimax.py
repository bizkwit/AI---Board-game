from itertools import groupby
from board import Winner
import card as card_m


class MiniMax:
    matrix_point_value = None
    e_call_counter = 0

    @classmethod
    def calculate_board_values(cls, board):
        cls.matrix_point_value = []
        for y in range(board.num_rows):
            value = y * 10 + 1
            cls.matrix_point_value.append([])
            for x in range(board.num_cols):
                cls.matrix_point_value[y].append(value)
                value += 1


def e(board):
    MiniMax.e_call_counter += 1
    if MiniMax.matrix_point_value is None:
        MiniMax.calculate_board_values(board)
    result = 0
    for row in range(board.num_rows):
        if row > 0 and board.point_counter_rows[row - 1] == 0:
            break
        for col in range(board.num_cols):
            if board.point_counter_cols[col] == 0:
                continue
            if board.matrix[row][col].value == "Wo":
                result += MiniMax.matrix_point_value[row][col]
            elif board.matrix[row][col].value == "W*":
                result += 3 * MiniMax.matrix_point_value[row][col]
            elif board.matrix[row][col].value == "R*":
                result -= 2 * MiniMax.matrix_point_value[row][col]
            elif board.matrix[row][col].value == "Ro":
                result -= 1.5 * MiniMax.matrix_point_value[row][col]
    return result


def get_e():
    global nb_e
    return str(nb_e)


def e2(board, is_colors=True, is_max=True):
    occurrence_winner = Winner.NONE
    rows_colors, rows_dots, cols_colors, cols_dots, \
    diag_front_colors, diag_front_dots, diag_back_colors, diag_back_dots = [], [], [], [], [], [], [], []
    max_points_height = board.num_rows
    for i in range(max_points_height):
        # if there are no points on the row, we stop
        if board.point_counter_rows[i] == 0:
            max_points_height = i
            break
        rows_colors.append('')
        rows_dots.append('')

    for i in range(board.num_cols):
        cols_colors.append('')
        cols_dots.append('')

    for i in range(max_points_height + board.num_cols - 1):
        diag_front_colors.append('')
        diag_front_dots.append('')

    for i in range(len(diag_front_colors)):
        diag_back_colors.append('')
        diag_back_dots.append('')

    min_diag = -max_points_height + 1

    for y in range(max_points_height):
        # if there are no points on the row, we stop
        if board.point_counter_rows[y] == 0:
            break
        for x in range(board.num_cols):
            rows_colors[y] += board.matrix[y][x].color
            rows_dots[y] += board.matrix[y][x].dot
            cols_colors[x] += board.matrix[y][x].color
            cols_dots[x] += board.matrix[y][x].dot
            diag_front_colors[x + y] += board.matrix[y][x].color
            diag_front_dots[x + y] += board.matrix[y][x].dot
            diag_back_colors[-min_diag + x - y] += board.matrix[y][x].color
            diag_back_dots[-min_diag + x - y] += board.matrix[y][x].dot

    arrays_of_colors_and_dots = [rows_colors, rows_dots, cols_colors, cols_dots, diag_front_colors,
                                 diag_front_dots, diag_back_colors, diag_back_dots]
    result = 0
    # running this outside the loop to be able to pass the True for is_row attribute
    for i in range(0, len(arrays_of_colors_and_dots), 2):
        if occurrence_winner == Winner.TIE:
            break
        result, occurrence_winner = verify_occurences(arrays_of_colors_and_dots[i],
                                                      arrays_of_colors_and_dots[i + 1], occurrence_winner, is_colors,
                                                      result, is_max)
    return result  #, occurrence_winner


def verify_occurences(colors_list, dots_list, occurrence_winner, is_colors, result, is_max):
    if is_colors:
        colors = -2
        dots = 1
    else:
        colors = 1
        dots = -2

    if is_max:
        colors *= -1
        dots *= -1

    for i in range(len(colors_list)):
        occurrences_colors = [(k, len(list(g))) for k, g in groupby(colors_list[i])]
        occurrences_dots = [(k, len(list(g))) for k, g in groupby(dots_list[i])]
        # verifying if any consecutive colors
        for occurrence in occurrences_colors:
            if occurrence[0] != card_m.emptyPoint.value and occurrence[1] >= 4:
                if occurrence_winner == Winner.DOTS:
                    occurrence_winner = Winner.TIE
                    result = -500000  # We make the tie a big negative number but higher then the loss
                    # if we already have a tie, we stop verifying any further
                    break
                else:
                    result = colors * 1000000
                    occurrence_winner = Winner.COLORS
                break  # we found a winner so we stop searching for it
            else:
                result += colors * occurrence[1]
        if occurrence_winner == Winner.TIE:
            break
        # verifying if any consecutive dots
        for occurrence in occurrences_dots:
            if occurrence[0] != card_m.emptyPoint.value and occurrence[1] >= 4:
                if occurrence_winner == Winner.COLORS:
                    occurrence_winner = Winner.TIE
                    result = -500000  # We make the tie a big negative number but higher then the loss
                    # if we already have a tie, we stop verifying any further
                    break
                else:
                    result = dots * 1000000
                    occurrence_winner = Winner.DOTS
                break  # we found a winner so we stop searching for it
            else:
                result += dots * occurrence[1]
        # if we already have a tie, we stop verifying any further
        if occurrence_winner == Winner.TIE:
            break
    return result, occurrence_winner
