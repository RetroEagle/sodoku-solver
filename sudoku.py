class Sudoku:
    def __init__(self):
        self.board = [[-1 for j in range(9)] for i in range(9)]

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
                    print((f"{(self.board[y][x]):2d}").replace(" ", chr(9632)) if self.board[y][x] > 0 else chr(9632) * 2, end="")   
                    # print("..", end="")
                print(chr(9632))

            else:
                for x in range(9):
                    if not x % 3 and x > 0:
                        print(" " + chr(124), end="")
                    print((f"{(self.board[y][x]):2d}") if self.board[y][x] > 0 else "  ", end="")   
                print()

    def enter(self, x, y, val):
        self.board[y][x] = val


    def load_sudoku(self, s):
        pass

f = open("~/projects/log-reader/sodoku-solver/Sudoku1.txt", "r")

s = Sudoku()
s.enter(1, 2, 3)
s.enter(1, 3, 3)
s.enter(1, 4, 3)
# s.print()
# s.enter(int(input("x")), int(input("y")), int(input("val")))
# s.print()
s.print_marked(1, 2)