import pulp_pack as lp

def optimal_finder(user_input: int, max_min: str, obj_coeff: dict, constraint_coefficients: dict, ineq: dict, rhs: dict):
    # Create a linear programming problem
    model = lp.LpProblem("Linear_Programming_Problem", lp.LpMaximize if max_min == "Max" else lp.LpMinimize)

    # Create variables
    x = lp.LpVariable("x", lowBound=0, cat=lp.LpInteger)
    y = lp.LpVariable("y", lowBound=0, cat=lp.LpInteger)

    # Set objective function
    model += eval(obj_coeff[f'co_1'].text) * x + eval(obj_coeff[f'co_2'].text) * y, "Objective"

    # Add constraints
    for row in range(user_input):
        lhs = eval(constraint_coefficients[f'constraint_{row+1}_1'].text) * x + eval(constraint_coefficients[f'constraint_{row+1}_2'].text) * y
        if ineq[f'inequal_{row+1}'].text == "≤":
            model += lhs <= eval(rhs[f'rhs_{row+1}'].text), f"Constraint_{row+1}"
        else:
            model += lhs >= eval(rhs[f'rhs_{row+1}'].text), f"Constraint_{row+1}"

    # Solve the problem
    model.solve(lp.PULP_CBC_CMD(fracGap=0.001))

    if model.status == lp.LpStatusOptimal:
        sol_dict = {}
        for variable in model.variables():
            sol_dict[variable.name] = variable.varValue

        sol_dict['optimum'] = lp.value(model.objective)
        return sol_dict, model
    else:
        return {}, model

