class Solver:
    def __init__(self, grid, actions=[]):
        super().__init__()
        self.state = grid
        self.size = len(grid)
        self.rank = int(self.size**0.5)

        self.state_invalid = False
        self.state_solved = False
        self.invalid_index = (-1, -1)

        self.backtracking_depth_max = 25
        self.backtracking_depth = 0
        self.backtracking_depth_temp = 0
        self.backtracking_step = 5
        self.actions = actions

        # self.ui_obj = ui_obj

    def solve(self):
        if len(self.actions) > 0:
            self.apply_actions(self.actions)

        self.apply_distinctive_iteration()

    def apply_actions(self, actions):
        for action in actions:
            if self.state_invalid:
                break
            else:
                self.setval(action)

    def is_valid(self, action):
        (i, j) = action['idx']
        val = action['val']
        for it in range(self.size):
            if (len(self.state[i][it]) <= 1) and (self.state[i][it][0] == val) and (it != j):
                return False
            if (len(self.state[it][j]) <= 1) and (self.state[it][j][0] == val) and (it != i):
                return False
        it = i//self.rank
        jt = j//self.rank
        for i1 in range(it * self.rank, it * self.rank + self.rank):
            for j1 in range(jt * self.rank, jt * self.rank + self.rank):
                if (len(self.state[i1][j1]) <= 1) and (self.state[i1][j1][0] == val) and (i1 != i) and (j1 != j):
                    return False
        return True

    def setval(self, action):
        (x, y) = action['idx']
        no = action['val']

        if not self.is_valid(action):
            self.state_invalid = True
            if self.invalid_index == (-1, -1):
                self.invalid_index = (x, y)
            return

        self.state[x][y] = [no]
        # if self.ui_obj:
        #     self.ui_obj.draw(self.state)
        #     pygame.event.get()

        relative_cells = self.getrelative_cells(x, y)

        for t in relative_cells:
            (i, j) = t
            if len(self.state[i][j]) > 2:
                if self.state[i][j].count(no) > 0:
                    self.state[i][j].remove(no)
            elif len(self.state[i][j]) == 2:
                if self.state[i][j].count(no) > 0:
                    self.state[i][j].remove(no)
                    self.setval({'idx': (i, j), 'val': self.state[i][j][0]})

        return

    def apply_distinctive_iteration(self):

        itercnt = 0
        restart_iteration = True
        while restart_iteration and (not self.state_invalid):
            itercnt += 1

            restart_iteration = False
            for i in range(self.size):
                for j in range(self.size):
                    if len(self.state[i][j]) > 1:
                        for k in self.state[i][j]:
                            restart_iteration = self.unique_in_relative_cells(k, i, j, self.getrelative_cells(i, j))
                            if restart_iteration:
                                self.setval({'idx': (i, j), 'val': k})
                                # pygame.event.get()
                                break
                    if restart_iteration:
                        break
                if restart_iteration:
                    break

        self.state_solved = True
        for i in range(self.size):
            for j in range(self.size):
                if len(self.state[i][j]) > 1:
                    self.state_solved = False

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

            if (int(x - x % self.rank) <= i <= int(x - x % self.size + self.size - 1) and
                    int(y - y % self.size) <= j <= int(y - y % self.size + self.size - 1)):
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

    def getrelative_cells(self, x, y):

        out = []
        for t in range(self.size):
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

        x1, y1 = x - (x % self.rank), y - (y % self.rank)

        for i in range(x1, x1 + self.rank):
            for j in range(y1, y1 + self.rank):
                if i == x or j == y:
                    pass
                else:
                    temp = (i, j)
                    out.append(temp)

        return out
