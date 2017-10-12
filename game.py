import numpy as np


def read_input(fname):  # -> n, p, t, board
    ''' Input lines format:
    1) integer n: the width and height of the board s.t. 0 < n <= 26
    2) integer p: number of fruit types s.t. 0 < p <= 9
    3) positive float t: remaining time in seconds
    4) the n x n board
        => n characters + EOL per line
        => each character:  0->p-1 OR *
    '''
    with open(fname, "r") as f:
        lines = f.read().split()

        n = int(lines[0])
        p = int(lines[1])
        t = float(lines[2])
        temp_grid = lines[3:]
    # Sanity checks
    assert(len(lines) == n + 3)
    assert(0 < n <= 26)
    assert(0 < p <= 9)
    assert(t > 0.0)
    assert(len(temp_grid) == n)

    # REVIEW Would forcing asterisk to a magic integer give us computational
    # bonus due to consistent data type? If so, is it even worth it?
    grid = []
    for row in temp_grid:
        items = []
        for char in row:
            items.append(char)
        grid.append(np.array(items))
    grid = np.array(grid)

    return n, p, t, grid

def printg(grid):
    n = len(grid)
    # A = 65
    print("   ", end="")
    for i in range(n):
        print(chr(65 + i) + " ", end="")
    print("")
    ind = 0
    for row in grid:
        ind += 1
        if ind >= 10:
            print(ind, end=" ")
        else:
            print(ind, end="  ")
        for item in row:
            print(item + " ", end="")
        print("")


def indices_to_coord(y, x):
    col = chr(65 + x)
    row = y + 1
    coord = "" + col + str(row)
    return coord


def coord_to_indices(coord_string):
    assert len(coord_string) == 2, "Invalid coordinate string"
    col = ord(coord_string[1]) - 65
    row = int(coord_string[2]) - 1


def find_clusters(grid):
    pass


def select_cluster(grid, cluster):
    pass


if __name__ == "__main__":
    IN_DIR = "tests/in/"
    n, p, t, grid = read_input(IN_DIR + "input_3.txt")
    printg(grid)
'''

OUTPUT
1) Selected move as two characters:
    -> A-Z representing column number (A is leftmost)
    -> 1-26 (1 is top row)
2) nxn board after gravity has been applied
'''
