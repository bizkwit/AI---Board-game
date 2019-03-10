import card as card_m
import board as board_m
import copy
import time
from minimax import *

class State:
    """ A state class represents a state which is a node in a game tree.
        A state is a possible next move that can be made.
        It has the following properties:
        - player = an integer where '-1' is MIN and '+1' is MAX
        - value = an int which is given by applying the e(n)
        - parent = another state object as a parent state
        - board = a board object with a current board configuration
        - children = a list of states as the children states
    """

    def __init__(self, board, current_player=0, current_value=0, parent_state=None):

        self.player = current_player
        self.value = current_value
        self.parent = parent_state
        self.children = []
        self.board_state = board
        self.counter = 0
        self.e_value = 0
        self.e_array = []
    # inserts a new state into the children list

    def add_child(self, new_child):
        self.children.append(new_child)

    def set_parent(self, parent_node):
        self.parent = parent_node
        self.board_state = board_m.Board(parent_node.board_state.num_rows, parent_node.board_state.num_cols)

    def set_state_value(self, new_value):
        self.value = new_value

    def generate_best_move_state(self, is_last_depth=False, is_max=True):
        global nb_e
        for i in range(1, 9):  # card state number to get the card
            for y in range(0, self.board_state.num_rows):
                # if there is no card under previous row, we don't check next rows
                if y > 0 and self.board_state.point_counter_rows[y - 1] == 0:
                    break
                # if the row is full, we skip the row
                if self.board_state.point_counter_rows[y] == self.board_state.num_cols:
                    continue
                for x in range(0, self.board_state.num_cols):
                    # if there is no cards in this column and y is greater then 0, we skip the column
                    # if the column is full, we skip the column
                    if y > 0 and self.board_state.point_counter_cols[x] == 0 \
                            or self.board_state.point_counter_cols[x] == self.board_state.num_rows:
                        continue
                    card = card_m.get_card(i, x, y)
                    if self.board_state.validate_move(card):
                        current_board = copy.deepcopy(self.board_state)
                        current_board.place_card(card)
                        if is_last_depth:
                            value = e(current_board)
                            self.counter += 1
                            self.e_value = value
                            self.e_array.append(value)
                        else:
                            value = 0
                        new_state = State(current_board, 1, value, self)
                        self.add_child(new_state)
        if is_last_depth:
            if is_max:
                self.value = max(child.value for child in self.children)
            else:
                self.value = min(child.value for child in self.children)
            self.children = []

    # !!!!!!!!!!!!  NEEDS TESTING !!!!!!!!!!!!!!!!!
    def generate_best_recycled_move_state(self, removed_card, is_max):
        for i in range(1, 9):  # card state number to get the card
            for y in range(0, self.board_state.num_rows):
                # if there is no card under previous row, we don't check next rows
                if y > 0 and self.board_state.point_counter_rows[y - 1] == 0:
                    break
                for x in range(0, self.board_state.num_cols):
                    # if there is no cards in this column and y is greater then 0, we skip the column
                    # if the column is full, we skip the column
                    if y > 0 and self.board_state.point_counter_cols[x] == 0 \
                            or self.board_state.point_counter_cols[x] == self.board_state.num_rows:
                        continue
                    card = card_m.get_card(i, x, y)
                    if card == removed_card:
                        continue
                    if self.board_state.validate_move(card):
                        board = copy.deepcopy(self.board_state)
                        board.place_card(card)
                        new_state = State(board, 1, e(board), self)
                        self.add_child(new_state)
        if is_max:
            best_state = max(self.children, key=lambda state: state.value)
        else:
            best_state = min(self.children, key=lambda state: state.value)
        self.board_state = best_state.board_state
        self.value = best_state.value
        self.children = []

    def get_counter(self):
        return self.counter

    def get_e_val(self):
        return self.value

    def get_e_array(self):
        return self.e_array

class GameTree:
    """ A game tree class where the game tree in getting managed and handled.
        It has the following properties:
        - DEPTH = serves as a constant that give a limit of the tree depth
        - root = serves a the root of the current game tree
    """

    DEPTH = 4  # treated as a constant

    # default constructor
    def __init__(self, root):
        self.root = root

    # updates the root to the current state

    def update_root(self, current_state):
        self.root = current_state

    def get_best_move(self, is_max):
        self.root.generate_best_move_state()
        for child in self.root.children:
            child.generate_best_move_state(True, not is_max)
        # self.root.value, self.root = mm_m.bot(self.root, 2, 1)
        if is_max:
            best_state = max(self.root.children, key=lambda state: state.value)
        else:
            best_state = min(self.root.children, key=lambda state: state.value)
        return best_state

    # !!!!!!!!!!!! NEEDS TESTING !!!!!!!!!!!!!!!!!
    def get_best_recycle_move(self, game, is_max):
        best_state = self.root
        for y in range(self.root.board_state.num_rows):
            # if the row has no cards, we stop
            if self.root.board_state.point_counter_rows[y] == 0:
                break
            for x in range(self.root.board_state.num_cols):
                # if the column has no cards, we skip
                if self.root.board_state.point_counter_cols[x] == 0 or \
                   self.root.board_state.matrix[y][x].card == game.last_card_played:
                    continue
                # if valid remove, we create a new state with removed card
                if self.root.board_state.validate_remove(self.root.board_state.matrix[y][x].card):
                    board = copy.deepcopy(self.root.board_state)
                    removed_card = self.root.board_state.matrix[y][x].card
                    board.remove_card(self.root.board_state.matrix[y][x].card)
                    child = State(board, is_max, 0, self.root)
                    # generating best recycling move state for this removed card
                    child.generate_best_recycled_move_state(removed_card, is_max)
                    if is_max:
                        if best_state.value < child.value:
                            best_state = child
                    else:
                        if best_state.value > child.value:
                            best_state = child
        self.update_root(best_state)

    def get_best_state(self, is_max, game):
        if game.cards_count > 0:
            self.update_root(self.get_best_move(is_max))
            game.cards_count -= 1
        else:
            self.get_best_recycle_move(game, is_max)

    def print_tree(self):
        number_of_nodes = 1
        parent_number = 0
        self.root.board_state.print_board()
        for child in self.root.children:
            number_of_nodes += 1
            parent_number += 1
            print("Parent: ", parent_number, "Value: ", child.value)
            child.board_state.print_board()
            child_number = 1
            for child1 in child.children:
                number_of_nodes += 1
                print(" Parent: ", parent_number, "Child: ", child_number, "Value: ", child1.value)
                child1.board_state.print_board()
                child_number = child_number + 1
        print("Root Value: ", self.root.value)
        print("Root Board: ")
        self.root.board_state.print_board()
        print("Total Nodes: ", number_of_nodes)

    def get_e(self):
        return MiniMax.e_call_counter
