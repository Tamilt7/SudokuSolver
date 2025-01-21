import win32clipboard

from sudokusolver.solver_4.Matrix import Matrix
from sudokusolver.solver_4.Puzzle import Puzzle

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
                   "\t4\t\t10\t\t14\t\t\t9\t7\t8\t\t\t15\t\t\r\n"


class Sudoku:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sudoku, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'matrix'):
            self.puzzle = Puzzle(default_puzzle)
            self.matrix = Matrix(self.puzzle.rank)

        print("Done!")

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

    def reset(self):
        self.matrix = Matrix(self.puzzle.rank)
