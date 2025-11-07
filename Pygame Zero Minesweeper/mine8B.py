# Version 8B
# D6415 Interactive Software
# Open source and copyright free

import pygame,random,sys, os
from pygame import *

import tkinter as tk
from tkinter import *

# Initialise stuff

init_x = 600
init_y = 150
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (init_x,init_y)
pygame.init()

# Define variables

game_map = []
checked = []
mines = [[-1, -1]]
minecount = 0
tme = 0
started = False
playing = False
FPS = 20
fpsClock = pygame.time.Clock()
frame = 0
state = ""

tile_size = 30
xbuf = 1
panh = 2.5
ybuf = 1
br = 3

rows = 0
cols = 0
minec = 0

# Styling
lightgrey = (175, 175, 175)
darkgrey = (100, 100, 100)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
darkgreen = (0, 125, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
magenta = (255, 0, 255)

screen_width = 100
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height), pygame.HIDDEN)
pygame.display.set_caption("Minesweeper")

# Tile Number Meanings
# 0 to 8 - Uncovered, mines adjacent
# 9 - Mine
# 10 - Clicked Mine
# 11 - Flagged
# 12 - Question mark
# 13 - No mine
# 14 - Revealed mine for victory
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
imghiddenmine = pygame.image.load('./Images/hiddenmine.png')
imgs = [img0, img1, img2, img3, img4, img5, img6, img7, img8, imgmine, imgclickedmine, imgflag, imgques, imgnomine, imghiddenmine]

imgd0 = pygame.image.load("./Images/digit0.png")
imgd1 = pygame.image.load("./Images/digit1.png")
imgd2 = pygame.image.load("./Images/digit2.png")
imgd3 = pygame.image.load("./Images/digit3.png")
imgd4 = pygame.image.load("./Images/digit4.png")
imgd5 = pygame.image.load("./Images/digit5.png")
imgd6 = pygame.image.load("./Images/digit6.png")
imgd7 = pygame.image.load("./Images/digit7.png")
imgd8 = pygame.image.load("./Images/digit8.png")
imgd9 = pygame.image.load("./Images/digit9.png")
imgdb = pygame.image.load("./Images/digitblank.png")
imgdd = pygame.image.load("./Images/digitdash.png")
digits = [imgd0, imgd1, imgd2, imgd3, imgd4, imgd5, imgd6, imgd7, imgd8, imgd9, imgdd, imgdb]

smiley = pygame.image.load("./Images/smiley.png")
smileyclick = pygame.image.load("./Images/smileyclick.png")
smileywin = pygame.image.load("./Images/smileywin.png")
smileylose = pygame.image.load("./Images/smileylose.png")
smileys = [smiley, smileyclick, smileywin, smileylose]

soundstart=pygame.mixer.Sound("./Audio/start.mp3")
soundclick=pygame.mixer.Sound("./Audio/click.mp3")
soundexplode = pygame.mixer.Sound("./Audio/explosion.mp3")
soundclear = pygame.mixer.Sound("./Audio/win.mp3")
soundwin = pygame.mixer.Sound("./Audio/victory.mp3")
soundlose = pygame.mixer.Sound("./Audio/gameover.mp3")
soundflag = pygame.mixer.Sound("./Audio/flag.mp3")
soundnomine = pygame.mixer.Sound("./Audio/nomine.mp3")

soundexplode.set_volume(0.5)
soundnomine.set_volume(1.5)
soundstart.set_volume(2)

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
def place_mines(fc, fr):
    global mines, minec
    mines = []
    pos = [fr, fc]

    for i in range(minec):
        while pos == [fr, fc] or mines.count(pos) > 0:
            pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        mines.append(pos)

    count = 0
    while find_mines(fr, fc) != 0 and minec <= rows*cols - 9 and count <= 350:
        mines = []
        pos = [fr, fc]
        for i in range(minec):
            while pos == [fr, fc] or mines.count(pos) > 0:
                pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
            mines.append(pos)
        count += 1

# Find the number of mines adjacent to the tile
def find_mines(r,c):
    m=0
    if [r,c] in mines:
        return 9
    else:
        for i in range(3):
            for j in range(3):
                if [r-1+i, c-1+j] in mines and not (i == 1 and j == 1):
                    m += 1
        return m

# Uncovers all tiles adjacent to an uncovered tile that has 0 mines adjacent
def uncover_adj(r,c):
    if r<0 or r>=rows or c<0 or c>=cols:
        return 0

    game_map[r][c]=find_mines(r,c)
    if (game_map[r][c]!=0 and game_map[r][c]!=11) or checked[r][c]:
        return 0

    checked[r][c] = True
    for i in range(3):
        for j in range(3):
            if not (i == 1 and j == 1):
                uncover_adj(r-1+i, c-1+j)

# Drawing the tiles
def draw_tiles():
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] != 99:
                screen.blit(imgs[game_map[row][col]], ((col + xbuf)*tile_size + br + 1, (row + 2*ybuf + panh)*tile_size + br + 1))
            else:
                screen.blit(imgcover, ((col + xbuf)*tile_size + br + 1, (row + 2*ybuf + panh)*tile_size + br + 1))

# Find the position of the mouse click
def find_pos(x, y, rows, cols):
    tilec = (x - xbuf) // tile_size
    tiler = (y - (2*ybuf + panh)) // tile_size
    if tilec <= cols and tilec >= 0 and tiler <= rows and tiler >= 0:
        return(tilec, tiler)
    else:
        return(-1, -1)

# Draws a frame
def draw_frame(x, y, w, h, b):
    for i in range(b):
        points = [(x + i, y + h - i), (x + w - i, y + h - i), (x + w - i, y + i)]
        pygame.draw.lines(screen, white, False, points, 1)

        points = [(x + i, y + h - i), (x + i, y + i), (x + w - i, y + i)]
        pygame.draw.lines(screen, darkgrey, False, points, 1)

# Placing the digits
def place_digits(num, x, y):
    if num >= 0:
        if num > 999:
            num = 999
        i=num // 100
        screen.blit(digits[i],(x,y))
        i=(num%100) // 10
        screen.blit(digits[i],(x+28,y))
        i=(num%100)%10
        screen.blit(digits[i],(x+56,y))
    else:
        if num < -99:
            num = -99
        screen.blit(digits[10],(x,y))
        i= -num // 10
        screen.blit(digits[i],(x+28,y))
        i= -num % 10
        screen.blit(digits[i],(x+56,y))

# Define showing a text
def show_text(content,size,color,position):
    if "pressstart2p" in pygame.font.get_fonts():
        font=pygame.font.SysFont("pressstart2p",size)
        text_surface=font.render(content,True,color)
        screen.blit(text_surface,position)
        print("font found")
    else:
        font=pygame.font.SysFont("lucidasanstypewriter",int(2*size))
        text_surface=font.render(content,True,color)
        screen.blit(text_surface,position)

# Showing the mines after loss
def show_mines(r, c):
    global playing, game_map, state
    state = "lost"
    playing = False
    incorrect = False
    soundexplode.play()
    soundnomine.stop()
    game_map[r][c] = 10
    draw_map()
    screen.blit(smileys[3], (screen_width/2 - 30, (ybuf+panh/2)*tile_size+br-30))
    pygame.display.flip()
    pygame.time.wait(750)
    for mine in mines:
        if mine != [r, c] and game_map[mine[0]][mine[1]] != 11:
            game_map[mine[0]][mine[1]] = 9
            draw_map()
            soundexplode.play()
            pygame.display.flip()
            pygame.time.wait(50)

    pygame.time.wait(500)

# Showing incorrectly placed flags
def show_incorrect():
    pygame.time.wait(1500)
    soundexplode.stop()
    soundnomine.play()
    pygame.time.wait(200)
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] == 11 and [row, col] not in mines:
                game_map[row][col] = 13
                draw_map()
                pygame.display.flip()
                pygame.time.wait(10)
    pygame.time.wait(500)

# Reveals mines after won
def reveal_mines():
    global playing, game_map, state
    state = "won"
    playing = False
    soundclear.play()
    for mine in mines:
        game_map[mine[0]][mine[1]] = 14
        draw_map()
        pygame.display.flip()
        pygame.time.wait(50)
    pygame.time.wait(300)

# Drawing the map
def draw_map():
    # fills the screen with grey
    screen.fill(lightgrey)

    # Draws smileys
    if state == "playing":
        screen.blit(smileys[0], (screen_width/2 - 30, (ybuf+panh/2)*tile_size+br-30))
    elif state == "won":
        screen.blit(smileys[2], (screen_width/2 - 30, (ybuf+panh/2)*tile_size+br-30))
    elif state == "lost":
        screen.blit(smileys[3], (screen_width/2 - 30, (ybuf+panh/2)*tile_size+br-30))

    draw_frame(xbuf*tile_size, ybuf*tile_size, cols*tile_size + 2*br, panh*tile_size + 2*br, 3)
    draw_frame(xbuf*tile_size, (2*ybuf + panh)*tile_size, cols*tile_size + 2*br, rows*tile_size + 2*br, 3)

    draw_tiles()
    place_digits(minecount, (xbuf+0.25)*tile_size+br, (ybuf+panh/2)*tile_size+br-25)
    place_digits(tme, (xbuf+cols-3)*tile_size+br, (ybuf+panh/2)*tile_size+br-25)

    if cols <= 10:
        size = 10
    elif cols <= 20:
        size = cols
    else:
        size = 20

    if playing and not started:
        msg='O - OPTIONS'
        x = (cols / 2 + xbuf)*tile_size - size * 5
        y = (rows + 2.6*ybuf + panh)*tile_size
        show_text(msg,size,black,(x, y))

# Game over text
def game_over(won, waittime):
    pygame.time.wait(waittime)
    if cols <= 10:
        size = 9
    elif cols <= 20:
        size = int(cols * 0.85)
    else:
        size = 17

    if won:
        msg='YOU WIN. R - RESTART, Q - QUIT'
        x = (cols + 2*xbuf - size)*tile_size / 2
        y = (rows + 2.6*ybuf + panh)*tile_size
        show_text(msg,size,darkgreen,(x, y))
        soundwin.play(-1)
    else:
        msg='GAME OVER. R - RESTART, Q - QUIT'
        x = (cols + 2*xbuf - size)*tile_size / 2 - 10
        y = (rows + 2.6*ybuf + panh)*tile_size
        show_text(msg,size,red,(x, y))
        soundlose.play()
    pygame.display.flip()

# Initialise the game
def init_game(col, row):
    global playing, started, tme, frame, state, minec
    playing = True
    started = False
    tme = 0
    frame = 0
    state = "playing"
    soundstart.play()
    create_map(row, col)

    if minec >= rows*cols:
        minec = rows*cols - 1

def main(r,c,m):
    global rows, cols, minec, started, frame, game_map, playing, screen_width, screen_height, tme, minecount
    rows, cols, minec = int(r), int(c), int(m)

    init_game(cols, rows)

    screen_width = (2*xbuf + cols) * tile_size + 2*br
    screen_height = (panh + 3.3*ybuf + rows) * tile_size + 4*br
    screen = pygame.display.set_mode((screen_width, screen_height))
    root.withdraw()

    # Main gameplay loop
    while True:
        mouse = pygame.mouse.get_pos()

        if playing:
            draw_map()
            screen.blit(smileys[0], (screen_width/2 - 30, (ybuf+panh/2)*tile_size+br-30))

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            #checks if a mouse is clicked and find the tile
            if ev.type == pygame.MOUSEBUTTONDOWN and playing == True:
                c = int(find_pos(mouse[0] - xbuf*tile_size + br, mouse[1] - (2*ybuf + panh)*tile_size + br, rows, cols)[0])
                r = int(find_pos(mouse[0] - xbuf*tile_size + br, mouse[1] - (2*ybuf + panh)*tile_size + br, rows, cols)[1])
                if c >= 0 and c < cols and r >= 0 and r < rows:
                    if pygame.mouse.get_pressed()[0] and game_map[r][c] != 11:
                        screen.blit(smileys[1], (screen_width/2 - 30, (ybuf+panh/2)*tile_size+br-30))
                        if started == False:
                            started = True
                            place_mines(c, r)

                        if game_map[r][c] == 99 or game_map[r][c] == 12:
                            if [r,c] not in mines:
                                soundclick.play()
                                uncover_adj(r, c)
                            else:
                                incorrect = False
                                show_mines(r, c)
                                for row in range(rows):
                                    for col in range(cols):
                                        if game_map[row][col] == 11 and [row, col] not in mines:
                                            incorrect = True
                                        pygame.time.wait(2)

                                if incorrect:
                                    show_incorrect()
                                game_over(False, 1000)

                if pygame.mouse.get_pressed()[0] and mouse[0] >= screen_width/2 - 30 and mouse[0] <= screen_width/2 + 30 and mouse[1] >= (ybuf+panh/2)*tile_size+br-30 and mouse[1] <= (ybuf+panh/2)*tile_size+br + 30:
                    init_game(cols, rows)

                if pygame.mouse.get_pressed()[2] and c >= 0 and c < cols and r >= 0 and r < rows:
                    soundflag.play()
                    if game_map[r][c] == 99:
                        game_map[r][c] = 11
                    elif game_map[r][c] == 11:
                        game_map[r][c] = 12
                    elif game_map[r][c] == 12:
                        game_map[r][c] = 99

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q and not playing:
                    pygame.quit()

                if ev.key == pygame.K_r and not playing:
                    soundwin.stop()
                    init_game(cols, rows)

                if ev.key == pygame.K_o:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HIDDEN)
                    soundwin.stop()
                    root.deiconify()

                    return 0

        if started and playing:
            won = True
            for row in range(rows):
                for col in range(cols):
                    if (game_map[row][col] == 99 or game_map[row][col] == 11 or game_map[row][col] == 12) and [row, col] not in mines:
                        won = False

            if won:
                reveal_mines()
                game_over(True, 1000)


        if started and playing:
            frame += 1
        tme = frame // FPS

        minecount = minec - sum(row.count(11) for row in game_map)

        if playing:
            pygame.display.update()

        fpsClock.tick(FPS)

# Game UI made with Tkinter
root = tk.Tk()

px = int(root.winfo_screenwidth()/2 - 400)   # Places the GUI at the center of the screen
py = int(root.winfo_screenheight()/2 - 250)

root.title("Options")
root.geometry(f"800x500+{px}+{py}")
root.configure(bg='black')

l_title = tk.Label(root, text="OPTIONS",font=("Press Start 2P", 50, 'bold'),fg='white', bg = 'black')
l_title.place(x=165,y=50)

l_row = tk.Label(root, text="ROWS:",font=("Press Start 2P", 25, 'bold'),fg='white', bg = 'black')
l_row.place(x=100,y=200)

_rows = tk.StringVar()
t_rows = tk.Entry(root,textvariable=_rows, bg='lightgrey', width=10)
t_rows.place(x=280,y=210)

l_col = tk.Label(root, text="COLS:",font=("Press Start 2P", 25, 'bold'),fg='white', bg = 'black')
l_col.place(x=440,y=200)

_cols = tk.StringVar()
t_cols = tk.Entry(root,textvariable=_cols, bg='lightgrey', width=10)
t_cols.place(x=620,y=210)

l_mine = tk.Label(root, text="MINES:",font=("Press Start 2P", 25, 'bold'),fg='white', bg = 'black')
l_mine.place(x=100,y=300)

_mines = tk.StringVar()
t_mines = tk.Entry(root,textvariable=_mines, bg='lightgrey', width=10)
t_mines.place(x=300,y=310)

l_creator = tk.Label(root, text="CREATED BY RAFSAN KABIR, JASON LI AND THANESH MOHANARAJAH",font=("Press Start 2P", 9),fg='white', bg = 'black')
l_creator.place(x=40,y=400)

l_watermark = tk.Label(root, text="D6415 INTERACTIVE SOFTWARE",font=("Press Start 2P", 20, 'bold'),fg='white', bg = 'black')
l_watermark.place(x=30,y=450)

b_set = tk.Button(root, text="START",width=8,height=1,font=("Press Start 2P", 20, 'bold'),fg='red',command=lambda:main(_rows.get(),_cols.get(),_mines.get()))
b_set.place(x=450,y=290)

root.mainloop()
