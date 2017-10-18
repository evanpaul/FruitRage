import time
import game
import math

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


def max_val(state):
    global PRUNED, ALPHA, BETAM

    if cutoff_test(state, state.depth):
        return evaluate(state)

    v = -INF
    # BRANCH_SUM += len(state.actions)
    # BRANCH_NUM += 1
    for act in state.actions:
        result = max(v, min_val(state.results(act, maxFlag=True)))
        v = result

        if PRUNE_FLAG and v >= BETA:
            PRUNED += 1
            return v

        ALPHA = max(ALPHA, v)
    return v


def min_val(state):
    global PRUNED, ALPHA, BETA

    if cutoff_test(state, state.depth):
        return evaluate(state)

    v = INF
    # BRANCH_SUM += len(state.actions)
    # BRANCH_NUM += 1
    for act in state.actions:
        result = min(v, max_val(state.results(
            act, maxFlag=False)))
        v = result

        if PRUNE_FLAG and v <= ALPHA:
            PRUNED += 1
            return v

        BETA = max(BETA, v)
    return v


def cutoff_test(state, depth):
    if depth >= CUT_DEPTH or not state.actions:
        return True


def evaluate(state):
    return state.value


def minimax_decision(state):
    global ALPHA, BETA
    # print("Best choice is worth:", max_val(state))
    maximum = -INF
    best_action = None
    print(list(map(lambda c: c.score, state.actions)))

    # BRANCH_SUM += len(state.actions)
    # BRANCH_NUM += 1
    for act in state.actions:
        child_node = state.results(act, maxFlag=True)
        v = min_val(child_node)

        if v > maximum:
            maximum = v
            best_action = act

    state.selected_cluster = best_action
    # state.show_choice()
    state.apply_choice()

    if state.selected_cluster:
        return state.selected_cluster.score
    else:
        return 0
    # print(best_action._display(state.grid))
# def minimax_decision(state):
#     print(max_val(state).v)


def calibrate(test_grid):
    global INF, CUT_DEPTH, PRUNED, NODES, ALPHA, BETA, PRUNE_FLAG
    PRUNE_FLAG = False
    INF = 99999
    ALPHA = -INF
    BETA = INF
    CUT_DEPTH = 2
    PRUNED = NODES = 0


    n = len(test_grid)
    p = 3
    while CUT_DEPTH <= 3:
        NODES = 0
        print("[!] Searching until depth of", CUT_DEPTH)

        root = Search_State(test_grid)
        start = time.process_time()
        score = minimax_decision(root)
        end = time.process_time()

        time_elapsed = end - start
        nps = float(NODES)/time_elapsed
        rough_guess_branching = 0.5 * n * p
        print("Nodes per second:", nps)
        CUT_DEPTH += 1

    possible_depth = math.log(nps * 300, rough_guess_branching)
    print("I could probably evaluate in 5 minutes up to", possible_depth)


def iterative_search(fname):
    global INF, CUT_DEPTH, PRUNED, NODES, ALPHA, BETA, BRANCH_NUM, BRANCH_SUM, PRUNE_FLAG
    PRUNE_FLAG = True
    INF = 99999
    ALPHA = -INF
    BETA = INF
    CUT_DEPTH = 1
    PRUNED = NODES = 0

    n, p, MAX_TIME, grid = game.read_input(fname)
    ALLOTTED_T = MAX_TIME / 2  # !
    START_T = now = time.process_time()
    print("[!] Allotted:", ALLOTTED_T)
    while now - START_T < ALLOTTED_T:
        BRANCH_SUM = BRANCH_NUM = 0.0
        NODES = 0
        print("[!] Searching until depth of", CUT_DEPTH)

        root = Search_State(grid)
        start = time.process_time()
        score = minimax_decision(root)
        end = time.process_time()
        now = time.process_time()
        used = now - START_T
        rough_guess_branching = 0.5 * n * p
        print("-------------------------")
        print("Local time elapsed:", end - start)
        print("Paths pruned:", PRUNED)
        print("States considered:", NODES)
        print("Allotted time used: %f/%f" % (used, ALLOTTED_T))
        print("Average branching factor=", BRANCH_SUM / BRANCH_NUM)
        print("Branching guess  guess: 0.5 * np=", rough_guess_branching)
        print("depth guess:", int(round(math.log(NODES, rough_guess_branching))))
        CUT_DEPTH += 1
        # TODO REMOVE
        if CUT_DEPTH == 5:
            break
    return score


if __name__ == "__main__":
    IN_DIR = "samples/in/"
    iterative_search(IN_DIR + "input_large_binary.txt")
