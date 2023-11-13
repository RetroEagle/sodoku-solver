#include <iostream>
#include <fstream>
#include <string>
#include <array>
#include <tuple>
#include <vector>
#include <map>

using namespace std;

template <int size>
using matrix = array<array<int, size>, size>;

const int SIZE = 9;
const int BLOCK_SIZE = 3;

struct pos
{
    int x = 0;
    int y = 0;
    auto operator<=>(const pos &) const = default;
};

class Sudoku
{
private:
    matrix<SIZE> board;

public:
    matrix<SIZE> get_board()
    {
        return board;
    }

    void init()
    {
        for (int y = 0; y < SIZE; y++)
        {
            for (int x = 0; x < SIZE; x++)
            {
                board[y][x] = 0;
            }
        }
    }

    void load()
    {
        string line;
        ifstream file;
        file.open("sudokus/Sudoku3.txt");
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

    void loads(Sudoku s)
    {
        matrix<SIZE> b = s.get_board();
        for (int y = 0; y < SIZE; y++)
        {
            for (int x = 0; x < SIZE; x++)
            {
                board[y][x] = b[y][x];
            }
        }
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
                }
                else
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
        }
        else
        {
            board[y][x] = val;
            return true;
        }
    }

    bool is_valid_move(int x, int y, int val)
    {
        // check if value is already filled
        if (board[y][x])
            return false;

        // check row
        for (int &n : get_row(y))
            if (n == val)
                return false;

        // check colum
        for (int &n : get_col(x))
            if (n == val)
                return false;

        // check block
        for (int &n : get_block(x / BLOCK_SIZE, y / BLOCK_SIZE))
            if (n == val)
                return false;

        return true;
    }

    int get_empty_cell_count()
    {
        int count = 0;
        for (auto &row : board)
            for (int &val : row)
                if (val == 0)
                    count++;

        return count;
    }

    array<int, SIZE> get_row(int index)
    {
        array<int, SIZE> row;
        for (int i = 0; i < SIZE; i++)
            row[i] = board[index][i];

        return row;
    }

    array<int, SIZE> get_col(int index)
    {
        array<int, SIZE> column;
        for (int i = 0; i < SIZE; i++)
            column[i] = board[i][index];

        return column;
    }

    array<int, SIZE> get_block(int x, int y)
    {
        array<int, SIZE> block;
        for (int ty = BLOCK_SIZE * y; ty < (BLOCK_SIZE + BLOCK_SIZE * y); ty++)
            for (int tx = BLOCK_SIZE * x; tx < (BLOCK_SIZE + BLOCK_SIZE * x); tx++)
                block[(ty - BLOCK_SIZE * y) * BLOCK_SIZE + tx - BLOCK_SIZE * x] = board[ty][tx];

        return block;
    }

    vector<pos> get_empty_cells()
    {
        vector<pos> empty_cells;
        for (int y = 0; y < SIZE; y++)
            for (int x = 0; x < SIZE; x++)
                if (board[y][x] == 0)
                    empty_cells.push_back(pos{x, y});

        return empty_cells;
    }

    vector<pos> get_connected_cells(int x, int y, vector<pos> variables)
    {
        vector<pos> connected_cells;
        for (auto &var : variables)
            // if in row OR in column OR in block
            if (var.x == x || var.y == y || ((var.x / BLOCK_SIZE == x / BLOCK_SIZE) && (var.y / BLOCK_SIZE == y / BLOCK_SIZE)))
                if (var.x != x || var.y != y)
                    connected_cells.push_back({var.x, var.y});

        return connected_cells;
    }

    vector<int> get_possible_values(int x, int y)
    {
        vector<int> values;
        for (int i = 1; i < 10; i++)
            if (is_valid_move(x, y, i))
                values.push_back(i);

        return values;
    }

    map<pos, vector<int>> get_domains(vector<pos> variables)
    {
        map<pos, vector<int>> domains;
        for (pos &p : variables)
        {
            domains.insert({p, get_possible_values(p.x, p.y)});
        }
        return domains;
    }

    bool contains(int value, vector<int> array)
    {
        for (int &i : array)
            if (i == value)
                return true;
        return false;
    }

    bool purge(int x, int y, int val, map<pos, vector<int>> &domains, vector<pos> &variables)
    {
        bool changed = false;
        // adjust all related domains
        for (pos &p : get_connected_cells(x, y, variables))
        {
            auto output = domains.find(p);
            if (contains(val, (output->second)))
            {
                erase((output->second), val);
                changed = true;
            }
        }

        domains.erase(pos{x, y}); // not strictly neccessary
        erase(variables, pos{x, y});
        return changed;
    }
};

class Solver
{
private:
    Sudoku &sudoku;

public:
    Solver(Sudoku &s) : sudoku(s) {}

    Sudoku get_sudoku()
    {
        return sudoku;
    }

    bool run()
    {
        vector<pos> variables = sudoku.get_empty_cells();
        map<pos, vector<int>> domains = sudoku.get_domains(variables);

        bool changed = true;
        while (changed)
        {
            changed = false;
            for (int i = 0; i < variables.size(); i++)
            {
                pos p = variables[i];
                auto output = domains.find(p);

                if ((output->second).size() <= 1)
                {
                    if ((output->second).size() == 0)
                        return false; // contradiction

                    int val = (output->second)[0];

                    sudoku.enter(p.x, p.y, val);
                    sudoku.purge(p.x, p.y, val, domains, variables);
                    changed = true; // remove val from connected domains
                    i--; // reduce counter as we remove an element from list we are iterating over
                }
            }
        }
        // make a guess
        if (variables.size() > 0)
        {
            pos p = domains.begin()->first;
            vector<int> choices = domains.begin()->second;

            for (auto &x : domains)
            {
                if (x.second.size() < choices.size())
                {
                    p = x.first;
                    choices = x.second;
                }
            }
            
            for (int &guess : choices)
            {
                Sudoku* child_sudoku = new Sudoku(sudoku);
                (*child_sudoku).enter(p.x, p.y, guess);

                Solver child_solver(*child_sudoku);
                if (child_solver.run())
                {
                    sudoku = *child_sudoku;
                    return true; // child has solved the sudoku
                }
            }
            return false; // sudoku is impossibel
        }
        return true; // soduko has been solved without a guess
    }
};

int main(int argc, char *argv[])
{
    Sudoku sudoku;
    sudoku.load();
    // sudoku.init();

    Solver solver(sudoku);
    
    sudoku.print();
    solver.run();
    sudoku.print();

    return 0;
}