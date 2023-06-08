from checker.constants import WIDTH, HEIGHT, BACKGROUND_COLOR1, SQUARE_SIZE, BLACK, RED
from checker.game import Game
from minimax.algorithm import minimax

game = Game()
last_ai_move_time = 0
ai_move_delay = 3500  # 3.5 second delay

def setup():
    global game
    size(WIDTH, HEIGHT)

def draw():
    if game.board.winner() is not None:
        noLoop()
    global last_ai_move_time
    game.update()
    if game.turn == RED:
        current_time = millis()
        if current_time - last_ai_move_time >= ai_move_delay:
            value, new_board = minimax(game.get_board(), 3, RED, game)
            game.ai_move(new_board)
            last_ai_move_time = current_time
    winner = game.board.winner()
    if winner == BLACK:
        player_name = input('Enter your name: ')
        game.board.update_scores(player_name)


def get_row_col_from_mouse():
    x = mouseX
    y = mouseY
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def mousePressed():
    row, col = get_row_col_from_mouse()
    game.select(row, col)

def input(self, message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
