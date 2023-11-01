#include <iostream>
#include <fstream>
#include <string>
#include <array>

using namespace std;

template <int size>
using matrix = array<array<int, size>, size>;

class Sudoku
{
private:
    matrix<9> board;

public:
    void load()
    {
        string line;
        ifstream file;
        file.open("sudokus/Sudoku1.txt");
        int row = 0;
        int col = 0;

        while (getline(file, line))
        {
            col = 0;
            for (char &ch : line)
            {
                board[row][col] = ch - '0';
                col++;
            }
            row++;
        }
        file.close();
    }

    void print()
    {
        for (auto &row : board)
        {
            for (int &val : row)
            {
                if (val > 0)
                {
                    cout << ' ' << val;
                } else
                {
                    cout << " .";
                }
            }
            cout << endl;
        }
    }

    bool enter(int x, int y, int val)
    {
        if (board[y][x])
        {
            throw invalid_argument("Value is already filled");
            // return false;
        } else
        {
            board[y][x] = val;
            return true;
        }

    }

    bool is_valid_move(int x, int y, int val)
    {
        if (board[x][y])
            return false;
        return true;
    }

    array<int, 9> get_row(int index)
    {
        // return board[index];
        array<int, 9> row;
        for (int i = 0; i < 9; i++)
        {
            row[i] = board[index][i];
        }
        return row;
    }

    array<int, 9> get_col(int index)
    {
        array<int, 9> column;
        for (int i = 0; i < 9; i++)
        {
            column[i] = board[i][index];
        }
        return column;
    }

    array<int, 9> get_block(int x, int y)
    {
        array<int, 9> block;
        for (int ty = 3 * y; ty < (3 + 3 * y); ty++)
        {
            for (int tx = 3 * x; tx < (3 + 3 * x); tx++)
            {
                block[(ty - 3 * y) * 3 + tx - 3 * x] = board[ty][tx];
            }
        }
        return block;
    }
};

class Solver
{
private:
    Sudoku sudoku;

public:
    Solver(Sudoku s)
    {
        sudoku = s;
    }

    bool run()
    {
        return false;
    }
};

void load(matrix<9> &arr)
{
    string line;
    ifstream file;
    file.open("sudokus/Sudoku1.txt");
    int row = 0;
    int col = 0;
    
    while(getline(file, line))
    {
        col = 0;
        for (char &ch : line)
        {
            // cout << ch << '\n';
            arr[row][col] = ch - '0';
            col++;
        }
        row++;
    }
    file.close();
}

int main(int argc, char *argv[])
{
    // cout << "teasdafsst" << endl;
    // array<std::array<int, 9>, 9> board[9][9];
    
    Sudoku sudoku;
    sudoku.load();
    
    Solver solver(sudoku);
    sudoku.print();
    // cout << sudoku.get_col(2) << endl;
    for (int &i : sudoku.get_block(1, 0))
        cout << i << endl;

    return 0;
}