import pygame
from config import THEME, TILE_SIZE
from os.path import join

PATH = join('assets', THEME)

pygame.init()
font = pygame.font.SysFont("sourcecodepro", TILE_SIZE // 6)

board = pygame.image.load(join(PATH, 'board.png'))

flipped_board = pygame.transform.flip(board, True, False)

coords = {}
coords[True] = pygame.Surface(board.get_size(), pygame.SRCALPHA)
coords[False] = pygame.Surface(board.get_size(), pygame.SRCALPHA)

for i in range(8):
  wn = font.render(str(8 - i), True, (255,255,255))
  wc = font.render(chr(97 + i), True, (255,255,255))
  bn = font.render(str(i + 1), True, (255,255,255))
  bc = font.render(chr(104 - i), True, (255,255,255))
  x, y = wn.get_size()
  offset = (y - x) // 3
  coords[True].blit(wn, (8 * TILE_SIZE - x - offset, i * TILE_SIZE))
  coords[True].blit(wc, (i * TILE_SIZE + offset, 8 * TILE_SIZE - y))
  coords[False].blit(bn, (8 * TILE_SIZE - x - offset, i * TILE_SIZE))
  coords[False].blit(bc, (i * TILE_SIZE + offset, 8 * TILE_SIZE - y))

coords[True].blit(flipped_board, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
coords[False].blit(flipped_board, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

pieces = {}

for c in ['w', 'b']:
  for p in ['K', 'Q', 'B', 'N', 'R', 'P']:
    index = p if c == 'w' else p.lower()
    sprite = pygame.image.load(join(PATH, c + p + '.svg'))
    pieces[index] = pygame.transform.smoothscale(sprite, (TILE_SIZE, TILE_SIZE))
