from multiprocessing import Process, Queue, Event
from copy import deepcopy
from itertools import product
import pygame
from datetime import datetime

from sudokusolver.solver_5.Sudoku import Sudoku, default_puzzle_2
from sudokusolver.solver_5.Solver import Solver

backtracking_depth_cap = 10
backtracking_step = 5
worker_process_cap = 5

C_dark_grey = (50, 50, 50)
C_light_grey = (120, 120, 120)
C_red = (120, 30, 30)

pixels = 800
screen = None
cell_size = pixels / 9
font = None


def get_backtracking_elements(grid):
    elements = []
    grid_size = len(grid)
    for size in range(2, (grid_size + 1)):
        for i in range(grid_size):
            for j in range(grid_size):
                if (len(grid[i][j]) > 1) and (len(grid[i][j]) <= size):
                    elements.append({'idx': (i, j), 'vals': grid[i][j]})
                    if len(elements) >= backtracking_step:
                        return elements
    return elements


def get_next_set_of_actions(tempgrid):
    elements = get_backtracking_elements(tempgrid)

    iter_element_indices = [x['idx'] for x in elements]
    iter_val_combinations = list(product(*[x['vals'] for x in elements]))

    actions_list = []
    for combo in iter_val_combinations:
        actions = []
        for idx, val in zip(iter_element_indices, combo):
            actions.append({'idx': idx, 'val': val})
        actions_list.append(actions)

    return actions_list


def worker_process(process_id, process_depth, process_count, queue, completion_event, grid, actions):
    if completion_event.is_set() or (process_count >= worker_process_cap):
        return

    if process_count % 20 == 0:
        print(f"{process_count}th Process {process_id} at level {process_depth} started.")

    solver = Solver(deepcopy(grid), actions)
    solver.solve()

    if solver.state_invalid:
        del solver
        return

    if solver.state_solved:
        queue.put((process_id, "Solution Found", solver.state))
        print(f"Process {process_id} found a solution!")
        completion_event.set()
        del solver
        return

    if process_depth < backtracking_depth_cap:
        child_processes = []
        next_actions_list = get_next_set_of_actions(solver.state)
        next_actions_list = next_actions_list[:worker_process_cap - process_count - len(next_actions_list)]

        for idx, next_actions in enumerate(next_actions_list):
            child_id = f"{str(process_id)}.{str(process_depth + 1)}_C{str(idx + 1)}"
            new_process_count = process_count + 1
            p = Process(target=worker_process,
                        args=(child_id,
                              process_depth + 1,
                              new_process_count,  # pass the updated process count
                              queue,
                              completion_event,
                              deepcopy(solver.state),
                              next_actions)
                        )
            p.start()
            child_processes.append(p)

        del solver
        for p in child_processes:
            p.join()


def refresh_screen_parameters(rank):
    global cell_size, font
    screen.fill((200, 200, 200))
    cell_size = pixels / (rank**2)
    font = pygame.font.SysFont("comicsans", int(cell_size * 0.4))


def get_actions_from_puzzle(puzzle):
    actions = []
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            if puzzle.grid[i][j]:
                action = {'idx': (i, j), 'val': puzzle.grid[i][j]}
                actions.append(action)
    return actions


def solve_puzzle(puzzle, matrix):
    result_queue = Queue()
    completion_event = Event()

    actions = get_actions_from_puzzle(puzzle)

    parent_process = Process(target=worker_process,
                             args=("1_P1", 1, 1, result_queue, completion_event, deepcopy(matrix.grid), actions))
    parent_process.start()

    while not completion_event.is_set() and parent_process.is_alive():
        try:
            result = result_queue.get(timeout=1)  # Non-blocking check
            print(f"Main process received result: {result}")
            matrix.grid = result[2]
        except result_queue.Empty:  # Use queue.Empty for a more specific exception
            pass  # Timeout expired, keep checking

    parent_process.join()


def is_edge(idx, rank=3):
    return ((idx + 1) % rank == 0) | (idx == 0)


def draw(puzzle, matrix):

    for i in range(matrix.size):
        for j in range(matrix.size):

            cell_size_1 = (cell_size - 5) if is_edge(j, matrix.rank) else (cell_size - 1)
            cell_size_2 = (cell_size - 5) if is_edge(i, matrix.rank) else (cell_size - 1)
            cell_stt1 = 4 if j == 0 else (j * cell_size)
            cell_stt2 = 4 if i == 0 else (i * cell_size)

            if puzzle.grid[i][j]:
                value_to_fill = puzzle.grid[i][j]

                if puzzle.invalid:
                    cell_bg_clr = C_red
                else:
                    cell_bg_clr = C_dark_grey

            elif len(matrix.grid[i][j]) == 1:
                value_to_fill = matrix.grid[i][j][0]
                cell_bg_clr = C_light_grey
            else:
                value_to_fill = 0
                cell_bg_clr = C_light_grey

            pygame.draw.rect(screen, cell_bg_clr, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))
            if value_to_fill > 0:
                pos_corrector = 0.27 + ((value_to_fill / 10) * 0.03)
                text1 = font.render(str(value_to_fill), 1, (0, 0, 0))
                screen.blit(text1, (cell_stt1 + cell_size_1 * pos_corrector, cell_stt2 + cell_size_2 * pos_corrector))

    while pygame.event.get():
        pass

    pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((pixels, (pixels + 100)))
    font = pygame.font.SysFont("comicsans", int(cell_size * 0.4))
    refresh_screen_parameters(3)

    sudoku = Sudoku()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    sudoku.update_puzzle(sudoku.get_clipboard())
                    refresh_screen_parameters(sudoku.puzzle.rank)
                elif event.key == pygame.K_4:
                    sudoku.update_puzzle(default_puzzle_2)
                    refresh_screen_parameters(4)
                elif event.key == pygame.K_RETURN:
                    time = datetime.now()
                    solve_puzzle(sudoku.puzzle, sudoku.matrix)
                    print(f"Duration: {datetime.now() - time}")
                elif event.key == pygame.K_r:
                    sudoku.reset()
            draw(sudoku.puzzle, sudoku.matrix)

            while pygame.event.get():
                pass

            pygame.display.update()

    pygame.quit()
