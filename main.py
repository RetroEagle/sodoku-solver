from solvers import *
from sudoku import *

if __name__ == "__main__":
    f = open("sudokus/Sudoku1.txt", "r")
    s = Sudoku(f.read())
    # s = Sudoku(size=16)
    s.print()
    solver = AdvancedAC3Solver(s)
#     solver = AC3PriorityQueue(s)
    output = solver.run()
    s.print()
    print("solved:\t\t", solver.sudoku.is_correct(),
          "\nguesses made:\t", solver.guesses,
          "\ncomparisons:\t", solver.evaluations)

    total1, total2 = 0, 0