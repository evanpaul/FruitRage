import minimax

if __name__ == "__main__":
    target = "samples/in/input_large.txt"
    p1_score = p2_score = 0

    while True:
        # Player 1
        print("[PLAYER 1]")
        p1_new = minimax.iterative_search(target)
        p1_score += p1_new
        target = "output.txt"
        print("[PLAYER 2]")
        p2_new = minimax.iterative_search(target)
        p2_score += p2_new

        if p1_new == 0 or p2_new == 0:
            print(p1_new, p2_new)
            break
    print("P1:%d, P2:%d" % (p1_score, p2_score))
