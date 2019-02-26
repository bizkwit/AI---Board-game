
class State:
    ''' A state class represents a state which is a node in a game tree.
        A state is a possible next move that can be made.
        It has the following properties:
        - player = an integer where '-1' is MIN and '+1' is MAX
        - value = an int which is given by applying the e(n)
        - parent = another state object as a parent state
        - board = a board object with a current board configuration
        - children = a list of states as the children states
    '''


    def __init__(self,player_num, board_config):
        self.player = player_num
        self.value = 0
        self.parent = None
        self.board_state = board_config
        self.children = []

    #inserts a new state into the children list
    @classmethod
    def add_child(self, new_child):
        self.children.append(new_child)


class GameTree:
    ''' A game tree class where the game tree in getting managed and handled.
        It has the following proporties:
        - DEPTH = serves as a constatnt that give a limit of the tree depth
        - root = serves a the root of the current game tree
    '''

    DEPTH = 4 #treated as a constant

    #defult constructor
    def __init__ (self):
            self.root = None

    #updates the root to the current state
    @classmethod
    def update_root(current_state):
        root = current_state
