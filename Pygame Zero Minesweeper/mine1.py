import pygame,random,sys
from pygame import *

pygame.init()

# Temporary
width = 16
height = 16

tile_size = 30
xbuf = 1
panh = 2
ybuf = 1

lightgrey = (175, 175, 175)
darkgrey = (100, 100, 100)
white = (255, 255, 255)

#screen_width = (2*xbuf + width) * tile_size
#screen_height = (panh + 3*ybuf + height) * tile_size
screen_width = 500
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

def draw_frame1(x, y, w, h, b):
    points = [(x, y + h), (x + w, y + h), (x + w, y)]
    pygame.draw.lines(screen, white, False, points, b)

    points = [(x + i, y + h - i), (x + i, y + i), (x + w - i, y + i)]
    pygame.draw.lines(screen, darkgrey, False, points,b)

def draw_frame2(x, y, w, h, b):
    points = [(x, y + h), (x + w, y + h), (x + w, y)]
    pygame.draw.lines(screen, white, False, points, b)

    for i in range(b):
        points = [(x + i, y + h - i + 1), (x + i, y + i), (x + w - i + 1, y + i)]
        pygame.draw.lines(screen, darkgrey, False, points, 1)

def draw_frame3(x, y, w, h, b):
    for i in range(b):
        points = [(x + i, y + h - i), (x + w - i, y + h - i), (x + w - i, y + i)]
        pygame.draw.lines(screen, white, False, points, 1)
        points = [(x + i, y + h - i), (x + i, y + i), (x + w - i, y + i)]
        pygame.draw.lines(screen, darkgrey, False, points, 1)


#pygame.draw.lines(screen, darkgrey, False, [(xbuf*tile_size, (panh + ybuf)*tile_size), (xbuf*tile_size, ybuf*tile_size), ((screen_width / tile_size - xbuf)*tile_size, ybuf*tile_size)], 3)
#pygame.draw.lines(screen, white, False, [(xbuf*tile_size, (panh + ybuf)*tile_size), ((screen_width / tile_size - xbuf)*tile_size, (panh + ybuf)*tile_size), ((screen_width / tile_size - xbuf)*tile_size, ybuf*tile_size)], 3)

screen.fill(lightgrey)

draw_frame3(100, 200, 300, 300, 3)
draw_frame3(100, 100, 300, 50, 3)

#pygame.draw.lines(screen, darkgrey, False, [(xbuf*tile_size, (panh + ybuf)*tile_size), (xbuf*tile_size, ybuf*tile_size), ((screen_width / tile_size - xbuf)*tile_size, ybuf*tile_size)], 6)
#pygame.draw.lines(screen, white, False, [(xbuf*tile_size-1.5, (panh + ybuf)*tile_size), ((screen_width / tile_size - xbuf)*tile_size, (panh + ybuf)*tile_size), ((screen_width / tile_size - xbuf)*tile_size, ybuf*tile_size-1.5)], 6)


pygame.display.update()
