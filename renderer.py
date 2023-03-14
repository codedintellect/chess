import pygame
import resources
from config import TILE_SIZE, COORDS

BOARD_SIZE = TILE_SIZE * 8
game = None
selected = None

# COLORS (taken with shame directly from lichess :D)
selected_color = (20, 85, 30, 127)
last_move_color = (155, 199, 0, 105)
hover_color = (255, 255, 255, 127)
hint_color = (241, 196, 15, 100)
threat_color = (231, 76, 60, 100)

class renderer:
  def __init__(self, window, game):
    self.window = window
    self.game = game

  def rotate_board(self, x, y):
    return (x, 7-y) if self.game.plr_color else (7-x, y)

  def coords_from_sq(self, sq):
    return pygame.Vector2(self.rotate_board(sq % 8, sq // 8))

  def corner_from_sq(self, sq):
    return self.coords_from_sq(sq) * TILE_SIZE

  def center_from_sq(self, sq):
    return self.corner_from_sq(sq) + pygame.Vector2(TILE_SIZE // 2)

  def rect(self, surface, sq, color, width=0):
    coords = self.corner_from_sq(sq)
    rect = (coords.x, coords.y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(surface, color, rect, width)

  def circle(self, surface, sq, color, radius):
    center = self.center_from_sq(sq)
    pygame.draw.circle(surface, color, center, radius)

  def arrow(self, surface, sq1, sq2, color):
    self.circle(surface, sq1, color, TILE_SIZE // 8)
    self.circle(surface, sq2, color, TILE_SIZE // 8)
    c1 = self.center_from_sq(sq1)
    c2 = self.center_from_sq(sq2)
    pygame.draw.line(surface, color, c1, c2, TILE_SIZE // 8)

  def threat(self, surface, sq):
    self.circle(surface, sq, threat_color, TILE_SIZE // 2.2)

  def render(self, selected):
    # RENDER BACKBOARD
    self.window.blit(resources.board, (0,0))

    # RENDER CELL LABELS
    if COORDS:
      self.window.blit(resources.coords[self.game.plr_color], (0,0))

    highlights = pygame.Surface(resources.board.get_size(), pygame.SRCALPHA)

    # RENDER LAST MOVE
    if lm := self.game.last_move():
      self.rect(highlights, lm.from_square, last_move_color)
      self.rect(highlights, lm.to_square, last_move_color)

    # RENDER SELECTED
    if selected is not None:
      self.rect(highlights, selected, selected_color)
      for mv in self.game.get_moves(selected):
        self.circle(highlights, mv.to_square, selected_color, TILE_SIZE // 7)
      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        x, y = self.rotate_board(pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)
        self.rect(highlights, y * 8 + x, hover_color, TILE_SIZE // 16)

    # RENDER CHECK
    if self.game.board.is_check():
      sq = self.game.board.king(self.game.board.turn)
      self.threat(highlights, sq)

    self.window.blit(highlights, (0,0))

    # RENDER PIECES
    for sq in range(64):
      if p := self.game.piece(sq):
        coords = self.corner_from_sq(sq)
        icon = resources.pieces[p.symbol()]
        if sq == selected and pygame.mouse.get_pressed()[0]:
          icon = icon.copy()
          icon.set_alpha(128)
        self.window.blit(icon, coords)

    # RENDER ENGINE SUGGESTIONS
    layer = pygame.Surface(resources.board.get_size(), pygame.SRCALPHA)
    if (eval := self.game.eval) and (pv := eval.get("pv")) is not None:
      if len(pv) > 0:
        self.arrow(layer, pv[0].from_square, pv[0].to_square, hint_color)
        if len(pv) > 1:
          self.arrow(layer, pv[1].from_square, pv[1].to_square, threat_color)

    self.window.blit(layer, (0,0))

    # RENDER PICKED UP PIECE
    if selected is not None and pygame.mouse.get_pressed()[0]:
      icon = resources.pieces[self.game.piece(selected).symbol()]
      pos = pygame.mouse.get_pos()
      self.window.blit(icon, (pos[0] - TILE_SIZE // 2, pos[1] - TILE_SIZE // 3))
