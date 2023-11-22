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
        row = [(vx, y) for vx in range(s) if vx != x]
        # col
        col = [(x, vy) for vy in range(s) if vy != y]
        # block
        block = [(vx, vy) for vx in range(x//bs * bs, x//bs * bs + bs) for vy in range(y//bs * bs, y//bs * bs + bs) if (vx, vy) != (x, y)]
        return set(row + col + block) # converting to a set is an easy way of getting rid of duplicates

class SimpleSolver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.evalutaions = 0

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
                    self.evalutaions += 1
                    if not i in block:
                        missing_values.append(i)

                # figure out coords of the open cells
                open_cells = [] # list of cells in the block that dont have a value yet            
                for i in range(size):
                    self.evalutaions += 1
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
                        self.evalutaions += 1
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
                    self.evalutaions += child_solver.evalutaions
                    
                    if output:
                        changed = True
                        self.sudoku.board = child.board
                        return True

        return self.sudoku.is_filled()
  
class AdvancedSolver(Solver):
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.evaluations = 0
        
    def purge(self, x, y, val, domains, variables):
        # remove value from all connected domains
        changed = False
        for x2, y2 in self.get_connected_cells(x, y).intersection(variables):
            self.evaluations += 1
            if val in domains[(x2, y2)]:
                domains[(x2, y2)].remove(val)
                changed = True
        
        # remove from variables, as it has been set and is no longer a variable
        variables.remove((x, y))
        self.evaluations += 1
        return changed
    
    def run(self, variables = None):
        if variables == None:
            variables = set([(x, y) for y in range(self.sudoku.size) for x in self.get_emtpy_cells(y)])
            self.evaluations += len(variables)
            
        domains = dict([((x, y), self.get_possible_values(x, y)) for x, y in variables])
        self.evaluations += len(domains)
        
        changed = True
        while changed:
            changed = False
            for x, y in variables.copy():
                self.evaluations += 1
                if len(domains[(x, y)]) <= 1:
                    if len(domains[(x, y)]) == 0:
                        return False # contradiction
                    
                    val = list(domains[(x, y)])[0]
                    self.sudoku.enter(x, y, val)
                    
                    changed = self.purge(x, y, val, domains, variables) or changed

        if len(variables) > 0:
            # take a guess by choosing a variable with the smalles possible domain to reduce guesses
            x, y = sorted(variables, key=lambda a : len(domains[a]))[0]
            
            for val in domains[(x, y)]:
                self.guesses += 1
                child = self.sudoku.clone()
                child.enter(x, y, val)
                child_solver = type(self)(child)
                
                # slight performance improvements, purging the guess is faster than making a new variables set
                new_variables = variables.copy()
                self.purge(x, y, val, domains, new_variables)
                output = child_solver.run(new_variables)
                self.guesses += child_solver.guesses
                self.evaluations += child_solver.evaluations
                
                if output:
                    changed = True
                    self.sudoku.board = child.board
                    return True # sudoku was completed by a guessed child
            return False # sudoku is not solvable
        return True # sudoku was completed without guessing (this iterations)
                   
class ArcConsistencySolver(Solver):
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.evaluations = 0
    
    def run(self):
        # prepares variables, domains and worklist (worklist contains all constraints)
        variables = set([(x, y) for y in range(self.sudoku.size) for x in self.get_emtpy_cells(y)]) # set of tuples
        domains = dict([((x, y), self.get_possible_values(x, y)) for x, y in variables]) # dict to link each position to a set of values
        worklist = [((x, y), (vx, vy)) for x, y in domains for vx, vy in self.get_connected_cells(x, y).intersection(domains)]  # list of constraints
        
        # iterate over worklist
        while len(worklist) > 0:
            a, b = worklist.pop()

            if self.reduce(a, b, domains):
                if len(domains[a]) == 0: 
                    return False
                worklist += [(c, a) for c in self.get_connected_cells(a[0], a[1]).intersection(domains) if c != a]
        
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
                self.evaluations += 1
                if va != vb:
                    found = True
            
            if not found:
                domains[a].remove(va)
                change = True
        return change
                
        
class AdvancedAC3Solver(ArcConsistencySolver):
    def __init__(self, sudoku: Sudoku):
        ArcConsistencySolver.__init__(self, sudoku)       
        
    def run(self):
        # setup stuff (either recieve all or create all)
        variables = set([(x, y) for y in range(self.sudoku.size) for x in self.get_emtpy_cells(y)]) # set of tuples
        domains = dict([((x, y), self.get_possible_values(x, y)) for x, y in variables]) # dict to link each position to a set of values
        worklist = [((x, y), (vx, vy)) for x, y in domains for vx, vy in self.get_connected_cells(x, y).intersection(domains)]  # list of constraints
        
        # iterate over worklist
        while len(worklist) > 0:
            a, b = worklist.pop()

            if self.reduce(a, b, domains):
                if len(domains[a]) == 0: 
                    return False
                worklist += [(c, a) for c in self.get_connected_cells(a[0],a[1]).intersection(domains) if c != a]
            
        
        # enter values into the sudoku
        for x, y in domains:
            # use backtracking, should the domain conatains more than one value
            if len(domains[(x, y)]) == 1:
                self.sudoku.enter(x, y, domains[(x, y)].pop())
            else:
                for val in domains[(x, y)]:
                    self.guesses += 1
                    child = self.sudoku.clone()
                    child.enter(x, y, val)
                    child_solver = type(self)(child)
                    if child_solver.run():
                        self.evaluations += child_solver.evaluations
                        self.guesses += child_solver.guesses
                        self.sudoku.board = child.board
                        return True # this means a child found a solution
                    self.evaluations += child_solver.evaluations
                    self.guesses += child_solver.guesses
                return False # if this gets reached somthing went REALLY wrong
        return True # reaching this means AC3 found a solution on its own
