def e(board):
    result = 0
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            if board.matrix[row][col].value == "Wo":
                result += col * 10 + row + 1
            elif board.matrix[row][col].value == "W*":
                result += 3 * (col * 10 + row + 1)
            elif board.matrix[row][col].value == "R*":
                result -= 2 * (col * 10 + row + 1)
            elif board.matrix[row][col].value == "Ro":
                result -= 1.5 * (col * 10 + row + 1)
    return result
