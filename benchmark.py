from solvers import *
from sudoku import *
import time


def benchmark():
    old_time = time.time_ns()
    
    for s in load_multiple_from_file():
        solver = SimpleSolver(s)
        output = solver.run()
        if not output:
            print("ERROR")
        
        # print(output, f"{solver.guesses:5d}", f"{solver.cycles:8d}")
    
    delta =  time.time_ns() - old_time 
    print(f"time needed: {(delta / 10**6):.5f}ms")
    # print(l[:10])
if __name__ == "__main__":
    benchmark()
        
# print(time.time_ns())
# print(time.time_ns())

