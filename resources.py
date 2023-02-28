import pygame
from config import THEME, TILE_SIZE
from os.path import join

PATH = join('assets', THEME)

board = pygame.image.load(join(PATH, 'board.png'))
pieces = {}

for c in ['w', 'b']:
  for p in ['K', 'Q', 'B', 'N', 'R', 'P']:
    index = p if c == 'w' else p.lower()
    sprite = pygame.image.load(join(PATH, c + p + '.svg'))
    pieces[index] = pygame.transform.smoothscale(sprite, (TILE_SIZE, TILE_SIZE))
