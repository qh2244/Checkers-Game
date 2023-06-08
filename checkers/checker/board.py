from .constants import BACKGROUND_COLOR1, ROWS, BACKGROUND_COLOR2, SQUARE_SIZE, BLACK, COLS, RED
from .piece import Piece


class Board:
    def __init__(self):
        """
        Initializes the Board object with an empty 2D list 
        representing the game board, sets the initial number 
        of black and red pieces and kings, creates the board, 
        and sets the initial turn to black and number of moves 
        since the last jump to 0.
        """
        self.board = [] # 2D list
        self.black_left = self.red_left = 12
        self.black_kings = self.red_kings = 0
        self.create_board()
        self.turn = BLACK
        self.moves_since_jump = 0

    def draw_squares(self):
        """
        Draws the squares of the board using the 
        BACKGROUND_COLOR1 and BACKGROUND_COLOR2 
        constants, which represent the colors of the squares.
        """
        noStroke()
        background(*BACKGROUND_COLOR1)
        for row in range(ROWS): 
            for col in range(row % 2, ROWS, 2):
                fill(*BACKGROUND_COLOR2)
                rect(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    
    def evaluate(self):
        """
        Evaluates the current state of 
        the board by subtracting the number 
        of black pieces and kings from the 
        number of red pieces and kings, and 
        adding half the number of kings for each player.
        """
        return self.red_left - self.black_left + (self.red_kings * 0.5 - self.black_kings * 0.5)

    def get_all_pieces(self, color):
        """
        Returns a list of all pieces of the given color on the board.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def has_legal_moves(self, color):
        """
        Returns True if the given color has 
        any legal moves left on the board, False otherwise.
        """
        for piece in self.get_all_pieces(color):
            if self.get_valid_moves(piece):
                return True
        return False

    
    def move(self, piece, row, col):
        """
        Moves the given piece to the given row and column, 
        swaps the positions of the two pieces, and updates 
        the position of the moved piece. If the piece reaches 
        the opposite end of the board, it becomes a king.
        """
        # swap
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            if not piece.king:  # check if the piece is not already a king
                piece.make_king()
                if piece.color == RED:
                    self.red_kings += 1
                else:
                    self.black_kings += 1

    def get_piece(self, row, col):
        """
        Returns the piece at the given row and column.
        """
        return self.board[row][col]

    def create_board(self):
        """
        Creates the initial game board by filling the 
        2D list with pieces of the appropriate color and position.
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self):
        """
        Draws the board and all pieces on it.
        """
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw()
    
    def remove(self, pieces):
        """
        Removes the given pieces from the board and updates 
        the number of pieces for the appropriate player.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.red_left -= 1

    def is_draw(self):
        """
        Returns True if the game has ended in a draw 
        (50 moves without a capture), False otherwise.
        """
        return self.moves_since_jump >= 50
    
    def make_move(self, move):
        """
        Makes the given move by calling the move() method
        and removing any captured pieces. Updates the number 
        of moves since the last jump.
        """
        piece = self.get_piece(move[0][0], move[0][1])
        dest = move[-1]
        if len(move) > 2:
            skips = move[1:-1]
        else:
            skips = []
        self.move(piece, dest[0], dest[1])
        if skips:
            self.remove(skips)
            self.moves_since_jump = 0
        else:
            self.moves_since_jump += 1

    def winner(self):
        """
        Returns the winner of the game, or None if the game is not over yet.
        """
        if self.moves_since_jump >= 50:
            textSize(100)
            fill(255, 255, 255)
            textAlign(CENTER)
            text("Draw!", width/2, height/2)
            return None

        if self.black_left <= 0:
            textSize(100)
            fill(255, 255, 255)
            textAlign(CENTER)
            text("Red Wins!", width/2, height/2)
            return RED
        elif self.red_left <= 0:
            textSize(100)
            fill(255, 255, 255)
            textAlign(CENTER)
            text("Black Wins!", width/2, height/2)
            return BLACK
        elif not self.has_legal_moves(self.turn):
            if self.turn == BLACK:
                textSize(100)
                fill(255, 255, 255)
                textAlign(CENTER)
                text("Red Wins!", width/2, height/2)
                return RED
            if self.turn == RED:
                textSize(100)
                fill(255, 255, 255)
                textAlign(CENTER)
                text("Black Wins!", width/2, height/2)
                return BLACK
            
        return None

    def record_winner(self):
        """
        Records the winner of the game in a file and updates the scores.
        """
        winner = self.winner()
        if winner is not None:
            if winner == RED:
                print("AI wins")
                self.update_scores('AI')
            else:
                print("Black wins")
        else:
            return None

    def update_scores(self, winner):
        """
        Updates the scores in the scores.txt file with the winner of the game.
        """
        scores = []
        with open('scores.txt', 'r') as f:
            for line in f:
                scores.append(line.strip().split())

        found = False
        for i, score in enumerate(scores):
            if score[0] == winner:
                scores[i][1] = str(int(scores[i][1]) + 1)
                found = True
                break

        if not found:
            scores.append([winner, '1'])

        scores.sort(key=lambda x: int(x[1]), reverse=True)

        with open('scores.txt', 'w') as f:
            for score in scores:
                f.write(score[0] + ' ' + score[1] + '\n')

    def get_valid_moves(self, piece):
        """
        Returns a dictionary of all valid moves 
        for the given piece, including any captures.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        A private method that traverses diagonally to the left to find valid moves for a piece.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
        A private method that traverses diagonally to the right to find valid moves for a piece.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
