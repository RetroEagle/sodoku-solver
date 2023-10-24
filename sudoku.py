import numpy as np
import math
import itertools

class Sudoku:
    def __init__(self, board = None, size=9):
        self.board = np.array([[0 for j in range(9)] for i in range(9)])
        self.size = size
        self.block_size = math.sqrt(size)
        if not board == None:
            self.load(board)

    def print(self):
        for y in range(9):
            if not y % 3 and y > 0:
                #  print("".join([chr(8213) * 2 if (x % 3 or x == 0)else "+" for x in range(9)]))
                print(chr(8213) * 7 + "+" + chr(8213) * 7 + "+" + chr(8213) * 7)

            for x in range(9):
                if not x % 3 and x > 0:
                    print(" " + chr(124), end="")
                print((f"{(self.board[y][x]):2d}") if self.board[y][x] > 0 else "  ", end="")   

            print()
    
    def print_marked(self, mx, my):
        for y in range(9):
            if not y % 3 and y > 0:
                #  print("".join([chr(8213) * 2 if (x % 3 or x == 0)else "+" for x in range(9)]))

                print(chr(8213) * 7 + "+" + chr(8213) * 7 + "+" + chr(8213) * 7)
                

            if y == my:
                for x in range(9):
                    if not x % 3 and x > 0:
                        print(chr(9632) + chr(124), end="")
                    
                    if x == mx:
                        print(" ", end=chr(9632))
                    else:
                        print((f"{(self.board[y][x]):2d}").replace(" ", chr(9632)) if self.board[y][x] > 0 else chr(9632) * 2, end="")   
                    # print("..", end="")
                print(chr(9632))

            else:
                for x in range(9):
                    if not x % 3 and x > 0:
                        print(" " + chr(124), end="")

                    if x == mx:
                        print((f"{(self.board[y][x]):2d}").replace(" ", chr(9608)) if self.board[y][x] > 1 else chr(9608) + " ", end="")
                    else: 
                        print((f"{(self.board[y][x]):2d}") if self.board[y][x] > 1 else "  ", end="")   
                print()

    def enter(self, x, y, val):
        self.board[y][x] = val

    def load(self, s):
        lists = s.split()
        for y in range(len(lists)):
            for x in range(len(lists[y])):
                self.board[y][x] = int(lists[y][x])

    def get_vert_line(self, index):
        return self.board[:, index]
        
    def get_hor_line(self, index):
        return self.board[index]

    def get_block(self, x, y):
        return self.board[y*3:(y+1)*3, x*3:(x+1)*3]

    def get_block_list(self, x, y):
        return list(itertools.chain.from_iterable(self.board[y*3:(y+1)*3, x*3:(x+1)*3]))
    
    def check_block(self, x, y):
        pass

    def check_vert_line(self, index):
        pass

    def check_hor_line(self, index):
        pass

    def check(self):
        # checks all


f = open("Sudoku1.txt", "r")
# print(f.read())

s = Sudoku(f.read())
s.print()
print(s.get_block_list(1, 2))