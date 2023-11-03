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

class Sudoku
{
private:
    matrix<9> board;

public:
    void load()
    {
        string line;
        ifstream file;
        file.open("sudokus/dummy1.txt");
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
        // check if value is already filled
        if (board[y][x])
            return false;

        // check row
        for (int &n : get_row(y))
        {
            if (n == val)
                return false;
        }
        // check colum
        for (int &n : get_col(x))
        {
            if (n == val)
                return false;
        }
        // check block
        for (int &n : get_block(x / 3, y / 3))
        {
            if (n == val)
                return false;
        }

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

    vector<tuple<int, int>> get_connected_cells(int x, int y, vector<tuple<int, int>> variables)
    {
        vector<tuple<int, int>> connected_cells;
        for (auto &var : variables)
            // if in row OR in column OR in block
            if (get<0>(var) == x || get<1>(var) == y || ((get<0>(var) / 3 == x / 3) && (get<1>(var) / 3 == y / 3)))
                if (get<0>(var) != x || get<1>(var) != y)
                    connected_cells.push_back({get<0>(var), get<1>(var)});

        return connected_cells;
    }

    vector<int> get_possible_values(int x, int y)
    {
        vector<int> values;
        for (int i = 1; i < 10; i++)
        {
            if (is_valid_move(x, y, i))
                values.push_back(i);

            // cout << "(" << x << ", " << y << ") " << i << " " << is_valid_move(x, y, i) << endl;
        }
        return values;
    }

    map<tuple<int, int>, vector<int>> get_domains(vector<tuple<int, int>> variables)
    {
        map<tuple<int, int>, vector<int>> domains;
        for (tuple <int, int> &pos : variables)
        {
            domains.insert({pos, get_possible_values(get<0>(pos), get<1>(pos))});
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

    bool purge(int x, int y, int val, map<tuple<int, int>, vector<int>> &domains, vector<tuple<int, int>> &variables)
    {
        bool changed = false;
        // adjust all related domains
        for (auto &pos : get_connected_cells(x, y, variables))
        {
            auto output = domains.find(pos);
            if (contains(val, (output->second)))
            {
                domains.erase(pos);
                changed = true;
            }
        }
        tuple<int, int> test = {x, y};
        // remove variable, as it has been filled
        for (int i = 0; i < variables.size(); i++)
        {
            if (variables[i] == test)
            {
                variables.erase(variables.begin() + i);
            }
        }
        return changed;
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

    Sudoku get_sudoku()
    {
        return sudoku;
    }

    bool run()
    {
        vector<tuple<int, int>> variables = sudoku.get_empty_cells();
        map<tuple<int, int>, vector<int>> domains = sudoku.get_domains(variables);

        bool changed = true;
        while (changed)
        {
            changed = false;
            for (auto &pos : variables)
            {
                int x = get<0>(pos);
                int y = get<1>(pos);

                auto output = domains.find(pos);

                if ((output->second).size() <= 1)
                {
                    if ((output->second).size() == 0)
                        return false;
                
                    int val = (output->second)[0];
                    // cout << x << " " << y << " " << val << " " << endl;
                    sudoku.enter(x, y, val);
                    sudoku.purge(x, y, val, domains, variables);
                    changed = true;
                }   
            }
        }

        
        // for (auto &x : domains)
        // {
        //     cout << get<0>(x.first) << ' ' << get<1>(x.first) << " : [ ";
        //     for (auto &v : x.second)
        //         cout << v << " ";
        //     cout << "]" <<endl;
        // }

        // for (auto &x : sudoku.get_possible_values(0, 0))
        // {
        //     // for (auto &y : get<0>(x))
        //     // {
        //     // }
        //     cout << x << endl;
        // }


        // for (auto &x : sudoku.get_connected_cells(0, 0, variables))
        // {
        //     cout << get<0>(x) << " " << get<1>(x) << endl;
        // }

        // vector<tuple<int, int>> test = sudoku.get_connected_cells(0, 0);

        // for (int i; i < )

        return false;
    }
};

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
    solver.get_sudoku().print();
    return 0;
}