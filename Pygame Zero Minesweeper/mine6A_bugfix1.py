# Your Code Goes Here
# To run, open Python’s IDLE Shell and open your existing document, or create a new one
# Version 6A_bugfix1

import pygame,random,sys, os
from pygame import *

import tkinter as tk
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import PhotoImage


init_x = 600
init_y = 150
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (init_x,init_y)
pygame.init()

game_map = []
checked = []
mines = [[-1, -1]]
started = False
FPS = 120
fpsClock = pygame.time.Clock()
frame = 0

tile_size = 30
xbuf = 1
panh = 2
ybuf = 1
br = 3

rows = 0
cols = 0
minec = 0

lightgrey = (175, 175, 175)
darkgrey = (100, 100, 100)
white = (255, 255, 255)


screen = pygame.display.set_mode((100, 100), pygame.HIDDEN)
pygame.display.set_caption("Minesweeper")

# Tile Number Meanings
# 0 to 8 - Uncovered, mines adjacent
# 9 - Mine
# 10 - Clicked Mine
# 11 - Flagged
# 12 - Question mark
# 99 - Uncovered tile


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
imgs = [img0, img1, img2, img3, img4, img5, img6, img7, img8, imgmine, imgclickedmine, imgflag, imgques]

soundstart=pygame.mixer.Sound("./Audio/start.mp3")
soundclick=pygame.mixer.Sound("./Audio/click.mp3")
soundexplode = pygame.mixer.Sound("./Audio/explosion.mp3")
soundclear = pygame.mixer.Sound("./Audio/win.mp3")
soundwin = pygame.mixer.Sound("./Audio/victory.mp3")
soundlose = pygame.mixer.Sound("./Audio/gameover.mp3")
soundflag = pygame.mixer.Sound("./Audio/flag.mp3")

soundexplode.set_volume(0.5)

# Creating a map with desired rows and columns:
def create_map(rows, cols):
    global game_map, checked
    game_map = []
    checked = []

    for i in range(rows):
        row = []
        checkrow = []
        for j in range(cols):
            row.append(99)
            checkrow.append(False)

        game_map.append(row)
        checked.append(checkrow)

# Placing mines
def place_mines(num, fc, fr):
    global mines
    mines = []
    pos = [fr, fc]
    for i in range(num):
        while pos == [fr, fc] or mines.count(pos) > 0:
            pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        mines.append(pos)

# Find the number of mines adjacent to the tile
def find_mines(r,c):
    m=0
    if [r,c] in mines:
        return 9
    else:
        if [r-1,c] in mines:
            m += 1
        if [r+1,c] in mines:
            m += 1
        if [r,c-1] in mines:
            m += 1
        if [r,c+1] in mines:
            m+= 1
        if [r-1,c-1] in mines:
            m += 1
        if [r+1,c+1] in mines:
            m += 1
        if [r+1,c-1] in mines:
             m += 1
        if [r-1,c+1] in mines:
            m += 1

        return m

# Uncovers all tiles adjacent to an uncovered tile that has 0 mines adjacent
def uncover_adj(r,c):
    if r>=0 and r<rows and c>=0 and c<cols:
        game_map[r][c]=find_mines(r,c)
        if game_map[r][c]==0 and not checked[r][c]:
             checked[r][c] = True
             uncover_adj(r-1,c)
             uncover_adj(r+1,c)
             uncover_adj(r,c-1)
             uncover_adj(r,c+1)
             uncover_adj(r-1,c-1)
             uncover_adj(r+1,c+1)
             uncover_adj(r-1,c+1)
             uncover_adj(r+1,c-1)
        else:
            return 0
    else:
        return 0

# Drawing the tiles
def draw_tiles():
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] != 99:
                screen.blit(imgs[game_map[row][col]], ((col + xbuf)*tile_size + br, (row + 2*ybuf + panh)*tile_size + br))
            else:
                screen.blit(imgcover, ((col + xbuf)*tile_size + br, (row + 2*ybuf + panh)*tile_size + br))

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
    soundstart.play()
    create_map(row, col)

def main(r,c,m):
    global rows, cols, minec, started
    rows, cols, minec = r, c, m

    init_game(cols, rows)

    screen_width = (2*xbuf + cols) * tile_size + 2*br
    screen_height = (panh + 3*ybuf + rows) * tile_size + 4*br
    screen = pygame.display.set_mode((screen_width, screen_height))
    root.withdraw()


    while True:
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            #checks if a mouse is clicked and find the tile
            if ev.type == pygame.MOUSEBUTTONDOWN:
                c = find_pos(mouse[0] - xbuf*tile_size + br, mouse[1] - (2*ybuf + panh)*tile_size + br, rows, cols)[0]
                r = find_pos(mouse[0] - xbuf*tile_size + br, mouse[1] - (2*ybuf + panh)*tile_size + br, rows, cols)[1]

                if c >= 0 and c < cols and r >= 0 and r < rows:
                    if pygame.mouse.get_pressed()[0] and game_map[r][c] != 11:
                        if started == False:
                            started = True
                            place_mines(minec, c, r)

                        if game_map[r][c] == 99 or game_map[r][c] == 12:
                            if [r,c] not in mines:
                                soundclick.play()
                            else:
                                soundexplode.play()
                        uncover_adj(r, c)

                if pygame.mouse.get_pressed()[2] and c >= 0 and c < cols and r >= 0 and r < rows:
                    soundflag.play()
                    if game_map[r][c] == 99:
                        game_map[r][c] = 11
                    elif game_map[r][c] == 11:
                        game_map[r][c] = 12
                    elif game_map[r][c] == 12:
                        game_map[r][c] = 99

        # fills the screen with grey
        screen.fill(lightgrey)

        draw_frame(xbuf*tile_size, ybuf*tile_size, screen_width - 2*xbuf*tile_size, panh*tile_size + br, 3)
        draw_frame(xbuf*tile_size, (2*ybuf + panh)*tile_size, screen_width - 2*xbuf*tile_size, rows*tile_size + br, 3)

        draw_tiles()
        pygame.display.update()

        #fpsClock.tick(FPS)

root = tk.Tk()
root.title("Options (WIP)")
root.geometry('800x300+600+200')

l_title = tk.Label(root, text="Please set the number of rows, columns and mines:",font=("Courier", 14, 'bold'),fg='blue' )
l_title.place(x=30,y=50)

l_row = tk.Label(root, text="Rows: ",font=("Courier", 13, 'bold'),fg='green' )
l_row.place(x=80,y=140)

rows = tk.StringVar()
t_rows = tk.Entry(root,textvariable=rows, bg='lightgrey', width=8)
t_rows.place(x=150,y=145)

l_col = tk.Label(root, text="Cols: ",font=("Courier", 13, 'bold'),fg='green' )
l_col.place(x=280,y=140)

cols = tk.StringVar()
t_cols = tk.Entry(root,textvariable=cols, bg='lightgrey', width=8)
t_cols.place(x=350,y=145)

l_mine = tk.Label(root, text="Mines: ",font=("Courier", 13, 'bold'),fg='green' )
l_mine.place(x=480,y=140)

mines = tk.StringVar()
t_mines = tk.Entry(root,textvariable=mines, bg='lightgrey', width=8)
t_mines.place(x=550,y=145)

b_set = tk.Button(root, text="Set",width=12,height=1,font=("Courier", 14, 'bold'),fg='red',command=lambda:main(int(rows.get()),int(cols.get()),int(mines.get())))
b_set.place(x=280,y=210)


root.mainloop()
