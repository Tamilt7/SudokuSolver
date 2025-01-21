from multiprocessing import Process, Queue, Event
from copy import deepcopy
import pygame
from datetime import datetime
from queue import Empty
import multiprocessing

backtracking_depth_cap = 10
backtracking_step = 5
worker_process_cap = 5

C_dark_grey = (50, 50, 50)
C_light_grey = (120, 120, 120)
C_red = (120, 30, 30)


def worker_process(process_id, process_depth, process_count, queue, completion_event, grid, actions):
    if completion_event.is_set() or (process_count >= worker_process_cap):
        return
    print(f"{process_count}th Process {process_id} at level {process_depth} started.")

    # solver = Solver(deepcopy(grid), actions)
    # solver.solve()

    # if solver.state_invalid:
    #     del solver
    #     return
    #
    # if solver.state_solved:
    #     queue.put((process_id, "Solution Found", solver.state))
    #     print(f"Process {process_id} found a solution!")
    #     completion_event.set()
    #     del solver
    #     return

    if process_depth < backtracking_depth_cap:
        child_processes = []
        next_actions_list = [[], [], []]
        next_actions_list = next_actions_list[:worker_process_cap - process_count]

        for idx, next_actions in enumerate(next_actions_list):
            child_id = f"{str(process_id)}.{str(process_depth + 1)}_C{str(idx + 1)}"
            process_count = process_count + 1
            p = Process(target=worker_process,
                        args=(child_id,
                              process_depth + 1,
                              process_count,  # pass the updated process count
                              queue,
                              completion_event,
                              deepcopy([]),
                              next_actions)
                        )
            p.start()
            child_processes.append(p)

        # del solver
        for p in child_processes:
            p.join()


def solve_puzzle(puzzle, matrix):
    result_queue = Queue()
    completion_event = Event()

    actions = []

    parent_process = Process(target=worker_process,
                             args=("1_P1", 1, 1, result_queue, completion_event, deepcopy([]), actions))
    parent_process.start()

    while not completion_event.is_set() and parent_process.is_alive():
        try:
            result = result_queue.get(timeout=1)  # Non-blocking check
            print(f"Main process received result: {result}")
            # matrix.grid = result[2]
        except Empty:  # Use queue.Empty for a more specific exception
            pass  # Timeout expired, keep checking

    parent_process.join()


def is_edge(idx, rank=3):
    return ((idx + 1) % rank == 0) | (idx == 0)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    pixels = 800
    cell_size = pixels / 9
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((pixels, (pixels + 100)))
    font = pygame.font.SysFont("comicsans", int(cell_size * 0.4))
    screen.fill((200, 200, 200))
    cell_size = pixels / 9
    font = pygame.font.SysFont("comicsans", int(cell_size * 0.4))

    matrix = []
    for i in range(9):
        row = []
        for j in range(9):
            col = []
            for k in range(9):
                col.append((k+1))
            row.append(col)
        matrix.append(row)

    puzzle = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(None)
        puzzle.append(row)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    screen.fill((200, 200, 200))
                    cell_size = pixels / 9
                    font = pygame.font.SysFont("comicsans", int(cell_size * 0.4))
                elif event.key == pygame.K_4:
                    screen.fill((200, 200, 200))
                    cell_size = pixels / 9
                    font = pygame.font.SysFont("comicsans", int(cell_size * 0.4))
                elif event.key == pygame.K_RETURN:
                    time = datetime.now()
                    solve_puzzle([], [])
                    print(f"Duration: {datetime.now() - time}")

            for i in range(9):
                for j in range(9):

                    cell_size_1 = (cell_size - 5) if is_edge(j, 3) else (cell_size - 1)
                    cell_size_2 = (cell_size - 5) if is_edge(i, 3) else (cell_size - 1)
                    cell_stt1 = 4 if j == 0 else (j * cell_size)
                    cell_stt2 = 4 if i == 0 else (i * cell_size)

                    if puzzle[i][j]:
                        value_to_fill = puzzle[i][j]

                        if False:
                            cell_bg_clr = C_red
                        else:
                            cell_bg_clr = C_dark_grey

                    elif len(matrix[i][j]) == 1:
                        value_to_fill = 0
                        cell_bg_clr = C_light_grey
                    else:
                        value_to_fill = 0
                        cell_bg_clr = C_light_grey

                    pygame.draw.rect(screen, cell_bg_clr, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))

            while pygame.event.get():
                pass

            pygame.display.update()

    pygame.quit()
