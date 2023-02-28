import chess
import pygame
import threading
import resources
from config import TILE_SIZE

BOARD_SIZE = TILE_SIZE * 8
is_playing_white = False

def render_pieces(board, window):
  for sq in range(64):
    p = board.piece_at(sq)
    if p:
      x = sq % 8
      y = sq // 8
      if is_playing_white:
        y = 7 - y
      else:
        x = 7 - x
      window.blit(resources.pieces[p.symbol()], (x * TILE_SIZE, y * TILE_SIZE))

def render_loop(board):
  clock = pygame.time.Clock()

  window = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

  # GAME LOOP
  running = True
  while running:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # RENDER BACKBOARD
    window.blit(resources.board, (0,0))

    # RENDER PIECES
    render_pieces(board, window)

    # RENDER SCREEN
    pygame.display.flip()

  # EXIT WINDOW
  pygame.quit()

def init(b):
  thread = threading.Thread(target=render_loop, args=(b,))
  thread.start()
