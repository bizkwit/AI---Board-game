
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
