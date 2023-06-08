from .game import Game
from .constants import BLACK, RED, BLUE, SQUARE_SIZE

def test_game_init():
    game = Game()
    assert game.turn == BLACK
    assert game.selected == None
    assert game.valid_moves == {}
    assert game.board != None

def test_game_reset():
    game = Game()
    game.select(5, 0)
    game.reset()
    assert game.turn == BLACK
    assert game.selected == None
    assert game.valid_moves == {}
    assert game.board != None

def test_game_select():
    game = Game()
    assert game.select(0, 1) == False
    assert game.select(5, 0) == True
    assert game.selected != None
    assert game.valid_moves != {}

def test_game_move():
    game = Game()
    game.select(5, 0)
    assert game._move(4, 1) == True
    assert game.board.get_piece(4, 1) != 0
    assert game.board.get_piece(5, 0) == 0
    assert game.turn == RED

def test_game_change_turn():
    game = Game()
    game.change_turn()
    assert game.turn == RED
    game.change_turn()
    assert game.turn == BLACK

def test_game_get_board():
    game = Game()
    assert game.get_board() == game.board

def test_game_ai_move():
    game = Game()
    board = game.get_board()
    game.ai_move(board)
    assert game.turn == RED