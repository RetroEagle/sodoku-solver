from sudoku import *

class SimpleSolver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        # sudoku.print()
        
    def run(self):
        changed = True
        while changed:
            changed = False
            hits = [] # (value, [(x, y)])
            for i in range(9): # iterates over each block
                bx, by = i % 3, i // 3
                block = self.sudoku.get_block_list(bx, by)
                
                # figure out which values are missing
                missing_values = []
                for i in range(1, self.sudoku.size + 1):
                    if not i in block:
                        missing_values.append(i)

                # figure out coords of the open cells
                open_cells = [] # list of cells in the block that dont have a value yet            
                for i in range(9):
                    if block[i] == 0:
                        open_cells.append(i)

                # translate local list indexes into global coords
                open_cells = [(bx * 3 + (j % 3), by * 3 + (j // 3)) for j in open_cells]
                
                # iterate through all missing values and check if one uniquely fits into one spot          
                for n in missing_values:
                    fits = [] # [(x, y)]
                    for x, y in open_cells:
                        # if s.check_block # dont need it
                        if s.check_hor_line(y, n):
                            if s.check_vert_line(x, n):
                                fits.append((x, y))

                    if len(fits) == 1:
                        changed = True
                        s.enter(fits[0][0], fits[0][1], n)
                        open_cells.remove((fits[0][0], fits[0][1]))
                    elif len(fits) == 0:
                        print("CONTRADICTION")
                        return False
                    
                    hits.append((n, fits))
                
            if changed == False and len(hits) > 0:
                hits.sort(key=lambda x : len(x[1]))
                # take a guess
                print("guesses", len(hits[0][1]))
                for x, y in hits[0][1]:
                    # print(x, y, hits[0][0])
                    # create new child sudoku
                    child = Sudoku(self.sudoku.export())
                    # implement guess
                    child.enter(x, y, hits[0][0])
                    # run guessed child
                    child_solver = SimpleSolver(child)
                    output = child_solver.run()
                    if output:
                        changed = True
                        print("SUCCESS!!!")
                        self.sudoku.board = child.board
                        child.print()
                        break
        return True
                    

f = open("Sudoku3.txt", "r")
s = Sudoku(f.read())
# s.print()

solver = SimpleSolver(s)
output = solver.run()
s.print()
print(output)

# for s in load_multiple_from_file():
#     solver = SimpleSolver(s)
#     solver.run()
#     print(solver.sudoku.is_filled())