import pygame
import threading
import resources
from config import TILE_SIZE

BOARD_SIZE = TILE_SIZE * 8
game = None
selected = None

def player_flip(x, y):
  if game.plr_color: # TRUE == WHITE
    return x, 7 - y
  else:
    return 7 - x, y

def render_pieces(window):
  for sq in range(64):
    p = game.piece(sq)
    if p:
      x, y = player_flip(sq % 8, sq // 8)
      window.blit(resources.pieces[p.symbol()], (x * TILE_SIZE, y * TILE_SIZE))

def mouse(e):
  global selected
  pos = pygame.mouse.get_pos()
  x, y = player_flip(pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)
  sq = y * 8 + x
  p = game.piece(sq)
  if p == None or not p.color == game.plr_color:
    if selected:
      game.try_move(selected, sq)
    selected = None
  elif e.type == pygame.MOUSEBUTTONDOWN:
    selected = sq

def render_loop():
  clock = pygame.time.Clock()

  window = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

  # GAME LOOP
  running = True
  while running:
    clock.tick(60)
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        running = False
      elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
        mouse(e)

    # RENDER BACKBOARD
    window.blit(resources.board, (0,0))

    # RENDER PIECES
    render_pieces(window)

    # RENDER CELL LABELS
    if True: # TODO: ADD CONFIG
      if game.plr_color:
        window.blit(resources.for_white, (0,0))
      else:
        window.blit(resources.for_black, (0,0))

    # RENDER SCREEN
    pygame.display.flip()

  # EXIT WINDOW
  pygame.quit()

def init(GAME):
  global game
  game = GAME
  thread = threading.Thread(target=render_loop)
  thread.start()
