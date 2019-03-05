def e(board):
    result = 0
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            if board.board[row][col].value == "Wo":
                result += row * 10 + col + 1
            if board.board[row][col].value == "W*":
                result += 3 * (row * 10 + col + 1)
            if board.board[row][col].value == "R*":
                result -= 2 * (row * 10 + col + 1)
            if board.board[row][col].value == "Ro":
                result -= 1.5 * (row * 10 + col + 1)
    return result
