import pygame
import threading
import resources
from renderer import render, flip
from config import TILE_SIZE

BOARD_SIZE = TILE_SIZE * 8
game = None
selected = None

def mouse(e):
  global selected
  pos = pygame.mouse.get_pos()
  x, y = flip(pos[0] // TILE_SIZE, pos[1] // TILE_SIZE, game)
  sq = y * 8 + x
  p = game.piece(sq)
  if p == None or not p.color == game.plr_color:
    if selected is not None:
      game.try_move(selected, sq)
    selected = None
  elif e.type == pygame.MOUSEBUTTONDOWN:
    selected = sq

def render_loop():
  clock = pygame.time.Clock()

  window = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

  # Make Surface type match to avoid doing it each frame, causing high CPU usage.
  resources.board = resources.board.convert()

  # GAME LOOP
  turn = game.board.ply()
  running = True
  while running:
    clock.tick(60)
    update_frame = False
    for e in pygame.event.get():
      # print(pygame.event.event_name(e.type))
      if e.type == pygame.QUIT:
        game.unexpected_end = True
        running = False
        break
      elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
        update_frame = True
        mouse(e)
      elif e.type == pygame.VIDEOEXPOSE:
        update_frame = True
      elif e.type == pygame.MOUSEMOTION:
        if selected is not None and pygame.mouse.get_pressed()[0]:
          update_frame = True

    if turn != game.board.ply():
      turn = game.board.ply()
      update_frame = True

    if update_frame:
      render(window, game, selected)
      # Update window
      pygame.display.flip()

  # EXIT WINDOW
  pygame.quit()

def init(GAME):
  global game
  game = GAME
  thread = threading.Thread(target=render_loop)
  thread.start()
