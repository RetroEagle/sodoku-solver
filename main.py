from solvers import *
from sudoku import *

if __name__ == "__main__":
    f = open("Sudoku3.txt", "r")
    s = Sudoku(f.read())
    # s = Sudoku(size=16)
    s.print()
    # solver = AdvancedAC3Solver(s)
    solver = SimpleSolver(s)
    output = solver.run()
    s.print()
    print("solved:\t\t", solver.sudoku.is_correct(),
          "\nguesses made:\t", solver.guesses,
          "\ncomparisons:\t", solver.cycles)

    total1, total2 = 0, 0

    print("name comparisons guesses name\t       comparisons guesses")
    for s in load_multiple_from_file():
        solver = AdvancedSolver(s.clone())
        output = solver.run()
        
        solver2 = SimpleSolver(s)
        output2 = solver2.run()
        
        total1 += solver.cycles
        total2 += solver2.cycles
        
        # print(solver.sudoku.is_correct(), "\t", f"{solver.guesses:5d}", f"{solver.cycles:8d}")
        print(f"AC3: {solver.cycles:8d} {solver.guesses:5d} \t SimpleSolver: {solver2.cycles:8d} {solver2.guesses:5d}")
    
    print(total1, total2)

    print(s.export())