import pygame,random,sys
from pygame import *

pygame.init()

# Temporary
cols = 30
rows = 16

tile_size = 30
xbuf = 1
panh = 2
ybuf = 1
br = 3

img0 = pygame.image.load('./Images/zero.png')
img1 = pygame.image.load('./Images/one.png')
img2 = pygame.image.load('./Images/two.png')
img3 = pygame.image.load('./Images/three.png')
img4 = pygame.image.load('./Images/four.png')
img5 = pygame.image.load('./Images/five.png')
img6 = pygame.image.load('./Images/six.png')
img7 = pygame.image.load('./Images/seven.png')
img8 = pygame.image.load('./Images/eight.png')
imgcover= pygame.image.load('./Images/covered.png')
imgflag = pygame.image.load('./Images/flagged.png')
imgques = pygame.image.load('./Images/unknown.png')
imgmine = pygame.image.load('./Images/mine.png')
imgnomine = pygame.image.load('./Images/nomine.png')
imgclickedmine = pygame.image.load('./Images/kaboom.png')


adjacent_states = [img0, img1, img2, img3, img4, img5, img6, img7, img8]
imglist = [img0, img1, img2, img3, img4, img5, img6, img7, img8, imgcover, imgflag, imgques, imgmine, imgnomine, imgclickedmine]

lightgrey = (175, 175, 175)
darkgrey = (100, 100, 100)
white = (255, 255, 255)

screen_width = (2*xbuf + cols) * tile_size + 2*br
screen_height = (panh + 3*ybuf + rows) * tile_size + 4*br
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



#pygame.draw.lines(screen, darkgrey, False, [(xbuf*tile_size, (panh + ybuf)*tile_size), (xbuf*tile_size, ybuf*tile_size), ((screen_width / tile_size - xbuf)*tile_size, ybuf*tile_size)], 6)
#pygame.draw.lines(screen, white, False, [(xbuf*tile_size-1.5, (panh + ybuf)*tile_size), ((screen_width / tile_size - xbuf)*tile_size, (panh + ybuf)*tile_size), ((screen_width / tile_size - xbuf)*tile_size, ybuf*tile_size-1.5)], 6)


def create_button(x, y, index):
    screen.blit(imglist[index], (x, y))

def draw_tiles(numrow, numcol, index):
    for row in range(numrow):
        for col in range(numcol):
            screen.blit(imglist[index], ((xbuf + col)*tile_size + br + 1, (2*ybuf + panh + row)*tile_size + br - 0.5))


def tile_pos(x, y, rows, cols):
    tilec = (x - xstart) // tile_size
    tiler = (y - xstart) // tile_size
    if tilec <= cols and tilec >= 0 and tiler <= rows and tiler >= 0:
        return(tilec, tiler)
    else:
        return(-1, -1)


screen.fill(white)

tile_size = 30
xstart = 4*tile_size
ystart = 4*tile_size

while True:
    
    for ev in pygame.event.get():
        
        if ev.type == pygame.QUIT:
            pygame.quit()
            
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            
            #if the mouse is clicked on the
            # button the game is terminated
            if tile_pos(mouse[0], mouse[1], rows, cols)[0] >= 0:
                print(tile_pos(mouse[0], mouse[1], rows, cols))
                
    # fills the screen with a color
    screen.fill(lightgrey)

    draw_frame3(xbuf*tile_size, ybuf*tile_size, screen_width - 2*xbuf*tile_size, panh*tile_size + br, 3)
    draw_frame3(xbuf*tile_size, (2*ybuf + panh)*tile_size, screen_width - 2*xbuf*tile_size, rows*tile_size + br, 3)
    
    
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
    
    # if mouse is hovered on a button it
    # changes to lighter shade 
   
    # updates the frames of the game

    draw_tiles(rows, cols, 9)
    pygame.display.update()

    # fpsClock.tick(FPS)
