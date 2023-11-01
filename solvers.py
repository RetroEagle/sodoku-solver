from sudoku import *

class Solver:
    def get_emtpy_cells(self, row):
        empty_cells = []
        row_list = self.sudoku.get_row(row)
        for i in range(self.sudoku.size):
            if row_list[i] == 0:
                empty_cells.append(i)
        
        return empty_cells
    
    def get_possible_values(self, x, y):
        val = self.sudoku.get_value(x, y)
        if val != 0: # this is in case x, y already has a value 
            return {val}
        possible_values = []
        for val in range(1, self.sudoku.size + 1):
            if self.sudoku.is_valid_move(x, y, val):
                possible_values.append(val)
        return set(possible_values)
    
    def get_connected_cells(self, x, y):
        s = self.sudoku.size
        bs = int(math.sqrt(s))
        # row
        row = [(vx, y) for vx in range(self.sudoku.size) if vx != x]
        # col
        col = [(x, vy) for vy in range(self.sudoku.size) if vy != y]
        # block
        block = [(vx, vy) for vx in range(x//bs * bs, x//bs * bs + bs) for vy in range(y//bs * bs, y//bs * bs + bs) if (vx, vy) != (x, y)]
        return set(row + col + block) # converting to a set is an easy way of getting rid of duplicates

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
                    self.cycles += 1
                    if not i in block:
                        missing_values.append(i)

                # figure out coords of the open cells
                open_cells = [] # list of cells in the block that dont have a value yet            
                for i in range(size):
                    self.cycles += 1
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
                        if self.sudoku.check_row(y, n):
                            if self.sudoku.check_col(x, n):
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
  
class AdvancedSolver(Solver):
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.cycles = 0
    
    def run(self):
        # prepares variables, domains and worklist (worklist contains all constraints)
        # variables = set([(x, y) for y in range(self.sudoku.size) for x in range(self.sudoku.size)])
        variables = set([(x, y) for y in range(self.sudoku.size) for x in self.get_emtpy_cells(y)]) # set of tuples
        domains = dict([((x, y), self.get_possible_values(x, y)) for x, y in variables]) # dict to link each position to a set of values
                    
class BorkenOptimisedSolver(Solver):
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.cycles = 0
    
    def get_missing_values(self, row):
        missing_values = []
        row_list = self.sudoku.get_row(row)
        for val in range(1, self.sudoku.size + 1):
            if val not in row_list:
                missing_values.append(val)
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
        missing_values = {} # row index: [val] # ITS JUST A LIST
        empty_cells = {} # row index: [cell id] # MAKE IT A LIST (later)

        available_values = [[] for _ in range(size + 1)] # [((row, col), amount of fits)]

        for row in range(size):
            missing_values.update({row: self.get_missing_values(row)})
            empty_cells.update({row: self.get_emtpy_cells(row)})

        possible_solutions = {} # global (row, col): [val]
        solutions = []
        for row in range(size):
            for col in empty_cells[row]:
                # print(row, col)
                fits = []
                for val in missing_values[row]:
                    if self.sudoku.check_col(col, val) and self.sudoku.check_block(col // block_size, row // block_size, val):
                        fits.append(val)

                possible_solutions.update({(row, col): fits})
                solutions.append(((row, col), fits))

                for val in fits:
                    available_values[val].append(((row, col), len(fits)))
                available_values[val].sort(key=lambda x: x[1])

        solution_dict = [[] for _ in range(size)]
        for key, lst in solutions:
            solution_dict[len(lst) - 1].append((key, lst))

        # print(solution_dict[0])

        # return False

        changed = True
        while changed:
            changed = False
            elem = None
            # print(solution_dict[0])
            # print(solution_dict[1])
            # print(solution_dict[2])

            for i in range(size):
                # print(key)
                if len(solution_dict[i]) > 0:
                    elem = solution_dict[i].pop()
                    break

            # print(elem)
            if elem == None or len(elem[1]) == 0:
                return False
            
            # print(solution_dict[4])

            if len(elem[1]) == 1:
                (row, col), (val,) = elem
                self.sudoku.enter(col, row, val)
                print("ENTERED: ", row, col, val)
                self.sudoku.print()
                changed = True
                
                # purge all values in that row, column and block
                i = 0
                while i < len(available_values[val]):
                    (r, c), l = available_values[val][i]
                    # if in col, row or block
                    # print((r, c), (row, col))
                    # print("ROW", c == col, "COL", r == row, "BLOCK", ((c // block_size == col // block_size) and (r // block_size == row // block_size)))
                    if c == col or r == row or ((c // block_size == col // block_size) and (r // block_size == row // block_size)):
                        # adjust available_values
                        if c == col and r == row:
                            del available_values[val][i]
                            i -= 1
                        else:
                            available_values[val][i] = ((r, c), l-1)
                        # remove from solution dict
                        # for j in range(len(solution_dict[l-1])):
                        j = 0
                        # print(solution_dict[l-1])
                        while j < len(solution_dict[l-1]):
                            # print("checking:", j, solution_dict[l-1][j], (r, c))
                            key, lst = solution_dict[l-1][j]
                            # print(key, r, c)
                            if key == (r, c):
                                print(key, lst, val)
                                lst.remove(val)
                                # print("from:", row, col)
                                print("REMOVED", r, c, val)
                                solution_dict[l-2].append(solution_dict[l-1].pop(j))
                                j -= 1
                            j += 1
                        print("ended", l)
                    i += 1

            else:
                return False # make a guess

        # for i in available_values:
        #     print(i)

        return False

class ArcConsistencySolver(Solver):
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.cycles = 0
        
        self.unary_cs = {} # unary constraints (not needed?)
        self.binary_cs = {} # binary constraints (always must be x != y)
    
    def run(self):
        # prepares variables, domains and worklist (worklist contains all constraints)
        # variables = set([(x, y) for y in range(self.sudoku.size) for x in range(self.sudoku.size)])
        variables = set([(x, y) for y in range(self.sudoku.size) for x in self.get_emtpy_cells(y)]) # set of tuples
        domains = dict([((x, y), self.get_possible_values(x, y)) for x, y in variables]) # dict to link each position to a set of values
        worklist = [((x, y), (vx, vy)) for x, y in variables for vx, vy in self.get_connected_cells(x, y).intersection(variables)] # list of constraints
        
        # iterate over worklist
        while len(worklist) > 0:
            a, b = worklist.pop()
            # self.cycles += 1 # cycle is better computed in reduce

            if self.reduce(a, b, domains):
                if len(domains[a]) == 0: 
                    return False
                worklist += [(c, a) for c in self.get_connected_cells(a[0], a[1]).intersection(variables) if c != a]
            
        solved = True
        # enter finished values into sudoku
        for x, y in domains:
            if len(domains[(x, y)]) == 1:
                self.sudoku.enter(x, y, domains[(x, y)].pop())
            else:
                solved = False
            
        return solved
        
    def reduce(self, a, b, domains):
        change = False
        for va in list(domains[a]):
            found = False
            for vb in list(domains[b]):
                self.cycles += 1
                if va != vb:
                    found = True
            
            if not found:
                domains[a].remove(va)
                change = True
                # return True
                
        return change
        
class AdvancedAC3Solver(ArcConsistencySolver):
    def __init__(self, sudoku: Sudoku):
        ArcConsistencySolver.__init__(self, sudoku)       
        
    def run(self):
        # setup stuff (either recieve all or create all)
        variables = set([(x, y) for y in range(self.sudoku.size) for x in self.get_emtpy_cells(y)]) # set of tuples
        domains = dict([((x, y), self.get_possible_values(x, y)) for x, y in variables]) # dict to link each position to a set of values
        worklist = [((x, y), (vx, vy)) for x, y in variables for vx, vy in self.get_connected_cells(x, y).intersection(variables)] # list of constraints
        
        self.cycles += len(variables) + len(domains) + len(worklist) # account for computational steps needed to create lists (technically not needed)
        # its also missing some computations in worklist because I first call get_connected_cells() but then discard most values by intersecting the set with variables
        # but ehh, whatever. Insignificant
        
        # iterate over worklist
        while len(worklist) > 0:
            a, b = worklist.pop()
            # self.cycles += 1 # cycle is better computed in reduce

            if self.reduce(a, b, domains):
                if len(domains[a]) == 0: 
                    return False
                worklist += [(c, a) for c in self.get_connected_cells(a[0], a[1]).intersection(variables) if c != a]
            
            
        for x, y in domains:
            if len(domains[(x, y)]) == 1:
                self.sudoku.enter(x, y, domains[(x, y)].pop())
            else:
                for val in domains[(x, y)]:
                    self.guesses += 1
                    child = self.sudoku.clone()
                    child.enter(x, y, val)
                    child_solver = AdvancedAC3Solver(child)
                    if child_solver.run():
                        self.cycles += child_solver.cycles
                        self.guesses += child_solver.guesses
                        self.sudoku.board = child.board
                        return True # this means a child found a solution
                    self.cycles += child_solver.cycles
                    self.guesses += child_solver.guesses
                return False # if this gets reached somthing went REALLY wrong
        return True # reaching this means AC3 found a solution on its own
    
if __name__ == "__main__":
    f = open("Sudoku3.txt", "r")
    s = Sudoku(f.read())
    
    s.print()
    # solver = AdvancedAC3Solver(s)
    solver = AdvancedSolver(s)
    output = solver.run()
    s.print()
    print("solved:\t\t", solver.sudoku.is_correct(),
          "\nguesses made:\t", solver.guesses,
          "\ncomparisons:\t", solver.cycles)

    # print("name comparisons guesses name\t       comparisons guesses")
    # for s in load_multiple_from_file()[:10]:
    #     solver = AdvancedAC3Solver(s.clone())
    #     output = solver.run()
        
    #     solver2 = SimpleSolver(s)
    #     output2 = solver2.run()
        
    #     # print(solver.sudoku.is_correct(), "\t", f"{solver.guesses:5d}", f"{solver.cycles:8d}")
    #     # print(solver.sudoku.is_correct(), "\t", f"{solver.guesses:5d}", f"{solver.cycles:8d}")
    #     print(f"AC3: {solver.cycles:8d} {solver.guesses:5d} \t SimpleSolver: {solver2.cycles:8d} {solver2.guesses:5d}")
        
