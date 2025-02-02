import threading
import time
import chess
import chess.engine
from config import DIFFICULTY

def analyze_position(game):
  engine = chess.engine.SimpleEngine.popen_uci("./stockfish")

  engine.configure({"Skill Level": 20, "Use NNUE": True, "Threads": 1})
  limit = chess.engine.Limit(depth=99, time=60)

  while not game.unexpected_end:
    turn = game.board.ply()
    with engine.analysis(game.board, limit) as analysis:
      for info in analysis:
        if turn != game.board.ply() or game.unexpected_end:
          break
        if (depth := info.get("depth")) is None or depth < 10:
          continue
        #if (pv := info.get("pv")) is None or len(pv) == 0:
        if not info.get("pv"):
          continue
        game.eval = info
    while turn == game.board.ply() and not game.unexpected_end:
      time.sleep(0.1)

  engine.quit()

def play(game):
  engine = chess.engine.SimpleEngine.popen_uci("./stockfish")

  engine.configure({"Skill Level": DIFFICULTY, "Use NNUE": True, "Threads": 1})
  limit = chess.engine.Limit(time=0.1)

  while not game.unexpected_end:
    if game.board.turn != game.plr_color:
      if game.ended():
        break
      result = engine.play(game.board, limit)
      game.board.push(result.move)

  engine.quit()

def start(game):
  analysis = threading.Thread(target=analyze_position, args=(game,))
  analysis.start()
  if not game.two_plr:
    player = threading.Thread(target=play, args=(game,))
    player.start()
