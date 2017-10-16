import game
# indices_to_coord(y, x)
# coord_to_indices(coord_string)
# get_clusters(grid, checked)
# find_cluster(grid, y, x, checked)
# get_valid_neighbors(grid, fruit_type, y, x, checked)
# apply_cluster(old_grid, cluster)

def test_indices_to_coord():
    #1
    y = x = 0
    assert game.indices_to_coord(y, x) == "A1"

    #2
    y = 9
    x = 5
    assert game.indices_to_coord(y, x) == "J10"

    #3
    failed = False
    try:
        y = x = -1
        game.indices_to_coord(y, x)
    except AssertionError:
        failed = True

    assert failed
