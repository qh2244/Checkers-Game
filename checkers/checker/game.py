from .constants import BLACK, RED, BLUE, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self):
        self._init()

    def update(self):
        """
        updates the game state by drawing the board, 
        drawing valid moves, checking for a winner, 
        and recording the winner
        """
        self.board.draw()
        self.draw_valid_moves(self.valid_moves)
        self.board.winner()
        self.board.record_winner()
    
    def check_winner(self):
        """
        checks if there is a winner in the game 
        and returns True if there is, False otherwise
        """
        if self.board.winner is not None:
            return True

    def _init(self):
        """
        initializes the game state by setting 
        the selected piece to None, creating a Board 
        object, setting the current turn to black, 
        and initializing the valid moves dictionary
        """
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def reset(self):
        """
        resets the game state by calling _init()
        """
        self._init()
    
    def select(self, row, col):
        """
        selects a piece to move by checking if the 
        given row and column contain a piece of the 
        current turn's color and setting the selected 
        piece and valid moves accordingly
        """
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False
    
    def _move(self, row, col):
        """
        moves the selected piece to the given 
        row and column, updating the board and 
        the turn if the move is valid
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        
        return True
    

    def draw_valid_moves(self, moves):
        """
        draws valid move indicators on the board using blue ellipses
        """
        for move in moves:
            row, col = move
            fill(*BLUE)
            ellipse(col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2, 15, 15)
    
    def change_turn(self):
        """
        switches the turn and clears the valid moves dictionary
        """
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = RED
        else:
            self.turn = BLACK
    
    def get_board(self):
        """
        returns the Board object
        """
        return self.board
    
    def ai_move(self, board):
        """
        sets the current board to the given board 
        and changes the turn to the other player 
        (i.e., the AI). This method is used to make a move for the AI.
        """
        self.board = board
        self.change_turn()