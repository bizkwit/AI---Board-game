import card as card_m
import board as board_m
import copy
import timeit


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

    def __init__(self, current_player=0, current_value=0, parent_state=None, board=board_m.Board(12, 8)):
        self.player = current_player
        self.value = current_value
        self.parent = parent_state
        self.children = []
        self.board_state = board

    # inserts a new state into the children list

    def add_child(self, new_child):
        self.children.append(new_child)

    def set_parent(self, parent_node):
        self.parent = parent_node

    def set_state_value(self, new_value):
        self.value = new_value


class GameTree:
    """ A game tree class where the game tree in getting managed and handled.
        It has the following properties:
        - DEPTH = serves as a constant that give a limit of the tree depth
        - root = serves a the root of the current game tree
    """

    DEPTH = 4  # treated as a constant

    # default constructor
    def __init__(self):
        self.root = None

    # updates the root to the current state

    def update_root(self, current_state):
        self.root = current_state

    def create_states_from_parent(self, parent_node):

        for i in range(1, 9):
            for j in range(0, 9):
                skipper = False
                for k in range(0, 13):
                    if skipper:
                        continue
                    card = card_m.get_card(i, j, k)
                    current_board = copy.deepcopy(parent_node.board_state)
                    if current_board.validate_move(card):
                        current_board.place_card(card)
                        new_state = State(1, 0, parent_node, current_board)
                        parent_node.add_child(new_state)
                        skipper = False
                    else:
                        skipper = True

    def print_nodes_from_parent(self, parent_node):
        print("Parent: ")
        parent_node.board_state.print_board()
        i = 1
        for child in parent_node.children:
            print("Child: ", i)
            child.board_state.print_board()
            i = i + 1                

    def create_tree(self):
        if self.root is None:
            # creating the root state with empty board
            start = State(1)
            self.update_root(start)
        self.create_states_from_parent(self.root)
        for child in self.root.children:
            self.create_states_from_parent(child)