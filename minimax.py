import time
# time.process_time() # use this later; this is CPU time for process (NOT wall time)
INF = 9999999

# max/min_val return utility values
def max_val(state, alpha, beta):
    if cutoff_test(state, depth):
        return evaluate(state)
    v = -INF
    for each act in actions(state):
        v = max(v, min_val(results(state, act), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_val(state, alpha, beta):
    if cutoff_test(state, depth):
        return evaluate(state)
    v = INF
    for each act in actions(state):
        v = min(v, max_val(results(state, act), alpha, beta))
        if v <= alpha:
            return v
        beta = max(beta, v)
    return v

# REVIEW Might make more sense to have depth global
def cutoff_test(state, depth):
    pass


def evaluate(state):
    pass
