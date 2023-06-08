from .constants import BACKGROUND_COLOR1, ROWS, BACKGROUND_COLOR2, SQUARE_SIZE, BLACK, COLS, RED
from .piece import Piece
from .board import Board
    
def test_create_board():
    board = Board()
    assert len(board.board) == 8
    assert len(board.board[0]) == 8
    assert board.board[3][3] == 0
    assert board.board[4][4] == 0

def test_get_all_pieces():
    board = Board()
    red_pieces = board.get_all_pieces(RED)
    assert len(red_pieces) == 12
    black_pieces = board.get_all_pieces(BLACK)
    assert len(black_pieces) == 12

def test_has_legal_moves():
    board = Board()
    assert board.has_legal_moves(RED)
    assert board.has_legal_moves(BLACK)

def test_get_all_pieces():
    # Create a new board and place some pieces on it
    board = Board()
    board.board[0][1] = Piece(0, 1, "red")
    board.board[2][3] = Piece(2, 3, "red")
    board.board[5][2] = Piece(5, 2, "black")

    # Test getting all red pieces
    red_pieces = board.get_all_pieces("red")
    assert len(red_pieces) == 2
    assert red_pieces[0].row == 0 and red_pieces[0].col == 1
    assert red_pieces[1].row == 2 and red_pieces[1].col == 3

    # Test getting all black pieces
    black_pieces = board.get_all_pieces("black")
    assert len(black_pieces) == 1
    assert black_pieces[0].row == 5 and black_pieces[0].col == 2

    # Test getting pieces of a non-existent color
    no_pieces = board.get_all_pieces("green")
    assert len(no_pieces) == 0

def test_move():
    # Create a new board and place a piece on it
    board = Board()
    board.board[2][3] = Piece(2, 3, "red")

    # Make a valid move and check that the board is updated correctly
    piece = board.get_piece(2, 3)
    board.move(piece, 3, 4)
    assert board.board[2][3] == 0
    assert board.board[3][4] == piece
    assert piece.row == 3 and piece.col == 4
    assert board.red_kings == 0

def test_get_piece():
    board = Board()
    piece = board.board[2][1]
    assert board.get_piece(2, 1) == piece

def test_remove():
    # Create a new board and place some pieces on it
    board = Board()
    board.board[3][4] = Piece(3, 4, "black")
    board.board[4][3] = Piece(4, 3, "red")

    # Remove one piece and check that the board and count are updated correctly
    pieces = [board.get_piece(3, 4)]
    board.remove(pieces)
    assert board.board[3][4] == 0
    assert board.black_left == 12
    assert board.red_left == 11

    # Remove the remaining piece and check that the board and count are updated correctly
    pieces = [board.get_piece(4, 3)]
    board.remove(pieces)
    assert board.board[4][3] == 0
    assert board.black_left == 12
    assert board.red_left == 10

def test_is_draw():
    # Create a new board with moves_since_jump < 50
    board = Board()
    board.moves_since_jump = 0
    assert board.is_draw() == False
    # Create a new board with moves_since_jump = 50
    board = Board()
    board.moves_since_jump = 50
    assert board.is_draw() == True
    # Create a new board with moves_since_jump > 50
    board = Board()
    board.moves_since_jump = 60
    assert board.is_draw() == True

def test_make_move():
    board = Board()
    # Set up the board for the test
    board.board[3][4] = Piece(3, 4, BLACK)
    board.black_left = 1

    # Move the piece to (4, 3)
    board.make_move([ (3, 4), (4, 3) ])

    # Check that the moved piece is now at (4, 3)
    piece = board.board[4][3]
    assert piece is not None
    assert piece.color == BLACK
    assert piece.row == 4
    assert piece.col == 3

def test_get_valid_moves():
    # create a board with a black piece at (5, 2)
    board = Board()
    board.board[5][2] = Piece(5, 2, BLACK)
    # get the valid moves for the black piece at (5, 2)
    valid_moves = board.get_valid_moves(board.board[5][2])
    # ensure that there are no valid moves
    assert len(valid_moves) == 2
    # create a board with a red piece at (2, 5)
    board = Board()
    board.board[2][5] = Piece(2, 5, RED)
    # get the valid moves for the red piece at (2, 5)
    valid_moves = board.get_valid_moves(board.board[2][5])
    # ensure that there are no valid moves
    assert len(valid_moves) == 2

def test__traverse_left():
    board = Board()
    piece = Piece(3, 2, RED)
    board.board[3][2] = piece
    board.board[4][1] = Piece(4, 1, BLACK)
    board.board[2][1] = Piece(2, 1, BLACK)
    moves = board._traverse_left(3, 0, -1, RED, 1)
    assert len(moves) == 1
    assert (3, 1) in moves
    assert moves[(3, 1)] == []








