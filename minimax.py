import gameTree as gameTree_m
import time

class Minimax:

    MAX = 1
    MIN = -1

    def __init__(self):
        self.player = 1
        #self.moves = []

    def player_switch(self, player):
        if player == 1:
            player == -1
        elif player == -1:
            player == 1
        return player

    def bot(self, node, depth, player):
        lowest_score = float("-inf")
        highest_score = float("inf")
        game = gameTree_m.GameTree()
        game.root = node
        game.create_tree(depth)
        while depth > 0:
            for child in game.root.children:
                child.value = self.e(child.board_state)
                print(child.value)
                if player == -1:
                    if child.value < highest_score:
                        highest_score = child.value
                        best_move = [highest_score]
                elif player == 1:
                    if child.value > lowest_score:
                        lowest_score = child.value
                        best_move = [lowest_score]
            self.bot(child, depth-1, -player)
            return best_move, child.board_state.print_board(), child.value

    @staticmethod
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

start_time = time.time()
newgame = gameTree_m.GameTree()
AI = Minimax()
print(AI.bot(newgame.root, 2, 1))
total_time = time.time() - start_time
print("--- method execution time: %s seconds ---" %(total_time))

