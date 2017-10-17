import time
import game
# time.process_time() # use this later; this is CPU time for process (NOT
# wall time)
INF = 99999
CUT_DEPTH = 2
PRUNED = 0
# REVIEW Low depths not pruning?


class Search_State:
    def __init__(self, grid, value=0, depth=0):
        self.grid = grid
        self.actions = game.get_clusters(self.grid)
        self.value = value
        self.depth = depth
        self.selected_cluster = None

    def results(self, action):
        return Search_State(game.apply_cluster(self.grid, action), action.score, depth=self.depth + 1)

    def show_choice(self):
        if not self.selected_cluster:
            print("No best action determined!")
            return False

        self.selected_cluster._display(self.grid)

    def apply_choice(self):
        if not self.selected_cluster:
            print("No best action determined!")
            return False

        game.save_output(game.apply_cluster(self.grid, self.selected_cluster), self.selected_cluster.coord_string)


def max_val(state, alpha=-INF, beta=INF):
    global PRUNED

    if cutoff_test(state, state.depth):
        return evaluate(state)

    v = -INF
    for act in state.actions:
        result = max(v, min_val(state.results(act), alpha, beta))
        v = result

        if v >= beta:
            PRUNED += 1
            return v

        alpha = max(alpha, v)
    return v


def min_val(state, alpha=-INF, beta=INF):
    global PRUNED

    if cutoff_test(state, state.depth):
        return evaluate(state)

    v = INF
    for act in state.actions:
        result = min(v, max_val(state.results(act), alpha, beta))
        v = result

        if v <= alpha:
            PRUNED += 1
            return v

        beta = max(beta, v)
    return v


def cutoff_test(state, depth):
    if depth >= CUT_DEPTH or not state.actions:
        return True


def evaluate(state):
    # TODO Heuristic
    return game.get_score_of_best_cluster(state.grid)


def minimax_decision(state):
    # print("Best choice is worth:", max_val(state))
    maximum = -INF
    best_action = None
    print(list(map(lambda c: c.score, state.actions)))

    for act in state.actions:
        child_node = state.results(act)
        v = min_val(child_node)

        if v > maximum:
            maximum = v
            best_action = act

    state.selected_cluster = best_action
    state.show_choice()
    state.apply_choice()

    # print(best_action._display(state.grid))
# def minimax_decision(state):
#     print(max_val(state).v)


if __name__ == "__main__":
    IN_DIR = "samples/in/"
    n, p, t, grid = game.read_input(IN_DIR + "input_5.txt")
    print("Searching until depth of", CUT_DEPTH)

    # game.init_checked_map()
    root = Search_State(grid)
    start = time.process_time()
    minimax_decision(root)
    end = time.process_time()
    print("Elapsed:", end - start)
    print("Paths pruned:", PRUNED)
    # for level in DEBUG:
    #     print(level)
