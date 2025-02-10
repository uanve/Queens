# Queens Solver

This repository contains a Python script (`queens.py`) that automates solving a Queens Puzzle available at [queens-game.com](https://www.queens-game.com/?map=map66). The script uses **Selenium** for web automation and **OR-Tools** (CP-SAT solver) for constraint programming. It navigates to the game page, scrapes the grid layout, formulates the puzzle as a constraint satisfaction problem, computes a valid solution, and simulates clicks to input the solution on the webpage.

## Features

- **Web Automation:**  
  Uses Selenium to launch a Chrome browser, load the puzzle page, and interact with the grid elements.
  
- **Constraint Programming:**  
  Implements a CP model where:
  - Exactly one queen is placed in each region.
  - No more than one queen is placed per row or column.
  - Queens cannot be adjacent (including diagonally).
  
- **Automated Input:**  
  Once the solution is found, the script simulates mouse clicks on the corresponding grid cells to automatically fill in the solution.

## Requirements

- **Python 3.6+**  
- **Selenium:**  
  Install via pip:
  ```bash
  pip install selenium
