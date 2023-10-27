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
                    
class BorkenOptimisedSolver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.guesses = 0
        self.cycles = 0

    # def get_missing_vals(self, x, y):
    #     missing_values = []
    #     block = self.sudoku.get_block_list(x, y)
    #     for i in range(1, self.sudoku.size + 1):
    #         if not i in block:
    #             missing_values.append(i)
    #     return missing_values
    
    def get_missing_values(self, row):
        missing_values = []
        row_list = self.sudoku.get_row(row)
        for val in range(1, self.sudoku.size + 1):
            if val not in row_list:
                missing_values.append(val)
        return missing_values

    def get_emtpy_cells(self, row):
        empty_cells = []
        row_list = self.sudoku.get_row(row)
        for i in range(self.sudoku.size):
            if row_list[i] == 0:
                empty_cells.append(i)
        return empty_cells

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
                

if __name__ == "__main__":
    f = open("Sudoku1.txt", "r")
    s = Sudoku(f.read())
    # s = Sudoku(size = 9)
    s.print()
    solver = BorkenOptimisedSolver(s)
    # solver = SimpleSolver(s)
    output = solver.run()
    s.print()
    print("solved:\t\t", output,
          "\nguesses made:\t", solver.guesses,
          "\ncomparisons:\t", solver.cycles)

    # for s in load_multiple_from_file():
    #     solver = OptimisedSolver(s)
    #     output = solver.run()
    #     print(output, f"{solver.guesses:5d}", f"{solver.cycles:8d}")
