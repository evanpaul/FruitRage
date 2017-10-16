import time
import game
# time.process_time() # use this later; this is CPU time for process (NOT
# wall time)
INF = 99999
CUT_DEPTH = 3
# DEBUG = [[] for x in range(CUT_DEPTH + 1)]
# REVIEW Depth%2==0 always selects worst option ???
# Either there's a bug OR we need to strongly disincentivize small clusters
# "Setting yourself up" might work for the minimax agent
# but definitely not for the random agent
PRUNED = 0
# Low depths not pruning?


class Search_State:
    def __init__(self, grid, value=0, depth=0):
        self.grid = grid
        self._checked = game.init_checked_map(len(self.grid))
        self.actions = game.get_clusters(self.grid, self._checked)
        self.value = value
        self.depth = depth
        self.selected_action = None

    def results(self, action):
        return Search_State(game.apply_cluster(self.grid, action), action.score, depth=self.depth + 1)

class O: # TODO Rename
    def __init__(self):
        self.v = 0
        self.action = None

def max_val(state, alpha=-INF, beta=INF):
    global PRUNED

    # DEBUG[state.depth].append(state.value)
    obj = O()
    if cutoff_test(state, state.depth) or not state.actions:
        obj.v = evaluate(state)
        return obj

    obj.v = -INF
    for act in state.actions:
        result = max(obj.v, min_val(state.results(act), alpha, beta).v)

        if result != obj.v:  # REVIEW Old value updated, do we care about this in min?
            obj.action = act

        obj.v = result

        if obj.v >= beta:
            PRUNED += 1
            return obj

        alpha = max(alpha, obj.v)
    return obj



def min_val(state, alpha=-INF, beta=INF):
    global PRUNED
    # print("[!] DEPTH =", state.depth)
    # if state.value > 1:
    # DEBUG[state.depth].append(state.value)
    obj = O()
    if cutoff_test(state, state.depth) or not state.actions:
        obj.v = evaluate(state)
        return obj

    obj.v = INF
    for act in state.actions:
        result = min( obj.v, max_val(state.results(act), alpha, beta).v)

        if result != obj.v:
            obj.action = act
        obj.v = result

        if obj.v <= alpha:
            PRUNED += 1
            return obj

        beta = max(beta, obj.v)
    return obj


def cutoff_test(state, depth):
    if depth >= CUT_DEPTH:
        return True


def evaluate(state):
    # TODO Heuristic
    return state.value



def minimax_decision(state):
    # print("Best choice is worth:", max_val(state))
    maximum = -INF
    best_action = None
    # print(list(map(lambda c: c.score, state.actions)))

    for act in state.actions:
        child_node = state.results(act)

        result_obj = min_val(child_node)

        if result_obj.v > maximum:
            maximum = result_obj.v
            best_action = result_obj.action



    return maximum

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
    print("Result:", minimax_decision(root))
    end = time.process_time()
    print("Elapsed:", end - start)
    print("Paths pruned:", PRUNED)
    # for level in DEBUG:
    #     print(level)
