# Sudoku Solver App

An interactive and engaging Sudoku Solver built using Pygame, offering multiple solving techniques and a smooth user experience. The app is designed to cater to players of all skill levels, featuring real-time puzzle-solving and dynamic puzzle generation. Whether you're a beginner or a seasoned Sudoku enthusiast, this app provides a fun and educational experience.

## Features

- **Dynamic Puzzle Generation**: Generate Sudoku puzzles of varying difficulty levels with customizable grid sizes.
- **Multiple Solving Techniques**: Includes various solving algorithms such as:
    - **Custom Algorithm**: A human-like approach for solving puzzles using logical deduction.
    - **Backtracking Solver**: A recursive algorithm for solving puzzles through trial and error.
    - **Parallel Backtracking**: An optimized version using multiprocessing for faster solution discovery.
    - **SAT Solver**: A high performant boolean based solver.
- **Interactive User Interface**: Clean and intuitive Pygame-based interface for puzzle interaction.
- **Real-time Puzzle Solving**: Instant puzzle-solving capabilities to aid users in learning and solving Sudoku.
- **Customizable Themes**: Personalize the appearance of the GUI with various color themes. (Work in Progress)

## Installation

To get started with the Sudoku Solver, follow these steps:

### Prerequisites

- Python 3.9
- Pygame library
- flask socketio

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/ThamizhLabs/SudokuSolver.git
   cd SudokuSolver
   ```

2. Install dependencies:

   ```bash
   conda env create -f env.yml
   ```

3. Run the game:

   ```bash
   python run_sudoku.py
   ```

The Solver will launch in a new window, and you can paste your question from an Excel table.
