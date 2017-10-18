import numpy as np
import random
import time
import minimax
if __name__ == "__main__":
    grid = []
    for i in range(15):
        row = []
        for j in range(15):
            row.append(str(random.randint(0, 5)))
        row = np.array(row)
        grid.append(row)
    grid = np.array(grid)

    minimax.calibrate(grid)
