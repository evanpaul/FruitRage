import numpy as np
import copy


class Cluster:
    def __init__(self, value):
        self.value = value
        self.cells = []

    def add_cell(self, y, x):
        self.cells.append((y, x))

    def display(self, grid):
        if len(self.cells) == 1:
            return
        g = copy.deepcopy(grid)
        for c in self.cells:
            g[c[0]][c[1]] = "X"
        print(g)


class Neighbor:
    def __init__(self, y, x):
        self.y = y
        self.x = x


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


# REVIEW THIS NEEDS MORE THOROUGH TESTING
def get_clusters(grid, checked):
    clusters = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # REVIEW Does scoring care about fruit type i.e. should we ignore 0?
            if not checked[i][j] and grid[i][j] != "*":
                new_cluster = find_cluster(grid, i, j, checked)
                clusters.append(new_cluster)
    return clusters


def find_cluster(grid, y, x, checked):
    target_value = grid[y][x]
    c = Cluster(target_value)
    checked[y][x] = True
    c.add_cell(y, x)
    neighbors = get_valid_neighbors(grid, target_value, y, x, checked)
    # Go through every valid neighbor to find the entirety of the cluster
    while neighbors:
        current = neighbors.pop(0)
        c.add_cell(current.y, current.x)
        checked[current.y][current.x] = True
        neighbors += get_valid_neighbors(
            grid, target_value, current.y, current.x, checked)

    return c


def get_valid_neighbors(grid, target_value, y, x, checked):
    neighbors = []
    # Up
    if y - 1 >= 0 and grid[y - 1][x] == target_value and not checked[y - 1][x]:
        neighbors.append(Neighbor(y - 1, x))
    # Down
    if y + 1 < len(grid) and grid[y + 1][x] == target_value and not checked[y + 1][x]:
        neighbors.append(Neighbor(y + 1, x))
    # Left
    if x - 1 >= 0 and grid[y][x - 1] == target_value and not checked[y][x - 1]:
        neighbors.append(Neighbor(y, x - 1))
    # Right
    if x + 1 < len(grid) and grid[y][x + 1] == target_value and not checked[y][x + 1]:
        neighbors.append(Neighbor(y, x + 1))

    return neighbors

# TODO Return board after selecting cluster i.e. removing cluster and applying gravity
def select_cluster(grid, cluster):
    pass


def init_checked_map(n):
    return np.array([np.array([False for x in range(n)]) for y in range(n)])


if __name__ == "__main__":
    IN_DIR = "tests/in/"
    n, p, t, grid = read_input(IN_DIR + "input_5.txt")
    printg(grid)
    checked = init_checked_map(len(grid))
    clusters = get_clusters(grid, checked)

    for clust in clusters:
        clust.display(grid)

'''

OUTPUT
1) Selected move as two characters:
    -> A-Z representing column number (A is leftmost)
    -> 1-26 (1 is top row)
2) nxn board after gravity has been applied
'''
