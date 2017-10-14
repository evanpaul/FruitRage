import time
import game
# time.process_time() # use this later; this is CPU time for process (NOT wall time)
INF = 99999999
CUT_DEPTH = 3


class Search_State:
    def __init__(self, grid, value=0, depth=0):
        self.grid = grid
        self._checked = game.init_checked_map(len(self.grid))
        self.actions = game.get_clusters(self.grid, self._checked)
        self.value = value
        self.depth = depth

    def results(self, action):
        return Search_State(game.apply_cluster(self.grid, action), action.score, depth=self.depth + 1)


def max_val(state, alpha=-INF, beta=INF):
    # print("[!] DEPTH =", state.depth)
    if cutoff_test(state, state.depth):
        return evaluate(state)
    v = -INF
    # print("At depth %d, I have %d options" % (state.depth, len(state.actions)))

    # print(list(map(lambda a: a.score, state.actions)))

    for act in state.actions:
        v = max(v, min_val(state.results(act), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_val(state,alpha=-INF, beta=INF):
    # print("[!] DEPTH =", state.depth)
    if cutoff_test(state, state.depth):
        return evaluate(state)
    v = INF
    for act in state.actions:
        v = min(v, max_val(state.results(act), alpha, beta))
        if v <= alpha:
            return v
        beta = max(beta, v)
    return v


def cutoff_test(state, depth):
    if depth == CUT_DEPTH:
        return True

def evaluate(state):
    return state.value

def minimax_decision(state):
    print("Best choice is worth:", max_val(state))


if __name__ == "__main__":
    IN_DIR = "tests/in/"
    n, p, t, grid = game.read_input(IN_DIR + "input_5.txt")
    # game.init_checked_map()
    root = Search_State(grid)
    start=time.process_time()
    minimax_decision(root)
    end=time.process_time()
    print("Elapsed:", end-start)
