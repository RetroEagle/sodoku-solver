import numpy as np
import math
import itertools

class Sudoku:
    def __init__(self, board = None, size=9):
        self.board = np.array([[0 for _ in range(size)] for _ in range(size)])
        self.size = size
        self.block_size = int(math.sqrt(size))
        if not (board == None):
            self.load(board)

    def load(self, s):
        lists = s.split()
        self.size = len(lists)
        for y in range(len(lists)):
            for x in range(len(lists[y])):
                self.board[y][x] = int(lists[y][x])
        
    def print(self):
        spacing = int(np.log10(self.size)) + 2
        for y in range(self.size):
            if not y % self.block_size and y > 0:
                for i in range(self.block_size - 1):
                    print(chr(8213) * (spacing * self.block_size + 1) + "+", end="")
                print(chr(8213) * (spacing * self.block_size + 1))
                      
            for x in range(self.size):
                if not x % self.block_size and x > 0:
                    print(" " + chr(124), end="")
                print((f"{(self.board[y][x]):{spacing}d}") if self.board[y][x] > 0 else " " * spacing, end="")
            print()

                              
    def print_raw(self):
        print(self.board)

    def enter(self, x, y, val): # enters value without checkig if it is a valid move 
        self.board[y][x] = val

    def enter_attempt(self, x, y, val):
        if self.is_valid_move(x, y, val):
            print("Valid")
            self.enter(x, y, val)
        else:
            print("Invalid!!!")
            
    def is_valid_move(self, x, y, val):
        # first check if move is on board
        if x >= self.size or y >= self.size:
            raise Exception("Value outside playingfield")
        
        # check if cell is already filled
        if self.board[y][x] != 0:
            return False

        # check if value is already blocked in the two lines and block
        if val in self.get_col(x):
            return False
        
        if val in self.get_row(y):
            return False
        
        if val in self.get_block_list(x // self.block_size, y // self.block_size):
            return False
        return True
    
    def is_filled(self):
        for row in self.board:
            for val in row:
                if val == 0:
                    return False
        return True
    
    def is_correct(self):
        # this does not need to be efficient, just a very simple short way of checking
        # works by grouping the data. If there are 9 groups then all values from 1-9 are present
        for i in range(self.size):
            if len(list(itertools.groupby(self.get_row(i)))) != self.size:
                return False
            if len(list(itertools.groupby(self.get_col(i)))) != self.size:
                return False
            if len(list(itertools.groupby(self.get_block_list(i//3, i%3)))) != self.size:
                return False
        return True
    
    def get_value(self, x, y):
        return self.board[y][x]

    def get_col(self, index):
        return self.board[:, index]
        
    def get_row(self, index):
        return self.board[index]

    def get_block(self, x, y):
        return self.board[y * self.block_size : (y + 1) * self.block_size,
                          x * self.block_size : (x + 1) * self.block_size]

    def get_block_list(self, x, y):
        return list(itertools.chain.from_iterable(self.board[y * self.block_size : (y + 1) * self.block_size, 
                                                             x * self.block_size : (x + 1) * self.block_size]))
    
    def check_block(self, x, y, val):
        return not val in self.get_block_list(x, y)

    def check_col(self, index, val):
        return not val in self.get_col(index)

    def check_row(self, index, val):
        return not val in self.get_row(index)
    
    def count_emtpy_cells(self):
        return sum([list(self.get_row(i)).count(0) for i in range(self.size)])
    
    def export(self):
        exp_str = ""
        for line in self.board:
            exp_str += "".join([str(n) for n in line]) + "\n"
        return exp_str
        
    def clone(self):
        # more efficient then exporting and importing via string... slightly
        new_sudoku = Sudoku(size=self.size)
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                new_sudoku.board[y][x] = self.board[y][x]
        return new_sudoku


def load_multiple_from_file(file = "sudokus/test_sudokus.txt"):
    f = open(file)
    sudokus = [Sudoku(i[4:]) for i in f.read().split("Grid")[1:]]
    return sudokus

if __name__ == "__main__":
    f = open("Sudoku5.txt", "r")
    s = Sudoku(f.read())
    s.print()
    print(s.count_emtpy_cells())