class Matrix:
    def __init__(self, rank=3):
        self.rank = rank
        self.size = rank**2

        self.grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                col = []
                for k in range(self.size):
                    col.append((k+1))
                row.append(col)
            self.grid.append(row)

    def print(self, grid=None):
        if grid:
            size = len(grid)
        else:
            grid = self.grid
            size = self.size
        print("Printing Grid..")
        fill_count = 0
        for i in range(size):
            row = grid[i]
            row_str = ''
            for x in row:
                if len(x) <= 1:
                    fill_count += 1
                    row_str = row_str + ',' + str(x[0])
                else:
                    row_str = row_str + ',' + '_'
            print(row_str)

        print(f"Elements filled = {fill_count}")
