from datetime import datetime
import win32clipboard
from copy import deepcopy

import pygame

from sudokusolver.Puzzle import Puzzle
from sudokusolver.Service import Service

C_dark_grey = (50, 50, 50)
C_light_grey = (120, 120, 120)
C_red = (120, 30, 30)

pixels = 800
default_font = "comicsans"

default_puzzle_rank_3 = "1\t\t5\t\t\t\t9\t8\t\r\n" \
                        "\t\t\t3\t\t\t\t1\t\r\n" \
                        "\t7\t6\t\t\t9\t4\t\t\r\n" \
                        "4\t\t1\t6\t9\t3\t\t2\t7\r\n" \
                        "8\t6\t2\t\t1\t5\t\t9\t4\r\n" \
                        "\t\t\t8\t\t\t\t6\t5\r\n" \
                        "\t1\t8\t4\t3\t\t\t\t\r\n" \
                        "7\t\t\t\t\t\t6\t\t\r\n" \
                        "\t\t\t\t7\t1\t\t4\t"

default_puzzle_rank_4 = "\t\t11\t\t\t6\t14\t2\t\t\t3\t\t12\t\t9\t\r\n" \
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
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((pixels, (pixels + 100)))
        self.cell_size = 0
        self.font = None
        self.clock = pygame.time.Clock()
        self.puzzle = Puzzle(rank=3)
        self.stt_time = datetime.now()
        self.local_connection = Service()

        self.refresh_screen_parameters(self.puzzle.rank)
        self.draw()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        self.puzzle = Puzzle(self.get_clipboard())
                        if self.puzzle.invalid:
                            self.puzzle = Puzzle(rank=3)

                        self.refresh_screen_parameters(self.puzzle.rank)

                    elif event.key == pygame.K_3:
                        self.puzzle = Puzzle(default_puzzle_rank_3)
                        self.refresh_screen_parameters(3)

                    elif event.key == pygame.K_4:
                        self.puzzle = Puzzle(default_puzzle_rank_4)
                        self.refresh_screen_parameters(4)

                    elif event.key == pygame.K_s:
                        self.local_connection.send_pulsar_request(deepcopy(self.puzzle), solver='sequential')

                    elif event.key == pygame.K_RETURN:
                        self.local_connection.send_pulsar_request(deepcopy(self.puzzle), solver='SAT')

                    elif event.key == pygame.K_p:
                        self.local_connection.send_pulsar_request(deepcopy(self.puzzle), solver='parallel')

                    elif event.key == pygame.K_r:
                        self.puzzle.reset()

                self.draw()
                pygame.display.update()

            if self.local_connection.response_data:
                self.puzzle.solution = self.local_connection.response_data
                self.local_connection.response_data = None
                self.draw()
                pygame.display.update()

            self.clock.tick(60)

    def refresh_screen_parameters(self, rank=3):
        self.screen.fill((200, 200, 200))
        self.cell_size = pixels / (rank**2)
        self.font = pygame.font.SysFont(default_font, int(self.cell_size * 0.4))

    def draw(self):

        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):

                cell_size_1 = (self.cell_size - 5) if self.is_edge(j, self.puzzle.rank) else (self.cell_size - 1)
                cell_size_2 = (self.cell_size - 5) if self.is_edge(i, self.puzzle.rank) else (self.cell_size - 1)
                cell_stt1 = 4 if j == 0 else (j * self.cell_size)
                cell_stt2 = 4 if i == 0 else (i * self.cell_size)

                if self.puzzle.question[i][j]:
                    value_to_fill = self.puzzle.question[i][j]

                    if self.puzzle.invalid:
                        cell_bg_clr = C_red
                    else:
                        cell_bg_clr = C_dark_grey

                elif len(self.puzzle.solution[i][j]) == 1:
                    value_to_fill = self.puzzle.solution[i][j][0]
                    cell_bg_clr = C_light_grey
                else:
                    value_to_fill = 0
                    cell_bg_clr = C_light_grey

                pygame.draw.rect(self.screen, cell_bg_clr, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
                if value_to_fill > 0:
                    pos_corrector = 0.27 + ((value_to_fill / 10) * 0.03)
                    text1 = self.font.render(str(value_to_fill), 1, (0, 0, 0))
                    self.screen.blit(text1,
                                     (cell_stt1 + cell_size_1 * pos_corrector, cell_stt2 + cell_size_2 * pos_corrector))

        pygame.display.update()

    @staticmethod
    def get_clipboard():
        win32clipboard.OpenClipboard()
        clipboard_text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return clipboard_text

    @staticmethod
    def is_edge(idx, rank=3):
        return ((idx + 1) % rank == 0) | (idx == 0)
