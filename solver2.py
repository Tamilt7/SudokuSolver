import pygame
import win32clipboard


r = 3
row_pixel = 800
cell_size = row_pixel / (r**2)
grid = []
init_grid = []
tempgrid = [[[1], [], [5], [], [], [], [9], [8], []],
            [[], [], [], [3], [], [], [], [1], []],
            [[], [7], [6], [], [], [9], [4], [], []],
            [[4], [], [1], [6], [9], [3], [], [2], [7]],
            [[8], [6], [2], [], [1], [5], [], [9], [4]],
            [[], [], [], [8], [], [], [], [6], [5]],
            [[], [1], [8], [4], [3], [], [], [], []],
            [[7], [], [], [], [], [], [6], [], []],
            [[], [], [], [], [7], [1], [], [4], []]
            ]

pygame.font.init()
font1 = pygame.font.SysFont("comicsans", int(cell_size * 0.72))

screen = pygame.display.set_mode((row_pixel, (row_pixel + 100)))


def getclipboardgrid():

    global tempgrid

    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    data = data.split("\r\n")
    for i in range(len(data)):
        row = data[i].split("\t")
        row2 = []
        for x in row:
            try:
                row2.append([int(x)])
            except ValueError:
                row2.append([])
        data[i] = row2

    if len(data) <= ((r**2) - 1):
        print("invalid input")
        print(len(data))
        print(len(data[(r**2) - 1]))

    elif len(data[(r**2) - 1]) <= ((r**2) - 1):
        print("invalid input")
        print(len(data))
        print(len(data[(r**2) - 10]))

    else:
        for i in range(r**2):
            for j in range(r**2):
                tempgrid[i][j] = data[i][j]


def initrank15grid():
    global r, tempgrid, cell_size, font1

    r = 15
    cell_size = row_pixel / (r**2)
    font1 = pygame.font.SysFont("comicsans", int(cell_size * 0.72))

    tempgrid = []
    for i in range(r**2):
        row = []
        for j in range(r**2):
            row.append([])
        tempgrid.append(row)

    tempgrid[7][7].append(5)


def initrank5grid():
    global r, tempgrid, cell_size, font1

    r = 5
    cell_size = row_pixel / (r**2)
    font1 = pygame.font.SysFont("comicsans", int(cell_size * 0.72))

    tempgrid = []
    for i in range(r**2):
        row = []
        for j in range(r**2):
            row.append([])
        tempgrid.append(row)


def initrank3grid():
    global r, tempgrid, cell_size, font1

    r = 3
    cell_size = row_pixel / (r**2)
    font1 = pygame.font.SysFont("comicsans", int(cell_size * 0.72))

    tempgrid = []
    for i in range(r**2):
        row = []
        for j in range(r**2):
            row.append([])
        tempgrid.append(row)


def initrank4grid():
    global r, tempgrid, cell_size, font1

    r = 4
    cell_size = row_pixel / (r**2)
    font1 = pygame.font.SysFont("comicsans", int(cell_size * 0.72))

    tempgrid = []
    for i in range(r**2):
        row = []
        for j in range(r**2):
            row.append([])
        tempgrid.append(row)

def solvesudoku():
    global grid

    # for x in range(100):
    grid1 = grid
    distinctive_iteration()
    missing_iteration()
    # if grid == grid1:
    #     break


def modifygrid():
    pass


def distinctive_iteration():

    itercnt = 0
    restart_iteration = True
    while restart_iteration:
        itercnt += 1
        # if itercnt % 100 == 0:
        # print(itercnt)

        restart_iteration = False
        for i in range(r**2):
            for j in range(r**2):
                if len(grid[i][j]) > 1:
                    for k in grid[i][j]:
                        restart_iteration = unique_in_relative_cells(k, i, j, getrelative_cells(i, j))
                        if restart_iteration:
                            setval(k, i, j)
                            break
                if restart_iteration:
                    break
            if restart_iteration:
                break

        # restart_iteration = False


def unique_in_relative_cells(val, x, y, relative_cells):
    relative_row_cells = []
    relative_col_cells = []
    relative_blk_cells = []


    flag1, flag2, flag3 = True, True, True

    for t in relative_cells:
        (i, j) = t

        if i == x:
            relative_row_cells.append(t)

        if j == y:
            relative_col_cells.append(t)

        if int(x - x % r) <= i <= int(x - x % r + r - 1) and int(y - y % r) <= j <= int(y - y % r + r - 1):
            relative_blk_cells.append(t)

    for t in relative_row_cells:
        i, j = t
        if grid[i][j].count(val) > 0:
            flag1 = False

    for t in relative_col_cells:
        i, j = t
        if grid[i][j].count(val) > 0:
            flag2 = False

    for t in relative_blk_cells:
        i, j = t
        if grid[i][j].count(val) > 0:
            flag3 = False

    return flag1 | flag2 | flag3


def missing_iteration():
    pass


def backtracking():
    pass


def setval(no, x, y):
    # print("Setting (" + str(x) + ", " + str(y) + ") from" + str(grid[x][y]) + "to " + str(no))
    grid[x][y] = [no]
    relative_cells = getrelative_cells(x, y)
    # print("Relative Cells ->", relative_cells)

    # if r == 3:
    #     pygame.time.wait(70)
    # elif r < 10:
    #     pygame.time.wait(10)

    draw()
    pygame.display.update()
    pygame.event.get()

    for t in relative_cells:
        (i, j) = t
        if len(grid[i][j]) > 2:
            if grid[i][j].count(no) > 0:
                # print("removing " + str(no) + "from (" + str(i) + ", " + str(j) + ")")
                grid[i][j].remove(no)
        elif len(grid[i][j]) == 2:
            if grid[i][j].count(no) > 0:
                # print("removing " + str(no) + "from (" + str(i) + ", " + str(j) + ")")
                grid[i][j].remove(no)
                setval(grid[i][j][0], i, j)


def getrelative_cells(x, y):
    global r

    out = []
    for t in range(r**2):
        if t == x:
            pass
        else:
            temp = (t, y)
            out.append(temp)
        if t == y:
            pass
        else:
            temp = (x, t)
            out.append(temp)

    x1, y1 = x - (x % r), y - (y % r)

    for i in range(x1, x1 + r):
        for j in range(y1, y1+r):
            if i == x or j == y:
                pass
            else:
                temp = (i, j)
                out.append(temp)

    return out


def loadgrid():
    global grid, init_grid

    init_grid = []
    for i in range(r**2):
        row = []
        for j in range(r**2):
            col = []
            for k in range(r**2):
                col.append((k+1))
            row.append(col)
        init_grid.append(row)

    grid = init_grid[:]

    for i in range(r**2):
        for j in range(r**2):
            if len(tempgrid[i][j]) > 0:
                setval(tempgrid[i][j][0], i, j)


def draw():
    global row_pixel, cell_size, grid

    cell_bg_clr1 = (50, 50, 50)
    cell_bg_clr2 = (120, 120, 120)
    for i in range(r**2):
        for j in range(r**2):

            if (j + 1) % r == 0:
                cell_size_1 = (cell_size - 5)
            else:
                cell_size_1 = (cell_size - 1)

            if (i + 1) % r == 0:
                cell_size_2 = (cell_size - 5)
            else:
                cell_size_2 = (cell_size - 1)

            if j == 0:
                cell_stt1 = 4
                cell_size_1 -= 4
            else:
                cell_stt1 = j * cell_size

            if i == 0:
                cell_stt2 = 4
                cell_size_2 -= 4
            else:
                cell_stt2 = i * cell_size

            if tempgrid[i][j]:
                pygame.draw.rect(screen, cell_bg_clr1, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
                if len(tempgrid[i][j]) == 1:
                    if tempgrid[i][j][0] > 9:
                        text1 = font1.render(str(tempgrid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.27, cell_stt2 + cell_size_2 * 0.27))
                    else:
                        text1 = font1.render(str(tempgrid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.3, cell_stt2 + cell_size_2 * 0.3))
            else:
                pygame.draw.rect(screen, cell_bg_clr2, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
                if grid and len(grid[i][j]) == 1:
                    if grid[i][j][0] > 9:
                        text1 = font1.render(str(grid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.27, cell_stt2 + cell_size_2 * 0.27))
                    else:
                        text1 = font1.render(str(grid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.3, cell_stt2 + cell_size_2 * 0.3))


screen.fill((200, 200, 200))
draw()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                grid = []
                getclipboardgrid()
                draw()
            elif event.key == pygame.K_4:
                grid = []
                screen.fill((200, 200, 200))
                initrank4grid()
                draw()
            elif event.key == pygame.K_5:
                grid = []
                screen.fill((200, 200, 200))
                initrank5grid()
                draw()
            elif event.key == pygame.K_3:
                grid = []
                screen.fill((200, 200, 200))
                initrank3grid()
                draw()
            elif event.key == pygame.K_0:
                grid = []
                screen.fill((200, 200, 200))
                initrank15grid()
                draw()
            elif event.key == pygame.K_RETURN:
                print("Enter pressed..")
                loadgrid()
                print(grid)
                solvesudoku()
                print(grid)
                print("Solved!")
            elif event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                print("Refresh started..")
                grid = []
                screen.fill((200, 200, 200))
                draw()
                pygame.display.update()
                print("Refresh Done")

    # if grid:
        draw()

    pygame.display.update()

pygame.quit()
