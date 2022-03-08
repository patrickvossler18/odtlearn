def get_node_status(grb_model, b, w, p, n):
    """
    This function give the status of a given node in a tree. By status we mean whether the node
        1- is pruned? i.e., we have made a prediction at one of its ancestors
        2- is a branching node? If yes, what feature do we branch on
        3- is a leaf? If yes, what is the prediction at this node?
    Parameters
    ----------
    grb_model :
        The gurobi model solved to optimality (or reached to the time limit).
    b :
        The values of branching decision variable b.
    w :
        The values of prediction decision variable w.
    p :
        The values of decision variable p
    n :
        A valid node index in the tree
    Returns
    -------
    pruned : int
        pruned=1 iff the node is pruned
    branching : int
        branching = 1 iff the node branches at some feature f
    selected_feature : str
        The feature that the node branch on
    leaf : int
        leaf = 1 iff node n is a leaf in the tree
    value :  double
        if node n is a leaf, value represent the prediction at this node
    """

    pruned = False
    branching = False
    leaf = False
    value = None
    selected_feature = None

    p_sum = 0
    for m in grb_model.tree.get_ancestors(n):
        p_sum = p_sum + p[m]
    if p[n] > 0.5:  # leaf
        leaf = True
        for k in grb_model.treatments_set:
            if w[n, k] > 0.5:
                value = k
    elif p_sum == 1:  # Pruned
        pruned = True

    if n in grb_model.tree.Nodes:
        if (pruned is False) and (leaf is False):  # branching
            for f in grb_model.X_col_labels:
                if b[n, f] > 0.5:
                    selected_feature = f
                    branching = True

    return pruned, branching, selected_feature, leaf, value


def print_tree(grb_model, b, w, p):
    """
    This function print the derived tree with the branching features and the predictions asserted for each node
    Parameters
    ----------
    grb_model :
        The gurobi model solved to optimality (or reached the time limit)
    b :
        The values of branching decision variable b
    w :
        The values of prediction decision variable w
    p :
        The values of decision variable p
    Returns
    -------
    Print out the tree in the console
    """
    for n in grb_model.tree.Nodes + grb_model.tree.Leaves:
        pruned, branching, selected_feature, leaf, value = get_node_status(
            grb_model, b, w, p, n
        )
        print("#########node ", n)
        if pruned:
            print("pruned")
        elif branching:
            print("branch on {}".format(selected_feature))
        elif leaf:
            print("leaf {}".format(value))