import copy
import heapq

from mip import ConstrsGenerator, Model

from odtlearn.utils.callback_helpers import (
    get_all_terminal_paths,
    get_cut_expression,
    get_cut_integer,
    get_nominal_path,
    shortest_path_solver,
)


def benders_subproblem(main_model_obj, b, p, w, i):
    label_i = main_model_obj._y[i]
    current = 1
    right = []
    left = []
    target = []
    subproblem_value = 0

    while True:
        (
            _,
            branching,
            selected_feature,
            _,
            terminal,
            _,
        ) = main_model_obj._get_node_status(b, w, p, current)
        if terminal:
            target.append(current)
            if current in main_model_obj._tree.Nodes:
                left.append(current)
                right.append(current)
            if w[current, label_i] > 0.5:
                subproblem_value = 1
            break
        elif branching:
            if (
                main_model_obj._X.at[i, selected_feature] == 1
            ):  # going right on the branch
                left.append(current)
                target.append(current)
                current = main_model_obj._tree.get_right_children(current)
            else:  # going left on the branch
                right.append(current)
                target.append(current)
                current = main_model_obj._tree.get_left_children(current)

    return subproblem_value, left, right, target


class BendersCallback(ConstrsGenerator):
    """
    This class contains a function that is called by the sovler at
    every node through the branch-&-bound tree while we solve the model.

    We are specifically interested at nodes
    where we get an integer solution for the master problem.
    When we get an integer solution for b and p, for every data-point we solve
    the sub-problem which is a minimum cut and check if g[i] <= value of
    sub-problem[i]. If this is violated we add the corresponding benders
    constraint as lazy constraint to the master problem and proceed.
    Whenever we have no violated constraint, it means that we have found
    the optimal solution.

    """

    def __init__(self, X, obj, solver, **kwargs):
        self.X = X
        self.obj = obj
        self.solver = solver
        self.g = kwargs.get("g")
        self.p = kwargs.get("p")
        self.b = kwargs.get("b")
        self.w = kwargs.get("w")

    def generate_constrs(self, model: Model, depth: int = 0, npass: int = 0):
        g_trans, p_trans, b_trans, w_trans = (
            {k: model.translate(v).x for k, v in self.g.items()},
            {k: model.translate(v).x for k, v in self.p.items()},
            {k: model.translate(v).x for k, v in self.b.items()},
            {k: model.translate(v).x for k, v in self.w.items()},
        )

        for i in self.X.index:
            g_threshold = 0.5
            if g_trans[i] > g_threshold:
                subproblem_value, left, right, target = benders_subproblem(
                    self.obj, b_trans, p_trans, w_trans, i
                )
                if subproblem_value == 0:
                    lhs = get_cut_integer(
                        self.solver,
                        self.obj,
                        left,
                        right,
                        target,
                        i,
                    )
                    # print(lhs)
                    new_constr = lhs
                    new_constr.sense = "<"
                    model += new_constr


def robust_tree_subproblem(
    master,
    i,
    terminal_nodes,
    terminal_path_dict,
    terminal_features_dict,
    terminal_assignments_dict,
    terminal_cutoffs_dict,
    initial_xi={},
    initial_mins={},
    initial_maxes={},
):
    label_i = master._y[i]
    target = []  # list of nodes whose edge to the sink is part of the min cut

    # Solve shortest path problem via DFS w/ pruning
    target, cost, xi, v = shortest_path_solver(
        master,
        i,
        label_i,
        terminal_nodes,
        terminal_path_dict,
        terminal_features_dict,
        terminal_assignments_dict,
        terminal_cutoffs_dict,
        initial_xi,
        initial_mins,
        initial_maxes,
    )

    return target, xi, cost, v


class RobustBendersCallback(ConstrsGenerator):
    """
    This class contains the functioncalled by the solver at every node through
    the branch-&-bound tree while we solve the model.
    We are specifically interested at nodes where we get an integer solution for the master problem.
    When we get an integer solution for b and p, for every datapoint we solve the subproblem
    which is a minimum cut and check if g[i] <= value of subproblem[i].
    If this is violated we add the corresponding benders constraint as lazy constraint to the master
    problem and proceed. Whenever we have no violated constraint, it means that we have found the optimal solution.
    """

    def __init__(self, X, obj, solver, **kwargs):
        self.X = X
        self.obj = obj
        self.solver = solver
        self.b = kwargs.get("b")
        self.w = kwargs.get("w")
        self.t = kwargs.get("t")

    def generate_constrs(self, model: Model, depth: int = 0, npass: int = 0):
        b_trans, w_trans, t_trans = (
            {k: model.translate(v).x for k, v in self.b.items()},
            {k: model.translate(v).x for k, v in self.w.items()},
            {k: model.translate(v).x for k, v in self.t.items()},
        )

        # Initialize a blank-slate xi
        initial_xi = {}
        for c in self.obj._solver.model._data["cat_features"]:
            initial_xi[c] = 0

        # Initialize dictionaries to store min and max values of each feature:
        initial_mins = {}
        initial_maxes = {}
        for c in self.obj._solver.model._data["cat_features"]:
            initial_mins[c] = self.obj._solver.model._data["min_values"][c]
            initial_maxes[c] = self.obj._solver.model._data["max_values"][c]

        whole_expr = self.solver.lin_expr(0)  # Constraint RHS expression
        priority_queue = []  # Stores elements of form (path_cost, index)
        path_dict = {}  # Stores all paths from shortest path problem
        xi_dict = (
            {}
        )  # Stores set of xi's from shortest path problem (feature perturbations)
        v_dict = (
            {}
        )  # Stores set of v's from shortest path problem (label perturbations)
        nom_path_dict = {}  # Stores set of nominal paths
        correct_points = []  # List of indices of nominally correctly classified points

        # Find nominal path for every data point
        for i in self.obj._solver.model._data["datapoints"]:
            nom_path, k = get_nominal_path(self.obj, b_trans, w_trans, i)
            if k != self.obj._y[i]:
                # Misclassified nominally - no need to check for shortest path
                curr_expr = get_cut_expression(
                    self.obj,
                    self.solver,
                    self.obj._X,
                    b_trans,
                    w_trans,
                    nom_path,
                    initial_xi,
                    False,
                    i,
                    self.obj._solver.model._data["f_theta_indices"],
                )
                whole_expr += curr_expr
                new_constr = self.obj._solver.model._data["t"][i] <= curr_expr
                model += new_constr
            else:
                # Correctly classified - put into pool of problems for shortest path
                correct_points += [i]
                nom_path_dict[i] = nom_path

        # Solve shortest path problem for every data point
        # Get all paths
        (
            terminal_nodes,
            terminal_path_dict,
            terminal_features_dict,
            terminal_assignments_dict,
            terminal_cutoffs_dict,
        ) = get_all_terminal_paths(self.obj, b_trans, w_trans)
        for i in correct_points:
            path, xi, cost, v = robust_tree_subproblem(
                self.obj,
                i,
                terminal_nodes,
                terminal_path_dict,
                terminal_features_dict,
                terminal_assignments_dict,
                terminal_cutoffs_dict,
                initial_xi=copy.deepcopy(initial_xi),
                initial_mins=copy.deepcopy(initial_mins),
                initial_maxes=copy.deepcopy(initial_maxes),
            )
            heapq.heappush(priority_queue, (cost, i))
            path_dict[i] = path
            xi_dict[i] = xi
            v_dict[i] = v

        # Add points that are misclassified to the constraint RHS
        total_cost = 0
        while True:
            if len(priority_queue) == 0:
                break

            # Get next least-cost point and see if still under epsilon budget
            current_point = heapq.heappop(priority_queue)
            curr_cost = current_point[0]
            if curr_cost + total_cost > self.obj._solver.model._data["epsilon"]:
                # Push point back into queue
                heapq.heappush(priority_queue, current_point)
                break
            # Add RHS expression for point if still under budget
            i = current_point[1]
            whole_expr += get_cut_expression(
                self.obj,
                self.solver,
                self.obj._X,
                b_trans,
                w_trans,
                path_dict[i],
                xi_dict[i],
                v_dict[i],
                i,
                self.obj._solver.model._data["f_theta_indices"],
            )
            total_cost += curr_cost

        added_cut = round(sum(t_trans)) > len(
            priority_queue
        )  # current sum of t is larger than RHS -> violated constraint(s)
        if added_cut:
            while len(priority_queue) != 0:
                current_point = heapq.heappop(priority_queue)
                i = current_point[1]
                whole_expr += get_cut_expression(
                    self.obj,
                    self.solver,
                    self.obj._X,
                    b_trans,
                    w_trans,
                    nom_path_dict[i],
                    initial_xi,
                    False,
                    i,
                    self.obj._solver.model._data["f_theta_indices"],
                )
            new_constr = (
                self.solver.quicksum(
                    self.obj._solver.model._data["t"][i]
                    for i in self.obj._solver.model._data["datapoints"]
                )
                <= whole_expr
            )
            model += new_constr
