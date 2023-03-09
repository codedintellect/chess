import pygame
import resources
from config import TILE_SIZE

BOARD_SIZE = TILE_SIZE * 8
game = None
selected = None

# COLORS (taken with shame directly from lichess :D)
selected_color = (20, 85, 30, 127)
last_move_color = (155, 199, 0, 105)
hover_color = (255, 255, 255, 127)

def flip(x, y, game):
  if game.plr_color: # TRUE == WHITE
    return x, 7 - y
  else:
    return 7 - x, y

def render_pieces(window, game, selected):
  for sq in range(64):
    p = game.piece(sq)
    if p:
      x, y = flip(sq % 8, sq // 8, game)
      icon = resources.pieces[p.symbol()]
      if sq == selected and pygame.mouse.get_pressed()[0]:
        icon = icon.copy()
        icon.set_alpha(128)
      window.blit(icon, (x * TILE_SIZE, y * TILE_SIZE))
  if selected is not None and pygame.mouse.get_pressed()[0]:
    icon = resources.pieces[game.piece(selected).symbol()]
    x, y = pygame.mouse.get_pos()
    window.blit(icon, (x - TILE_SIZE // 2, y - TILE_SIZE // 3))

def highlight_rect(surface, sq, color, game, width=0):
  x, y = flip(sq % 8, sq // 8, game)
  rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
  pygame.draw.rect(surface, color, rect, width)

def highlight_circle(surface, sq, color, game):
  x, y = flip(sq % 8, sq // 8, game)
  center = ((x + 0.5) * TILE_SIZE, (y + 0.5) * TILE_SIZE)
  pygame.draw.circle(surface, color, center, TILE_SIZE // 7) # Why 7? No idea...

def render(window, game, selected):
  # RENDER BACKBOARD
  window.blit(resources.board, (0,0))

  highlights = pygame.Surface(resources.board.get_size(), pygame.SRCALPHA)

  # RENDER LAST MOVE
  lm = game.last_move()
  if lm:
    highlight_rect(highlights, lm.from_square, last_move_color, game)
    highlight_rect(highlights, lm.to_square, last_move_color, game)

  # RENDER SELECTED
  if selected:
    highlight_rect(highlights, selected, selected_color, game)
    for mv in game.get_moves(selected):
      highlight_circle(highlights, mv.to_square, selected_color, game)
    if pygame.mouse.get_pressed()[0]:
      pos = pygame.mouse.get_pos()
      x, y = flip(pos[0] // TILE_SIZE, pos[1] // TILE_SIZE, game)
      highlight_rect(highlights, y * 8 + x, hover_color, game, TILE_SIZE // 16)

  window.blit(highlights, (0,0))

  # RENDER CELL LABELS
  if True: # TODO: ADD CONFIG
    if game.plr_color:
      window.blit(resources.for_white, (0,0))
    else:
      window.blit(resources.for_black, (0,0))

  # RENDER PIECES
  render_pieces(window, game, selected)
