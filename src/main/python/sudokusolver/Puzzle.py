class Puzzle:
    def __init__(self, from_str=None, rank=3):

        self.invalid = False

        if from_str:
            data = from_str.split("\r\n")
            data = [x for x in data if len(x) > 0]
            if ' ' in data[0]:
                sep = ' '
            elif '\t' in data[0]:
                sep = '\t'
            else:
                sep = ''
            for i in range(len(data)):
                row = data[i].split(sep)
                row2 = []
                for x in row:
                    try:
                        row2.append(int(x))
                    except ValueError:
                        row2.append(None)
                data[i] = row2
        else:
            data = [[None for _ in range(rank**2)] for _ in range(rank**2)]

        self.size = len(data)
        self.rank = int(self.size**0.5)
        self.solution = [[[z for z in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

        if len(data) != len(data[self.size - 1]):
            print("Invalid Clipboard data!")
            self.invalid = True
        elif self.size not in [9, 16, 25, 36]:
            print("Unsupported Puzzle size!")
            self.invalid = True
        else:
            self.question = data
            if not self.puzzle_valid():
                self.invalid = True
                print(f"invalid puzzle!")

    def puzzle_valid(self):

        for row in self.question:
            row = [x for x in row if x is not None]
            if len(row) != len(set(row)):
                return False

        seen = [{-1} for _ in range(self.size)]  # Create a set for each column

        for row in self.question:
            for col_index, value in enumerate(row):
                if value in seen[col_index]:
                    return False  # Duplicate found in column
                if value:
                    seen[col_index].add(value)

        for i in range(0, self.size, self.rank):
            for j in range(0, self.size, self.rank):
                sub_grid = set()  # Create a set for each subgrid
                for x in range(i, i + self.rank):
                    for y in range(j, j + self.rank):
                        value = self.question[x][y]
                        if value in sub_grid:
                            return False  # Duplicate found in subgrid
                        if value:
                            sub_grid.add(value)

        return True

    def reset(self):
        self.solution = [[[z for z in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
