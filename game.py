import numpy as np
import copy
import itertools
import time

class Cluster:
    def __init__(self, fruit_type, coord_string):
        self.fruit_type = fruit_type
        self.cells = []
        self.score = 0
        self.affected_col_indices = set()
        self.coord_string = coord_string

    def add_cell(self, y, x):
        self.cells.append((y, x))
        self.affected_col_indices.add(x)

    def _display(self, grid):  # For debugging
        g = copy.deepcopy(grid)
        for c in self.cells:
            g[c[0]][c[1]] = "X"

        printg(g)
        print("[!] Selected:", self.coord_string)
        print("[!] Fruit gathered: %d" % (self.score))

    def calculate_score(self):
        # YIKES this is only calculated at the END
        # So really what matters is total number of fruit, not fruit per turn

        self.score = len(self.cells) # ** 2


class Neighbor:
    def __init__(self, y, x):
        self.y = y
        self.x = x


def read_input(fname):  # -> n, p, t, board
    '''Input lines format:
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

def save_output(grid, coord):
    with open("output.txt", "w") as f:
        f.write(coord + "\n")

        for row in grid:
            for cell in row:
                f.write(cell)
            f.write("\n")

def save_alternate_output(grid, coord):
    with open("output.txt", "w") as f:
        f.write(str(len(grid)) + "\n")
        f.write("9\n")
        f.write("30.0\n")

        for row in grid:
            for cell in row:
                f.write(cell)
            f.write("\n")




def printg(grid):
    '''Pretty print grid'''
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
    '''Convert coordinate to grid notation e.g. (0, 0) to A1'''
    assert 0 <= y <= 26 and 0 <= x <= 26, "Invalid coordinates"
    col = chr(65 + x)
    row = y + 1
    coord = "" + col + str(row)
    return coord


def coord_to_indices(coord_string):
    '''Convert grid notation to coordinate e.g. A1 to (0, 0)'''
    assert type(coord_string) == "str" and len(coord_string) == 2, "Invalid coordinate string"
    col = ord(coord_string[1]) - 65
    row = int(coord_string[2]) - 1


def get_score_of_best_cluster(grid):
    clusters = get_clusters(grid)
    if clusters:
        return clusters[0].score
    else:
        return 0

def get_clusters(grid):
    '''Search grid for all possible groups of fruits i.e. fruit clusters

    Uses a boolean table (checked) to ensure no fruit is added to more than one
    cluster
    '''
    checked = init_checked_map(len(grid))
    clusters = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if not checked[i][j] and grid[i][j] != "*":
                new_cluster = find_cluster(grid, i, j, checked)
                clusters.append(new_cluster)



    # I don't see any reason a single fruit should be selected unless it's the
    # only option. There's a larger problem with the agents tendency to choose
    # low values at even depths.

    good_choices = False
    # REVIEW: Is this a bad idea?
    for cl in clusters:
        if cl.score > 1:
            good_choices = True

    if good_choices:
        # print("[!] Removing single clusters")
        clusters = list(filter(lambda c: c.score > 1, clusters))
    # else:
    #     print("[!] Better choices don't exist!")



    return sorted(clusters, reverse=True,key=lambda c: c.score)



def find_cluster(grid, y, x, checked):
    '''Finds the entirety of a cluster

    Given the coordinate of a fruit that has not yet been assigned to a cluster,
    a full cluster is returned after fully searching all of its neighbors. The
    score of the cluster is calculated at the end such that:
    cluster.score = (# of fruit in cluster)^2
    '''
    fruit_type = grid[y][x]
    clust = Cluster(fruit_type, indices_to_coord(y, x))
    checked[y][x] = True
    clust.add_cell(y, x)
    # print(checked)
    neighbors = get_valid_neighbors(grid, fruit_type, y, x, checked)
    # Go through every valid neighbor to find the entirety of the cluster
    while neighbors:
        current = neighbors.pop(0)
        clust.add_cell(current.y, current.x)
        checked[current.y][current.x] = True
        neighbors += get_valid_neighbors(
            grid, fruit_type, current.y, current.x, checked)
    clust.calculate_score()  # Determine how much this cluster is worth

    return clust


def get_valid_neighbors(grid, fruit_type, y, x, checked):
    '''Finds the valid neighbors of a unassigned fruit

    Every valid (i.e. existant and unassigned), non-diagonal direction is checked.
    Fruit of matching type adhering to these restrictions are returned in a list
    that is further searched in a FIFO fashion by find_cluster()
    '''
    neighbors = []
    # Up
    if y - 1 >= 0 and grid[y - 1][x] == fruit_type and not checked[y - 1][x]:
        checked[y - 1][x] = True
        neighbors.append(Neighbor(y - 1, x))
    # Down
    if y + 1 < len(grid) and grid[y + 1][x] == fruit_type and not checked[y + 1][x]:
        checked[y + 1][x] = True
        neighbors.append(Neighbor(y + 1, x))
    # Left
    if x - 1 >= 0 and grid[y][x - 1] == fruit_type and not checked[y][x - 1]:
        checked[y][x - 1] = True
        neighbors.append(Neighbor(y, x - 1))
    # Right
    if x + 1 < len(grid) and grid[y][x + 1] == fruit_type and not checked[y][x + 1]:
        checked[y][x + 1] = True
        neighbors.append(Neighbor(y, x + 1))

    return neighbors


def apply_cluster(old_grid, cluster):
    '''Remove a cluster from the grid and apply gravity'''
    grid = copy.deepcopy(old_grid)
    # Remove fruit cluster from grid
    for coord in cluster.cells:
        grid[coord[0]][coord[1]] = "*"

    # print("[!] Selecting cluster of type %s and size %d" %
    #       (cluster.fruit_type, len(cluster.cells)))
    # cluster._display(grid)
    # Apply gravity column by column
    for column in cluster.affected_col_indices:
        swap = False
        y = len(grid) - 1
        # Start from the bottom and swap empty cells with non-empty to apply gravity
        while y >= 0:
            if grid[y][column] == "*" and not swap:
                if y == 0:
                    break
                swap = True
                peak = (y, column)

            elif grid[y][column] != "*" and swap:
                # Swap
                grid[peak[0]][peak[1]] = grid[y][column]
                grid[y][column] = "*"
                swap = False
                y = peak[0]

            y -= 1
    return grid


def init_checked_map(n):
    '''Initialize a boolean table to track cluster assignments'''
    return np.array([np.array([False for x in range(n)]) for y in range(n)])




if __name__ == "__main__":
    IN_DIR = "tests/in/"
    n, p, t, grid = read_input(IN_DIR + "input_blank.txt")

    clusters = get_clusters(grid)
    print(len(clusters))
    # empty = False
    #
    # i = first = second = 0
    # while not empty:
    #     i += 1
    #
    #     checked = init_checked_map(len(grid))
    #     clusters = get_clusters(grid, checked)
    #     descending_score_clusters = sorted(
    #         clusters, key=lambda c: c.score, reverse=True)
    #     print("\n[BEFORE]")
    #     printg(grid)
    #     best_cluster = descending_score_clusters[0]
    #     grid = apply_cluster(grid, best_cluster)
    #     print("[ClUSTER REMOVED AND GRAVITY APPLIED]")
    #     printg(grid)
    #
    #     if i % 2 != 0:
    #         first += best_cluster.score
    #     else:
    #         second += best_cluster.score
    #
    #     empty = True
    #     for cell in list(itertools.chain.from_iterable(grid)):
    #         if cell != "*":
    #             empty = False
    #             break
    # print("[FINAL SCORES]")
    # print("First player:", first)
    # print("Second player", second)

'''

OUTPUT
1) Selected move as two characters:
    -> A-Z representing column number (A is leftmost)
    -> 1-26 (1 is top row)
2) nxn board after gravity has been applied
'''
