#from gameplay import trace_nb
import gameTree as gameTree_m
import board as board_m


board = board_m.Board(12, 8)
game_tree = gameTree_m.GameTree(gameTree_m.State(board, 0))
print(game_tree.get_e())
