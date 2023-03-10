import threading
import time
import chess
import chess.engine

def analyze_position(game):
  engine = chess.engine.SimpleEngine.popen_uci("./stockfish")

  engine.configure({"Skill Level": 20, "Use NNUE": True, "Threads": 1})
  limit = chess.engine.Limit(depth=99, time=60)

  while not game.board.is_game_over() and not game.unexpected_end:
    turn = game.board.ply()
    result = None
    with engine.analysis(game.board, limit) as analysis:
      for info in analysis:
        if turn != game.board.ply() or game.unexpected_end:
          break
        result = info
        if (depth := info.get("depth")) is None or depth < 10:
          continue
        if (pv := info.get("pv")) is None or len(pv) < 2:
          break
        bm = pv[0]
        bt = pv[1]
        score = info.get("score").pov(game.plr_color)
        print()
        print("ANALYSIS:")
        print(f" SCORE: {score}")
        print(f" BEST MOVE: {bm}")
        print(f" THREAT: {bt}")
        print("\r\033[F\033[F\033[F\033[F\033[F\033[F")
    while turn == game.board.ply() and not game.unexpected_end:
      time.sleep(0.1)

  engine.quit()

def start(game):
  thread = threading.Thread(target=analyze_position, args=(game,))
  thread.start()
