# Your Code Goes Here
# To run, open Python’s IDLE Shell and open your existing document, or create a new one

import pygame,random,sys
from pygame import *

pygame.init()
game_map = []
mines = [[-1, -1]]
started = False
fpsClock = pygame.time.Clock()
frame = 0
FPS = 120

# Temporary
cols = 30
rows = 16
minec = 99

tile_size = 30
xbuf = 1
panh = 2
ybuf = 1
br = 3

lightgrey = (175, 175, 175)
darkgrey = (100, 100, 100)
white = (255, 255, 255)

screen_width = (2*xbuf + cols) * tile_size + 2*br
screen_height = (panh + 3*ybuf + rows) * tile_size + 4*br
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

# Tile Number Meanings
# 0 - Covered
# 1 - Uncovered
# 2 - Uncovered with mine
# 3 - Covered with flag
# 4 - Covered with question mark


# Importing sounds and images.
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
adjacent = [img0, img1, img2, img3, img4, img5, img6, img7, img8, imgmine]

startsfx=pygame.mixer.Sound("./Audio/tone1.mp3")
clicksfx=pygame.mixer.Sound("./Audio/tone2.mp3")
explodesfx = pygame.mixer.Sound("./Audio/explosion.mp3")
clearsfx = pygame.mixer.Sound("./Audio/win.mp3")
winsfx = pygame.mixer.Sound("./Audio/victory.mp3")
losesfx = pygame.mixer.Sound("./Audio/gameover.mp3")
flagsfx = pygame.mixer.Sound("./Audio/flag.mp3")

explodesfx.set_volume(0.5)

# Creating a map with desired rows and columns:
def create_map(rows, cols):
    global game_map
    game_map = []

    for row in range(rows):
        row = []
        for j in range(cols):
            row.append(0)
        game_map.append(row) 

# Placing mines
def place_mines(num, fc, fr):
    global mines
    mines = []
    pos = [fc, fr]
    for i in range(num):
        while pos == [fc, fr] or mines.count(pos) > 0:
            pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        mines.append(pos)

# Find the number of mines adjacent to the tile
def find_mines(x, y):
    count = 0
    if mines.count([x, y]) > 0:
        return 9
	
    if y != 0:
        if x != 0:
            if mines.count([x - 1, y - 1]) > 0:
                count += 1
        if x != len(game_map[0]):
            if mines.count([x + 1, y - 1]) > 0:
                count += 1
        if mines.count([x, y - 1]) > 0:
            count += 1
    if y != len(game_map):
        if x != 0:
            if mines.count([x - 1, y + 1]) > 0:
                count += 1
        if x != len(game_map[0]):
            if mines.count([x + 1, y + 1]) > 0:
                count += 1
        if mines.count([x, y + 1]) > 0:
            count += 1
    if x != 0:
        if mines.count([x - 1, y]) > 0:
            count += 1
    if x != game_map[0]:
        if mines.count([x + 1, y]) > 0:
            count += 1

    return count

# Uncovers all tiles adjacent to an uncovered tile that has 0 mines adjacent
def uncover_all_adj():
    global game_map
    rown = 0
    coln = 0
    for rown in range(rows):
        for coln in range(cols):
            row = rown - 1
            col = coln - 1
            if game_map[row][col] == 1 and find_mines(col, row) == 0:
                #print(col, row)
                if row != 0:
                    if col != 0:
                        game_map[row - 1][col - 1] = 1
                    if col != len(game_map[0]):
                        game_map[row - 1][col + 1] = 1
                    game_map[row - 1][col] = 1
                if row != rows:
                    if col != 0:
                        game_map[row + 1][col - 1] = 1
                    if col != cols:
                        game_map[row + 1][col + 1] = 1
                    game_map[row + 1][col] = 1
                if col != 0:
                    game_map[row][col - 1] = 1
                if col != cols:
                    game_map[row][col + 1] = 1
                game_map[row][col]
                #fpsClock.tick(FPS*5)

# Drawing the tiles
def draw_tiles():
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] == 0:
                screen.blit(imgcover, ((col + xbuf)*tile_size + br, (row + 2*ybuf + panh)*tile_size + br))
            elif game_map[row][col] == 1:
                minesadj = find_mines(col, row)
                screen.blit(adjacent[minesadj], ((col + xbuf)*tile_size + br, (row + 2*ybuf + panh)*tile_size + br))
            elif game_map[row][col] == 2:
                screen.blit(imgmine, ((col + xbuf)*tile_size + br, (row + 2*ybuf + panh)*tile_size + br))

def find_pos(x, y, rows, cols):
    tilec = (x - xbuf) // tile_size
    tiler = (y - (2*ybuf + panh)) // tile_size
    if tilec <= cols and tilec >= 0 and tiler <= rows and tiler >= 0:
        return(tilec, tiler)
    else:
        return(-1, -1)

def draw_frame(x, y, w, h, b):
    for i in range(b):
        points = [(x + i, y + h - i), (x + w - i, y + h - i), (x + w - i, y + i)]
        pygame.draw.lines(screen, white, False, points, 1)

        points = [(x + i, y + h - i), (x + i, y + i), (x + w - i, y + i)]
        pygame.draw.lines(screen, darkgrey, False, points, 1)


            

def init_game(col, row):
    startsfx.play()
    create_map(row, col)

 
init_game(cols, rows)

while True:
    mouse = pygame.mouse.get_pos()
    
    for ev in pygame.event.get():
        
        if ev.type == pygame.QUIT:
            pygame.quit()
            
        #checks if a mouse is clicked and find the tile
        if ev.type == pygame.MOUSEBUTTONDOWN:
            c = find_pos(mouse[0] - xbuf*tile_size + br, mouse[1] - (2*ybuf + panh)*tile_size + br, rows, cols)[0]
            r = find_pos(mouse[0] - xbuf*tile_size + br, mouse[1] - (2*ybuf + panh)*tile_size + br, rows, cols)[1]
            if c >= 0 and c < cols and r >= 0 and r < rows and mines.count([c, r]) == 0:
                clicksfx.play()
                game_map[r][c] = 1
                uncover_all_adj()
                uncover_all_adj()
            elif mines.count([c, r]) > 0:
                game_map[r][c] = 2
                explodesfx.play()
                #break

            if started == False:
                started = True
                place_mines(minec, c, r)
                print(mines)

    
    
                
    # fills the screen with a color
    screen.fill(lightgrey)

    draw_frame(xbuf*tile_size, ybuf*tile_size, screen_width - 2*xbuf*tile_size, panh*tile_size + br, 3)
    draw_frame(xbuf*tile_size, (2*ybuf + panh)*tile_size, screen_width - 2*xbuf*tile_size, rows*tile_size + br, 3)
    
    draw_tiles()

    frame += 1
    pygame.display.update()

    #fpsClock.tick(FPS)
