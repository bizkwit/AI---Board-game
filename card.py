from termcolor import colored
class Card:
    """ A Card class is represents a card that the player plays with. A card
    has the following proporties:
    attributes:
    - is_horizontal = A boolean to check if the card is horizontal or vertical
    - points: An array of two points
    """

    # a constructor to initialize the card
    def __init__(self, Point1, Point2, position):
        self.is_horizontal = position
        self.p1 = Point1
        self.p2 = Point2
        self.p1.card = self
        self.p2.card = self
        self.points = [self.p1, self.p2]

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


redFilled = 'R*'
whiteFilled = 'W*'
redEmpty = 'Ro'
whiteEmpty = 'Wo'


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
    def __init__(self, color, dot):
        if color == "white" and dot == "o":
            self.value = whiteEmpty
        elif color == 'white' and dot == "*":
            self.value = whiteFilled
        elif color == 'red' and dot == "o":
            self.value = redEmpty
        elif color == 'red' and dot == "*":
            self.value = redFilled
        elif color == "_" and dot == "_":
            self.value = "_"
        self.card = None
        self.color = color
        self.dot = dot
        self.x_coord = 0
        self.y_coord = 0


# returns the card with specific coordinates
def get_card(state_num, x=0, y=0):
    if 0 <= state_num >= 9:
        return
    elif state_num == 1:
        card = Card(Point("red", "*"), Point("white", "o"), True)
    elif state_num == 2:
        card = Card(Point("white", "o"), Point("red", "*"), False)
    elif state_num == 3:
        card = Card(Point("white", "o"), Point("red", "*"), True)
    elif state_num == 4:
        card = Card(Point("red", "*"), Point("white", "o"), False)
    elif state_num == 5:
        card = Card(Point("red", "o"), Point("white", "*"), True)
    elif state_num == 6:
        card = Card(Point("white", "*"), Point("red", "o"), False)
    elif state_num == 7:
        card = Card(Point("white", "*"), Point("red", "o"), True)
    else:
        card = Card(Point("red", "o"), Point("white", "*"), False)
    card.set_x_y(x, y)
    return card

#prints all the cards for the player to see
def print_cards():
    RF = colored("*", "grey","on_red")
    RE = colored("o", "grey","on_red")
    WF = colored("*", "grey","on_white")
    WE = colored("o","grey","on_white")

    print()
    print("Here are the card configurations for you to choose:")
    print("       ", "|R*|","       ", "|Wo|","       ", "|Ro|","       ", "|W*|")
    print("|R* Wo|", "|Wo|","|Wo R*|", "|R*|","|Ro W*|", "|W*|","|W* Ro|", "|Ro|")
    print("   1   ", " 2  ","   3   ", " 4  ","   5   ", " 6  ","   7   ", " 8  ")
'''||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
   |||              print with colors                               |||
   ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
   
    print("Here are the card configurations for you to choose:")
    print("  ", RF,"  ",WE,"  ",RE,"  ",WF)
    print(RF+WE, WE,WE+RF,RF,RE+WF,WF,WF+RE,RE)
    print("1 ","2","3 ","4","5 ","6","7 ","8")
'''