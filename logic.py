import chess

class game:
  def __init__(self):
    self.board = chess.Board()
    self.plr_color = chess.WHITE

  def try_move(self, start, end):
    if self.piece(start).color != self.plr_color:
      return
    mv = chess.Move(start, end)
    if mv in self.board.legal_moves:
      self.board.push(mv)
      self.plr_color = not self.plr_color # FOR 2-PLR GAMING

  def piece(self, sq):
    return self.board.piece_at(sq)

  def last_move(self):
    if len(self.board.move_stack):
      return self.board.move_stack[-1]

  def get_moves(self, sq):
    return filter(lambda x: x.from_square == sq, self.board.legal_moves)
