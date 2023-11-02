#include <iostream>
#include <fstream>
#include <string>
#include <array>
#include <tuple>
#include <vector>

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

    int get_empty_cell_count()
    {
        int count = 0;
        for (auto &row : board)
        {
            for (int &val : row)
            {
                if (val == 0)
                    count++;
            }
        }
        return count;
    }

    array<int, 9> get_row(int index)
    {
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

    vector<tuple<int, int>> get_empty_cells()
    {
        vector<tuple<int, int>> empty_cells;
        for (int y = 0; y < 9; y++)
        {
            for (int x = 0; x < 9; x++)
            {
                if (board[y][x] == 0)
                    empty_cells.push_back({x, y});
            }
        }
        return empty_cells;
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
        vector<tuple<int, int>> variables = sudoku.get_empty_cells();

        for (tuple<int, int> &x : variables)
        {
            cout << get<0>(x) << ' ' << get<1>(x) << endl;
        }

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
    // for (int &i : sudoku.get_block(1, 0))
    //     cout << i << endl;

    // cout << sudoku.get_empty_cell_count() << endl;

    // tuple<int, int> a = {1, 2};
    // tuple<int, int> b = {1, 2};

    // cout << (a == b) << endl;

    // array<int, 9> a = {1, 2, 3, 4, 5, 6};

    solver.run();

    return 0;
}