import time
import game
# time.process_time() # use this later; this is CPU time for process (NOT
# wall time)
INF = 99999
CUT_DEPTH = 3
PRUNED = 0
# REVIEW Low depths not pruning?

# TODO:
# Better eval (consider the state of the board WITHOUT calling get_clusters)
# Killer heuristic


class Search_State:
    def __init__(self, grid, value=0, depth=0):
        self.grid = grid
        self.actions = game.get_clusters(self.grid)
        self.value = value
        self.depth = depth
        self.selected_cluster = None

    def results(self, action, maxFlag):
        global NODES
        NODES += 1
        # An action is a Cluster
        if maxFlag:
            # print("old(max)=>", self.value)
            new_score = self.value + action.score
            # print("new(max)=>", new_score)
        else:
            # print("old(min)=>", self.value)
            new_score = self.value - action.score
            # print("new(min)=>", new_score)

        return Search_State(game.apply_cluster(self.grid, action), value=new_score, depth=self.depth + 1)

    def show_choice(self):
        if not self.selected_cluster:
            print("No best action determined!")
            return False

        self.selected_cluster._display(self.grid)

    def apply_choice(self):
        if not self.selected_cluster:
            print("No best action determined!")
            return False

        game.save_output(game.apply_cluster(
            self.grid, self.selected_cluster), self.selected_cluster.coord_string)


def max_val(state, alpha=-INF, beta=INF):
    global PRUNED

    if cutoff_test(state, state.depth):
        return evaluate(state)

    v = -INF
    for act in state.actions:
        result = max(v, min_val(state.results(act, maxFlag=True), alpha, beta))
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
        result = min(v, max_val(state.results(
            act, maxFlag=False), alpha, beta))
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
    return state.value


def minimax_decision(state):
    # print("Best choice is worth:", max_val(state))
    maximum = -INF
    best_action = None
    print(list(map(lambda c: c.score, state.actions)))

    for act in state.actions:
        child_node = state.results(act, maxFlag=True)
        v = min_val(child_node)

        if v > maximum:
            maximum = v
            best_action = act

    state.selected_cluster = best_action
    state.show_choice()
    state.apply_choice()


if __name__ == "__main__":
    n, p, MAX_TIME, grid = game.read_input("input.txt")
    NODES = 0

    root = Search_State(grid)
    print("[!] Searching until depth of", CUT_DEPTH)
    minimax_decision(root)
