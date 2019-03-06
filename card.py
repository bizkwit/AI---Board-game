
import copy


class Card:
    """ A Card class is represents a card that the player plays with. A card
    has the following proporties:
    attributes:
    - is_horizontal = A boolean to check if the card is horizontal or vertical
    - points: An array of two points
    """

    # a constructor to initialize the card
    def __init__(self, Point1, Point2, position, card_num):
        self.is_horizontal = position
        self.p1 = Point1
        self.p2 = Point2
        self.p1.card = self
        self.p2.card = self
        self.cofig_num = card_num

    def __deepcopy__(self, memodict={}):
        return Card(copy.deepcopy(self.p1), copy.deepcopy(self.p2), self.is_horizontal)

    def __eq__(self, other):
        is_equal = False
        if self is other:
            is_equal = True
        elif type(self) == type(other) \
                and self.p1 == other.p1 \
                and self.p2 == other.p2 \
                and self.is_horizontal == other.is_horizontal:
            is_equal = True
        return is_equal

    def set_x(self, x):
        self.p1.x_coord = x
        if self.is_horizontal:
            self.p2.x_coord = x + 1
        else:
            self.p2.x_coord = x

    def set_y(self, y):
        self.p1.y_coord = y
        if self.is_horizontal:
            self.p2.y_coord = y
        else:
            self.p2.y_coord = y + 1

    def set_x_y(self, x, y):
        self.p1.x_coord = x
        self.p1.y_coord = y
        if self.is_horizontal:
            self.p2.x_coord = x + 1
            self.p2.y_coord = y
        else:
            self.p2.x_coord = x
            self.p2.y_coord = y + 1

    # a function to update the coordinates of the card before inserting
    # checks if the card is vertical or horizontal and updates correspondly
    # def update_coord(self,x,y):
    #   self.p1.x_coord = x
    #  self.p1.y_coord = y


class Point:
    """A point class is an inner class of the Card class. Points have the
    following properties:
    Attributes:
    - value: a string to visualize the point and to be put in the matrix
    - color: a string representing the color of the point
    - dot: a char represent whether the dot is blank or black
    - x_coord: int that stores the x coordinate. this will be determined by player later
    - y_coord: int that stores the y coordinate. this will be determined by player later
    !!! the color and dot are kept for an easier way to check winning state!!!
    """

    # initializes each point with a color
    def __init__(self, color, dot, card=None, x=0, y=0):
        if color == '_' or dot == '_':
            self.value = color
        else:
            self.value = color + dot
        self.card = card
        self.color = color
        self.dot = dot
        self.x_coord = x
        self.y_coord = y

    def __deepcopy__(self, memodict={}):
        return Point(self.color, self.dot, self.card, self.x_coord, self.y_coord)

    def __eq__(self, other):
        is_equal = False
        if self is other:
            is_equal = True
        elif type(self) == type(other) \
                and self.y_coord == other.y_coord \
                and self.x_coord == other.x_coord \
                and self.value == other.value:
            is_equal = True
        return is_equal


emptyPoint = Point("_", "_")


# returns the card with specific coordinates
def get_card(state_num, x=0, y=0):
    if 0 <= state_num >= 9:
        return
    elif state_num == 1:
        card = Card(Point("R", "*"), Point("W", "o"), True, state_num)
    elif state_num == 2:
        card = Card(Point("W", "o"), Point("R", "*"), False, state_num)
    elif state_num == 3:
        card = Card(Point("W", "o"), Point("R", "*"), True, state_num)
    elif state_num == 4:
        card = Card(Point("R", "*"), Point("W", "o"), False, state_num)
    elif state_num == 5:
        card = Card(Point("R", "o"), Point("W", "*"), True, state_num)
    elif state_num == 6:
        card = Card(Point("W", "*"), Point("R", "o"), False, state_num)
    elif state_num == 7:
        card = Card(Point("W", "*"), Point("R", "o"), True, state_num)
    else:
        card = Card(Point("R", "o"), Point("W", "*"), False,state_num)
    card.set_x_y(x, y)
    return card


# prints all the cards for the player to see
def print_cards():
    # colorama.init(autoreset=True)
    # RF = colored("*", "grey","on_red")
    # RE = colored("o", "grey","on_red")
    # WF = colored("*", "grey","on_white")
    # WE = colored("o","grey","on_white")

    # print("Here are the card configurations for you to choose:")
    # print("  ", RF,"  ",WE,"  ",RE,"  ",WF)
    # print(RF+WE, WE,WE+RF,RF,RE+WF,WF,WF+RE,RE)
    # print("1 ","2","3 ","4","5 ","6","7 ","8")

    print()
    print("Here are the card configurations for you to choose:")
    print("       ", "|R*|", "       ", "|Wo|", "       ", "|Ro|", "       ", "|W*|")
    print("|R* Wo|", "|Wo|", "|Wo R*|", "|R*|", "|Ro W*|", "|W*|", "|W* Ro|", "|Ro|")
    print("   1   ", " 2  ", "   3   ", " 4  ", "   5   ", " 6  ", "   7   ", " 8  ")


'''||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
   |||              print with colors                               |||
   ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    print("Here are the card configurations for you to choose:")
    print("  ", RF,"  ",WE,"  ",RE,"  ",WF)
    print(RF+WE, WE,WE+RF,RF,RE+WF,WF,WF+RE,RE)
    print("1 ","2","3 ","4","5 ","6","7 ","8")
'''