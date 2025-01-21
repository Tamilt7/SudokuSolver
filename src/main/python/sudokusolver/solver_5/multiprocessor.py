from multiprocessing import Process, Queue, Event
from copy import deepcopy
from itertools import product
import pygame

from sudokusolver.solver_5.App import App
from sudokusolver.solver_5.Solver import Solver

backtracking_depth_cap = 10
backtracking_step = 5
worker_process_cap = 5


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
        # print(f"Process {process_id} terminated")
        del solver
        return

    if solver.state_solved:
        queue.put((process_id, "Solution Found", solver.state))
        print(f"Process {process_id} found a solution!")
        completion_event.set()
        del solver
        return

    # If the result state is valid and not solved, trigger sub processes
    if process_depth < backtracking_depth_cap:
        child_processes = []
        next_actions_list = get_next_set_of_actions(solver.state)
        next_actions_list = next_actions_list[:worker_process_cap - process_count - len(next_actions_list)]

        for idx, next_actions in enumerate(next_actions_list):
            child_id = f"{str(process_id)}.{str(process_depth + 1)}_C{str(idx + 1)}"
            process_count += 1
            p = Process(target=worker_process,
                        args=(child_id,
                              process_depth + 1,
                              process_count,
                              queue,
                              completion_event,
                              deepcopy(solver.state),
                              next_actions)
                        )
            p.start()
            child_processes.append(p)

        for p in child_processes:
            p.join()


class MultiProcessor(App):
    def __init__(self):
        super().__init__()

    def solve_puzzle(self):
        result_queue = Queue()
        completion_event = Event()

        actions = self.get_actions_from_puzzle(self.puzzle)

        parent_process = Process(target=worker_process,
                                 args=("1_P1", 1, 1, result_queue, completion_event, deepcopy(self.matrix.grid), actions))
        parent_process.start()

        while not completion_event.is_set() and parent_process.is_alive():
            try:
                # Check if any results are available in the queue
                result = result_queue.get(timeout=1)  # Non-blocking check
                print(f"Main process received result: {result}")
                self.matrix.grid = result[2]
            except:
                pass  # Timeout expired, keep checking

        parent_process.join()

        self.draw()


if __name__ == "__main__":

    pygame.font.init()
    pygame.init()
    MultiProcessor().run()
    pygame.quit()
