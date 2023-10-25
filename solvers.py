from sudoku import *

class SimpleSolver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        
    def run(self):
        for i in range(9):
            bx, by = i % 3, i // 3
            block = self.sudoku.get_block_list(bx, by)
            
            # figure out which values are missing
            missing_values = []
            for i in range(self.sudoku.size):
                if not i in block:
                    missing_values.append(i)

            # figure out coords of the open cells
            open_cells = [] # list of cells in the block that dont have a value yet            
            for i in range(9):
                if block[i] == 0:
                    open_cells.append(i)

            # translate local list indexes into global coords
            open_cells = [(bx + (j % 3), by + (j // 3)) for j in open_cells]

            # iterate through all missing values and check if one uniquely fits into one spot
            for n in missing_values:
                pass      
            


f = open("Easy.txt", "r")
s = Sudoku(f.read())
s.print()
solver = SimpleSolver(s)
solver.run()