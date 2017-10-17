import time
import game
# time.process_time() # use this later; this is CPU time for process (NOT
# wall time)

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

        game.save_alternate_output(game.apply_cluster(
            self.grid, self.selected_cluster), self.selected_cluster.coord_string)


def max_val(state, alpha, beta):
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


def min_val(state, alpha, beta):
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
        v = min_val(child_node, -INF, INF)

        if v > maximum:
            maximum = v
            best_action = act

    state.selected_cluster = best_action
    state.show_choice()
    state.apply_choice()

    if state.selected_cluster:
        return state.selected_cluster.score
    else:
        return 0
    # print(best_action._display(state.grid))
# def minimax_decision(state):
#     print(max_val(state).v)
def iterative(fname):
    global INF, CUT_DEPTH, PRUNED, NODES
    INF = 99999
    CUT_DEPTH = 1
    PRUNED = NODES = 0

    n, p, MAX_TIME, grid = game.read_input(fname)
    ALLOTTED_T = MAX_TIME/2  # !
    START_T = now = time.process_time()
    print("[!] Allotted:", ALLOTTED_T)

    while now - START_T < ALLOTTED_T:
        NODES = 0
        print("[!] Searching until depth of", CUT_DEPTH)

        root = Search_State(grid)
        start = time.process_time()
        score = minimax_decision(root)
        end = time.process_time()
        now = time.process_time()
        used = now - START_T

        print("-------------------------")
        print("Local time elapsed:", end - start)
        print("Paths pruned:", PRUNED)
        print("States considered:", NODES)
        print("Allotted time used: %f/%f" % (used, ALLOTTED_T))

        CUT_DEPTH += 1
        # TODO REMOVE
        if CUT_DEPTH == 5:
            break
    return score

if __name__ == "__main__":
    IN_DIR = "samples/in/"
    iterative(IN_DIR + "input_5.txt")
