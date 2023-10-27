from sudoku import *

class SimpleSolver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.cycles = 0

    def run(self):
        size, block_size = self.sudoku.size, self.sudoku.block_size
        changed = True
        while changed:
            changed = False
            hits = [] # (value, [(x, y)])
            for i in range(size): # iterates over each block
                bx, by = i % block_size, i // block_size
                block = self.sudoku.get_block_list(bx, by)
                
                # figure out which values are missing
                missing_values = []
                for i in range(1, size + 1):
                    if not i in block:
                        missing_values.append(i)

                # figure out coords of the open cells
                open_cells = [] # list of cells in the block that dont have a value yet            
                for i in range(size):
                    if block[i] == 0:
                        open_cells.append(i)

                # translate local list indexes into global coords
                open_cells = [(bx * block_size + (j % block_size),
                               by * block_size + (j // block_size)) 
                               for j in open_cells]
                
                # iterate through all missing values and check if one uniquely fits into one spot          
                for n in missing_values:
                    fits = [] # [(x, y)]
                    for x, y in open_cells:
                        self.cycles += 1
                        # if s.check_block # dont need it
                        if self.sudoku.check_hor_line(y, n):
                            if self.sudoku.check_vert_line(x, n):
                                fits.append((x, y))

                    if len(fits) == 1:
                        changed = True
                        self.sudoku.enter(fits[0][0], fits[0][1], n)
                        open_cells.remove((fits[0][0], fits[0][1]))
                    elif len(fits) == 0:
                        # contradiction
                        return False
                    
                    hits.append((n, fits))
                
            if changed == False and len(hits) > 0:
                # sort for the hit with the lowest amount of potential guesses
                # the goal is to solve as much as possible without having to guess 
                hits.sort(key=lambda x : len(x[1]))

                # take a guess
                for x, y in hits[0][1]:
                    self.guesses += 1
                    # create new child sudoku
                    # child = Sudoku(board=self.sudoku.export(), size=self.sudoku.size)
                    child = self.sudoku.clone()
                    # implement guess
                    child.enter(x, y, hits[0][0])
                    # run guessed child
                    child_solver = SimpleSolver(child)
                    output = child_solver.run()

                    self.guesses += child_solver.guesses
                    self.cycles += child_solver.cycles
                    
                    if output:
                        changed = True
                        self.sudoku.board = child.board
                        return True

        return self.sudoku.is_filled()
                    
class OptimisedSolver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.cycles = 0

    def get_missing_vals(self, x, y):
        missing_values = []
        block = self.sudoku.get_block_list(x, y)
        for i in range(1, self.sudoku.size + 1):
            if not i in block:
                missing_values.append(i)
        return missing_values
    
    def get_open_cells(self, x, y):
        open_cells = [] 
        block = self.sudoku.get_block_list(x, y)   
        for i in range(self.sudoku.size):
            if block[i] == 0:
                open_cells.append(i)
        return open_cells

    def run(self):
        size, block_size = self.sudoku.size, self.sudoku.block_size
        changed = True
        missing_values = [self.get_missing_vals(i % block_size, i // block_size) for i in range(size)]
        open_cells = [self.get_open_cells(i % block_size, i // block_size) for i in range(size)]
        
        while changed:
            changed = False
            hits = [] # (value, [(x, y)])
            for i in range(size): # iterates over each block
                bx, by = i % block_size, i // block_size
                block = self.sudoku.get_block_list(bx, by)                
                
                # iterate through all missing values and check if one uniquely fits into one spot          
                for n in missing_values[i]:
                    fits = [] # [(x, y)]
                    for j in open_cells[i]:
                        
                        # if s.check_block # dont need it
                        self.cycles += 1
                        x, y = bx * block_size + (j % block_size), by * block_size + (j // block_size)
                        if self.sudoku.check_hor_line(y, n):
                            if self.sudoku.check_vert_line(x, n):
                                fits.append((x, y, j, n))

                    if len(fits) == 1:
                        changed = True
                        self.sudoku.enter(fits[0][0], fits[0][1], n)
                        
                        open_cells[i].remove(fits[0][2])
                        missing_values[i].remove(fits[0][3])
                    elif len(fits) == 0:
                        # contradiction
                        return False
                    
                    hits.append((n, fits))
                
            if changed == False and len(hits) > 0:
                # sort for the hit with the lowest amount of potential guesses
                # the goal is to solve as much as possible without having to guess 
                hits.sort(key=lambda x : len(x[1]))

                # take a guess
                for i in hits[0][1]:
                    self.guesses += 1
                    x, y = bx * block_size + (j % block_size), by * block_size + (j // block_size)
                    # create new child sudoku
                    # child = Sudoku(board=self.sudoku.export(), size=self.sudoku.size)
                    child = self.sudoku.clone()
                    # implement guess
                    child.enter(x, y, hits[0][0])
                    # run guessed child
                    # child_solver = OptimisedSolver(child)
                    child_solver = type(self)(child)
                    output = child_solver.run()

                    self.guesses += child_solver.guesses
                    self.cycles += child_solver.cycles
                    
                    if output:
                        changed = True
                        self.sudoku.board = child.board
                        return True

        return self.sudoku.is_filled()

if __name__ == "__main__":
    f = open("Sudoku1.txt", "r")
    s = Sudoku(f.read())
    # s = Sudoku(size = 9)
    # s.print()
    solver = OptimisedSolver(s)
    output = solver.run()
    s.print()
    print("solved:\t\t", output,
          "\nguesses made:\t", solver.guesses,
          "\ncomparisons:\t", solver.cycles)

    for s in load_multiple_from_file():
        solver = OptimisedSolver(s)
        output = solver.run()
        print(output, f"{solver.guesses:5d}", f"{solver.cycles:8d}")
