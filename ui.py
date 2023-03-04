import pygame
import threading
import resources
from config import TILE_SIZE

BOARD_SIZE = TILE_SIZE * 8
game = None
selected = None

# COLORS (taken with shame directly from lichess :D)
selected_color = (20, 85, 30, 127)
last_move_color = (155, 199, 0, 105)

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
      icon = resources.pieces[p.symbol()]
      if sq == selected and pygame.mouse.get_pressed()[0]:
        transparent = icon.copy()
        transparent.set_alpha(128)
        window.blit(transparent, (x * TILE_SIZE, y * TILE_SIZE))
        x, y = pygame.mouse.get_pos()
        window.blit(icon, (x - TILE_SIZE // 2, y - TILE_SIZE // 3))
      else:
        window.blit(icon, (x * TILE_SIZE, y * TILE_SIZE))


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

def highlight_square(surface, sq, color):
  x, y = player_flip(sq % 8, sq // 8)
  rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
  pygame.draw.rect(surface, color, rect)

def highlight_circle(surface, sq, color):
  x, y = player_flip(sq % 8, sq // 8)
  center = ((x + 0.5) * TILE_SIZE, (y + 0.5) * TILE_SIZE)
  pygame.draw.circle(surface, color, center, TILE_SIZE // 7) # Why 7? No idea...


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

    highlights = pygame.Surface(resources.board.get_size(), pygame.SRCALPHA)

    # RENDER SELECTED
    if selected:
      highlight_square(highlights, selected, selected_color)
      for mv in game.get_moves(selected):
        highlight_circle(highlights, mv.to_square, selected_color)

    # RENDER LAST MOVE
    lm = game.last_move()
    if lm:
      highlight_square(highlights, lm.from_square, last_move_color)
      highlight_square(highlights, lm.to_square, last_move_color)

    window.blit(highlights, (0,0))

    # RENDER CELL LABELS
    if True: # TODO: ADD CONFIG
      if game.plr_color:
        window.blit(resources.for_white, (0,0))
      else:
        window.blit(resources.for_black, (0,0))

    # RENDER PIECES
    render_pieces(window)

    # RENDER SCREEN
    pygame.display.flip()

  # EXIT WINDOW
  pygame.quit()

def init(GAME):
  global game
  game = GAME
  thread = threading.Thread(target=render_loop)
  thread.start()
