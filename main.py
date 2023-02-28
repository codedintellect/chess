import chess
import ui

board = chess.Board()
ui.init(board)
print('yay')
board.push_san("e4")
