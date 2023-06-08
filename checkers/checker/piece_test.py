from .piece import Piece
from .constants import RED, BLACK, SQUARE_SIZE, WHITE

def test_constructor():
    piece = Piece(2, 3, BLACK)
    assert piece.row == 2
    assert piece.col == 3
    assert piece.color == BLACK
    assert not piece.king
    assert piece.x == 3 * 100 + 50
    assert piece.y == 2 * 100 + 50

def test_make_king():
    piece = Piece(0, 0, RED)
    assert not piece.king
    piece.make_king()
    assert piece.king

def test_move():
    piece = Piece(2, 2, WHITE)
    piece.move(4, 5)
    assert piece.row == 4
    assert piece.col == 5
    assert piece.x == 5 * 100 + 50
    assert piece.y == 4 * 100 + 50