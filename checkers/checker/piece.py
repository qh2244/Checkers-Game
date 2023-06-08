from .constants import SQUARE_SIZE, WHITE

class Piece:
    def __init__(self, row, col, color):
        """
        constructs a new Piece object with the given row, column, and color
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    
    def calc_pos(self):
        """
        calculates the position of the piece based on its row and column
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """
        sets the king attribute to True
        """
        if not self.king:
            self.king = True
    
    def draw(self):
        """
        draws the piece on the screen using 
        the x and y attributes to determine the position.
        """
        stroke(*WHITE)
        strokeWeight(2)
        fill(*self.color)
        ellipse(self.x, self.y, SQUARE_SIZE * 0.8, SQUARE_SIZE * 0.8)
        fill(*self.color)
        strokeWeight(2)
        ellipse(self.x, self.y, SQUARE_SIZE * 0.6, SQUARE_SIZE * 0.6)
        if self.king:
            crown = loadImage("crown.png")
            crown.resize(50,50)
            image(crown, self.x - crown.width//2, self.y - crown.height//2)  # draw the crown image

    def move(self, row, col):
        """
        sets the new row and column of the piece and recalculates its position
        """
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        """
        returns a string representation of the piece
        """
        return str(self.color)