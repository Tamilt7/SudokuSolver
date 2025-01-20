import pygame
from itertools import product
import win32clipboard
from copy import deepcopy


backtracking_depth_max = 25
backtracking_depth = 0
backtracking_step = 5
backtracking_depth_temp = 0
r = 3
row_pixel = 800
cell_size = row_pixel / (r**2)
font_size = int(cell_size * 0.4)
problem_grid = [[[] for y in range(r*r)] for x in range(r*r)]
problem_grid_invalid_idx = (-1, -1)
grid = []
default_problem_text = "1\t\t5\t\t\t\t9\t8\t\r\n" \
               "\t\t\t3\t\t\t\t1\t\r\n" \
               "\t7\t6\t\t\t9\t4\t\t\r\n" \
               "4\t\t1\t6\t9\t3\t\t2\t7\r\n" \
               "8\t6\t2\t\t1\t5\t\t9\t4\r\n" \
               "\t\t\t8\t\t\t\t6\t5\r\n" \
               "\t1\t8\t4\t3\t\t\t\t\r\n" \
               "7\t\t\t\t\t\t6\t\t\r\n" \
               "\t\t\t\t7\t1\t\t4\t\r\n"

pygame.font.init()
font1 = pygame.font.SysFont("comicsans", font_size)
screen = pygame.display.set_mode((row_pixel, (row_pixel + 100)))


def getclipboardgrid():

    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    updateproblem_grid(data)


def updateproblem_grid(question_str):
    global problem_grid, problem_grid_invalid_idx, grid

    data = question_str
    problem_grid_invalid_idx = (-1, -1)

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
        problem_grid = [[[] for y in range(r*r)] for x in range(r*r)]
        for i in range(r**2):
            for j in range(r**2):
                problem_grid[i][j] = data[i][j]

    actions = get_actions_from_problem_grid()
    obj = SudokuSolver(deepcopy(grid), actions, do_not_solve=True)
    if obj.state_invalid:
        print(f"invalid Input at index {obj.invalid_index}!")
        problem_grid_invalid_idx = obj.invalid_index
    del obj


def initgrid(n):
    global grid, r, problem_grid, cell_size, font1

    screen.fill((200, 200, 200))

    if r != n:
        r = n
        problem_grid = [[[] for _ in range(r*r)] for _ in range(r*r)]
        cell_size = row_pixel / (r**2)
        font1 = pygame.font.SysFont("comicsans", int(cell_size * 0.4))

    grid = []
    for i in range(r**2):
        row = []
        for j in range(r**2):
            col = []
            for k in range(r**2):
                col.append((k+1))
            row.append(col)
        grid.append(row)


def get_actions_from_problem_grid():
    actions = []
    for i in range(r**2):
        for j in range(r**2):
            if len(problem_grid[i][j]) > 0:
                action = {'idx': (i, j), 'val': problem_grid[i][j][0]}
                actions.append(action)
    return actions


class SudokuSolver:
    def __init__(self, state, actions, do_not_solve=False):
        self.state = state
        self.actions = actions
        self.state_invalid = False
        self.state_solved = False
        self.do_not_solve = do_not_solve
        self.invalid_index = (-1, -1)

        self.apply_actions()
        self.solve_state()

    def apply_actions(self):
        for x in self.actions:
            (i, j) = x['idx']
            val = x['val']
            self.setval(val, i, j)
            if self.state_invalid:
                break

    def solve_state(self):
        self.distinctive_iteration()
        self.state_solved = True
        for i in range(r*r):
            for j in range(r*r):
                if len(self.state[i][j]) > 1:
                    self.state_solved = False

    def distinctive_iteration(self):

        itercnt = 0
        restart_iteration = True
        while restart_iteration and (not self.state_invalid):
            itercnt += 1

            restart_iteration = False
            for i in range(r**2):
                for j in range(r**2):
                    if len(self.state[i][j]) > 1:
                        for k in self.state[i][j]:
                            restart_iteration = self.unique_in_relative_cells(k, i, j, self.getrelative_cells(i, j))
                            if restart_iteration:
                                self.setval(k, i, j)
                                break
                    if restart_iteration:
                        break
                if restart_iteration:
                    break

            # restart_iteration = False

    def unique_in_relative_cells(self, val, x, y, relative_cells):
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
            if self.state[i][j].count(val) > 0:
                flag1 = False

        for t in relative_col_cells:
            i, j = t
            if self.state[i][j].count(val) > 0:
                flag2 = False

        for t in relative_blk_cells:
            i, j = t
            if self.state[i][j].count(val) > 0:
                flag3 = False

        return flag1 | flag2 | flag3

    def setval(self, no, x, y):
        if self.state_invalid:
            return

        if not self.valid(self.state, x, y, no):
            self.state_invalid = True
            if self.invalid_index == (-1, -1):
                self.invalid_index = (x, y)
            return

        self.state[x][y] = [no]
        draw(self.state)
        pygame.display.update()
        pygame.event.get()

        relative_cells = self.getrelative_cells(x, y)

        for t in relative_cells:
            (i, j) = t
            if len(self.state[i][j]) > 2:
                if self.state[i][j].count(no) > 0:
                    self.state[i][j].remove(no)
            elif len(self.state[i][j]) == 2:
                if self.state[i][j].count(no) > 0:
                    self.state[i][j].remove(no)
                    self.setval(self.state[i][j][0], i, j)

        return

    @staticmethod
    def valid(m, i, j, val):
        for it in range(r**2):
            if (len(m[i][it]) <= 1) and (m[i][it][0] == val) and (it != j):
                return False
            if (len(m[it][j]) <= 1) and (m[it][j][0] == val) and (it != i):
                return False
        it = i//r
        jt = j//r
        for i1 in range(it * r, it * r + r):
            for j1 in range(jt * r, jt * r + r):
                if (len(m[i1][j1]) <= 1) and (m[i1][j1][0] == val) and (i1 != i) and (j1 != j):
                    return False
        return True

    @staticmethod
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


def get_backtracking_elements(state):
    elements = []
    for size in range(2, (r**2 + 1)):
        for i in range(r**2):
            for j in range(r**2):
                if (len(state[i][j]) > 1) and (len(state[i][j]) <= size):
                    elements.append({'idx': (i, j), 'vals': state[i][j]})
                    if len(elements) >= backtracking_step:
                        return elements

    return elements


def solvesudoku():
    global grid
    actions = get_actions_from_problem_grid()
    obj1 = SudokuSolver(deepcopy(grid), actions)

    if obj1.state_invalid:
        print(f"Problem solving puzzle at index {obj1.invalid_index}!")
        return
    else:
        grid = obj1.state

    del obj1

    printgrid()

    apply_backtracking(deepcopy(grid))

    printgrid()
    print("Done!")


def apply_backtracking(tempgrid):
    global grid, backtracking_depth, backtracking_depth_temp

    backtracking_depth += 1
    if backtracking_depth > backtracking_depth_temp:
        backtracking_depth_temp = backtracking_depth
        print(f"At depth {backtracking_depth}")
        printgrid(deepcopy(tempgrid))

    iter_elements = get_backtracking_elements(tempgrid)
    iter_element_indices = [x['idx'] for x in iter_elements]
    iter_val_combinations = list(product(*[x['vals'] for x in iter_elements]))

    iterations = []
    for combo in iter_val_combinations:
        actions = []
        for idx, val in zip(iter_element_indices, combo):
            actions.append({'idx': idx, 'val': val})
        iterations.append(actions)

    for actions in iterations:
        obj = SudokuSolver(deepcopy(tempgrid), actions)
        if not obj.state_invalid:
            if (not obj.state_solved) and (backtracking_depth < backtracking_depth_max):
                apply_backtracking(deepcopy(obj.state))

        if obj.state_solved and (not obj.state_invalid):
            grid = obj.state
            del obj
            return
        del obj


def printgrid(temp=None):
    if not temp:
        temp = deepcopy(grid)
    print("Printing Grid..")
    fill_count = 0
    for i in range(r*r):
        row = temp[i]
        row_str = ''
        for x in row:
            if len(x) <= 1:
                fill_count += 1
                row_str = row_str + ',' + str(x[0])
            else:
                row_str = row_str + ',' + '_'
        print(row_str)

    print(f"Elements filled = {fill_count}")


def draw(print_grid=None):
    global row_pixel, cell_size

    if not print_grid:
        print_grid = deepcopy(grid)

    cell_bg_clr1 = (50, 50, 50)
    cell_bg_clr2 = (120, 120, 120)
    cell_bg_clr3 = (120, 30, 30)
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

            if problem_grid[i][j]:
                if (i, j) == problem_grid_invalid_idx:
                    pygame.draw.rect(screen, cell_bg_clr3, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
                else:
                    pygame.draw.rect(screen, cell_bg_clr1, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))

                if len(problem_grid[i][j]) == 1:
                    if problem_grid[i][j][0] > 9:
                        text1 = font1.render(str(problem_grid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.27, cell_stt2 + cell_size_2 * 0.27))
                    else:
                        text1 = font1.render(str(problem_grid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.3, cell_stt2 + cell_size_2 * 0.3))
            else:
                pygame.draw.rect(screen, cell_bg_clr2, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
                if print_grid and len(print_grid[i][j]) == 1:
                    if print_grid[i][j][0] > 9:
                        text1 = font1.render(str(print_grid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.27, cell_stt2 + cell_size_2 * 0.27))
                    else:
                        text1 = font1.render(str(print_grid[i][j][0]), 1, (0, 0, 0))
                        screen.blit(text1, (cell_stt1 + cell_size_1 * 0.3, cell_stt2 + cell_size_2 * 0.3))


screen.fill((200, 200, 200))
initgrid(3)
updateproblem_grid(default_problem_text)
# initgrid(3)
draw()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                getclipboardgrid()
            elif event.key == pygame.K_4:
                initgrid(4)
            elif event.key == pygame.K_5:
                initgrid(5)
            elif event.key == pygame.K_3:
                initgrid(3)
            # elif event.key == pygame.K_0:
            #     initgrid(15)
            elif event.key == pygame.K_RETURN:
                solvesudoku()
            elif event.key == pygame.K_r:  # and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                print("Refresh started..")
                initgrid(r)
                print("Refresh Done")

        # if grid:
        draw()
        pygame.display.update()

pygame.quit()

