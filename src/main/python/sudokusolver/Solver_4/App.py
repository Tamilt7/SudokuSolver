import pygame
import win32clipboard
from itertools import product
from copy import deepcopy
from datetime import datetime

from sudokusolver.Solver_4.Matrix import Matrix
from sudokusolver.Solver_4.Puzzle import Puzzle
from sudokusolver.Solver_4.Solver import Solver


backtracking_depth_max = 30
backtracking_step = 5
backtracking_iter_cap = 10000

C_dark_grey = (50, 50, 50)
C_light_grey = (120, 120, 120)
C_red = (120, 30, 30)

default_puzzle = "1\t\t5\t\t\t\t9\t8\t\r\n" \
                 "\t\t\t3\t\t\t\t1\t\r\n" \
                 "\t7\t6\t\t\t9\t4\t\t\r\n" \
                 "4\t\t1\t6\t9\t3\t\t2\t7\r\n" \
                 "8\t6\t2\t\t1\t5\t\t9\t4\r\n" \
                 "\t\t\t8\t\t\t\t6\t5\r\n" \
                 "\t1\t8\t4\t3\t\t\t\t\r\n" \
                 "7\t\t\t\t\t\t6\t\t\r\n" \
                 "\t\t\t\t7\t1\t\t4\t"

default_puzzle_2 = "\t\t11\t\t\t6\t14\t2\t\t\t3\t\t12\t\t9\t\r\n" \
                   "10\t7\t\t\t12\t\t\t3\t\t\t\t\t16\t1\t\t2\r\n" \
                   "\t\t\t\t\t10\t\t\t12\t\t\t\t\t\t\t\r\n" \
                   "\t\t3\t15\t\t\t9\t5\t16\t\t\t6\t\t\t13\t14\r\n" \
                   "13\t\t2\t5\t8\t9\t\t16\t\t\t\t\t6\t\t7\t\r\n" \
                   "\t\t\t\t\t\t5\t14\t\t\t4\t\t\t\t11\t1\r\n" \
                   "\t\t12\t\t7\t15\t\t10\t14\t16\t\t\t\t\t\t\r\n" \
                   "4\t9\t\t3\t\t\t1\t13\t\t15\t7\t\t\t\t\t\r\n" \
                   "\t\t\t\t\t3\t15\t\t13\t12\t\t\t4\t\t1\t8\r\n" \
                   "\t\t\t\t\t\t6\t9\t2\t\t14\t8\t\t3\t\t\r\n" \
                   "3\t13\t\t\t\t8\t\t\t1\t9\t\t\t\t\t\t\r\n" \
                   "\t10\t\t2\t\t\t\t\t11\t\t16\t5\t15\t6\t\t12\r\n" \
                   "11\t6\t\t\t3\t\t\t7\t4\t2\t\t\t1\t8\t\t\r\n" \
                   "\t\t\t\t\t\t\t6\t\t\t1\t\t\t\t\t\r\n" \
                   "2\t\t7\t8\t\t\t\t\t3\t\t\t13\t\t\t4\t10\r\n" \
                   "\t4\t\t10\t\t14\t\t\t9\t7\t8\t\t\t15\t\t\r\n" \


class App:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'matrix'):
            pygame.font.init()

            self.row_pixel = 800
            self.cell_size = 0
            self.font1 = None
            self.screen = pygame.display.set_mode((self.row_pixel, (self.row_pixel + 100)))

            self.puzzle = Puzzle(default_puzzle)
            self.matrix = Matrix(self.puzzle.rank)

            self.refresh_screen_parameters()

            self.backtracking_depth = 0
            self.backtracking_depth_temp = 0
            self.backtracking_iter_count = 0
            self.curr_branch = ""
            self.cache_failed_branches = {}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        self.update_puzzle(self.get_clipboard())
                    elif event.key == pygame.K_4:
                        self.update_puzzle(default_puzzle_2)
                    elif event.key == pygame.K_RETURN:
                        time = datetime.now()
                        self.backtracking_iter_count = 0
                        self.solve_puzzle()
                        print(f"Total Backtracking Iterations: {self.backtracking_iter_count}")
                        self.backtracking_iter_count = 0
                        print(f"Duration: {datetime.now() - time}")
                    elif event.key == pygame.K_r:
                        self.reset()
                self.draw(self.matrix.grid)

    def solve_puzzle(self):
        actions = self.get_actions_from_puzzle(self.puzzle)
        solver = Solver(deepcopy(self.matrix.grid), actions)

        if solver.state_invalid:
            print(f"Problem solving puzzle at index {solver.invalid_index}!")
            return
        else:
            self.matrix.grid = solver.state

        self.draw()

        if not solver.state_solved:
            del solver
            self.apply_backtracking(deepcopy(self.matrix.grid))

        print("Done!")

    @staticmethod
    def get_actions_from_puzzle(puzzle):
        actions = []
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                if puzzle.grid[i][j]:
                    action = {'idx': (i, j), 'val': puzzle.grid[i][j]}
                    actions.append(action)
        return actions

    def get_backtracking_elements(self, grid):
        elements = []
        for size in range(2, (self.matrix.size + 1)):
            for i in range(self.matrix.size):
                for j in range(self.matrix.size):
                    if (len(grid[i][j]) > 1) and (len(grid[i][j]) <= size):
                        elements.append({'idx': (i, j), 'vals': grid[i][j]})
                        if len(elements) >= backtracking_step:
                            return elements

        return elements

    def apply_backtracking(self, tempgrid):

        self.backtracking_depth += 1
        if self.backtracking_depth > self.backtracking_depth_temp:
            self.cache_failed_branches[str(self.backtracking_depth)] = []
            self.backtracking_depth_temp = self.backtracking_depth
            # print(f"At depth {self.backtracking_depth}")
            # Matrix(3).print(tempgrid)

        iter_elements = self.get_backtracking_elements(tempgrid)
        iter_element_indices = [x['idx'] for x in iter_elements]
        iter_val_combinations = list(product(*[x['vals'] for x in iter_elements]))

        iterations = []
        for combo in iter_val_combinations:
            actions = []
            for idx, val in zip(iter_element_indices, combo):
                actions.append({'idx': idx, 'val': val})
            iterations.append(actions)

        for actions in iterations:
            self.curr_branch = self.curr_branch + self.simplify(actions)
            if (self.curr_branch in set(self.cache_failed_branches[str(self.backtracking_depth)])) or (self.backtracking_iter_count > backtracking_iter_cap):
                self.curr_branch = self.curr_branch[:(-13 * backtracking_step)]
            else:
                self.backtracking_iter_count = self.backtracking_iter_count + 1
                solver = Solver(deepcopy(tempgrid), actions)
                if solver.state_invalid:
                    self.cache_failed_branches[str(self.backtracking_depth)].append(self.curr_branch)
                    self.curr_branch = self.curr_branch[:(-13 * backtracking_step)]
                else:
                    if not solver.state_solved:
                        self.apply_backtracking(deepcopy(solver.state))
                        self.draw(solver.state)
                    else:
                        self.matrix.grid = solver.state
                        self.draw(self.matrix.grid)
                        # with open("output.json", "w") as json_file:
                        #     json.dump(self.cache_failed_branches, json_file, indent=4)
                        return
                del solver

        self.backtracking_depth -= 1
        self.curr_branch = self.curr_branch[:(-13 * backtracking_step)]

    @staticmethod
    def simplify(actions):
        out = ""
        for x in actions:
            out = out + str(1000 + x['idx'][0]) + str(1000 + x['idx'][1]) + str(1000 + x['val']) + ':'

        return out

    def refresh_screen_parameters(self):
        self.screen.fill((200, 200, 200))
        self.cell_size = self.row_pixel / self.puzzle.size
        self.font1 = pygame.font.SysFont("comicsans", int(self.cell_size * 0.4))

    def is_edge(self, idx):
        return ((idx + 1) % self.puzzle.rank == 0) | (idx == 0)

    def draw(self, grid=None):

        if not grid:
            grid = self.matrix.grid

        for i in range(self.matrix.size):
            for j in range(self.matrix.size):

                cell_size_1 = (self.cell_size - 5) if self.is_edge(j) else (self.cell_size - 1)
                cell_size_2 = (self.cell_size - 5) if self.is_edge(i) else (self.cell_size - 1)
                cell_stt1 = 4 if j == 0 else (j * self.cell_size)
                cell_stt2 = 4 if i == 0 else (i * self.cell_size)

                if self.puzzle.grid[i][j]:
                    value_to_fill = self.puzzle.grid[i][j]

                    if self.puzzle.invalid:
                        cell_bg_clr = C_red
                    else:
                        cell_bg_clr = C_dark_grey

                elif len(grid[i][j]) == 1:
                    value_to_fill = grid[i][j][0]
                    cell_bg_clr = C_light_grey
                else:
                    value_to_fill = 0
                    cell_bg_clr = C_light_grey

                pygame.draw.rect(self.screen, cell_bg_clr, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
                if value_to_fill > 0:
                    pos_corrector = 0.27 + ((value_to_fill / 10) * 0.03)
                    text1 = self.font1.render(str(value_to_fill), 1, (0, 0, 0))
                    self.screen.blit(text1, (cell_stt1 + cell_size_1 * pos_corrector, cell_stt2 + cell_size_2 * pos_corrector))

        while pygame.event.get():
            pass

        pygame.display.update()

    @staticmethod
    def get_clipboard():
        win32clipboard.OpenClipboard()
        clipboard_text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return clipboard_text

    def update_puzzle(self, clipboard_text):
        self.puzzle = Puzzle(clipboard_text)
        if self.puzzle.invalid:
            self.puzzle = Puzzle(default_puzzle)

        self.reset()
        self.refresh_screen_parameters()

    def reset(self):
        self.matrix = Matrix(self.puzzle.rank)
        self.backtracking_depth = 0
        self.backtracking_depth_temp = 0
        self.backtracking_iter_count = 0


App().run()
