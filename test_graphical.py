import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, latex



def graphical_method_plotter(user_input:int,constraint_coefficients:dict,inequal_inputs:dict,rhs_inputs:dict):
    # Collect number of constraints from user
    constraints = []
    for row in range(user_input):
        constraint_i = f"{constraint_coefficients[f'constraint_{row+1}_{1}'].text}*x + {constraint_coefficients[f'constraint_{row+1}_{2}'].text}*y {inequal_inputs[f'inequal_{row+1}'].text} {rhs_inputs[f'rhs_{row+1}'].text}"
        if "≤" in constraint_i:
            constraint_i=constraint_i.replace("≤","<=")
        else:
            constraint_i=constraint_i.replace("≥",">=")
        constraints.append(constraint_i)


    # Find the maximum value in the constraints
    x_max_possible = []
    y_max_possible = []

    x,y = symbols('x y')
    for constraint in constraints:
        if "<=" in constraint:
            eq,rhs_c=constraint.split("<=")
            rhs_c = rhs_c.strip()
            equat = Eq(eval(eq),int(rhs_c))
        else:
            eq,rhs_c=constraint.split(">=")
            rhs_c = rhs_c.strip()
            equat = Eq(eval(eq),int(rhs_c))
        solution_x = solve(equat.subs(y,0),x)
        solution_y=solve(equat.subs(x,0),y)
        x_max_possible.extend(solution_x)
        y_max_possible.extend(solution_y)
    max_x =int(max(x_max_possible))+1
    max_y = int(max(y_max_possible))+1
    
    
    # Generate gridlines for plotting
    gridline_x = np.linspace(-2, abs(max_x), 500)
    gridline_y = np.linspace(-2, abs(max_y), 500)
    x, y = np.meshgrid(gridline_x, gridline_y)

    # Initialize the feasible region
    feasible_region = True

    # Check feasibility of each constraint
    for i in constraints:
        feasible_region &= eval(i)

    # Plot the feasible region
    plt.imshow(feasible_region, extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)

    # Generate x values for plotting
    x_values = np.linspace(0, max_x, 2000)

    # Plot each individual constraint
    for i in range(user_input):
        equation_str = constraints[i]
        if "<=" in equation_str:
            equation_str = equation_str.replace("<=", "=")
        elif ">=" in equation_str:
            equation_str = equation_str.replace(">=", "=")
        try:
            x, y = symbols('x y')
            lhs, rhs = equation_str.split("=")
            first_var = lhs.split("+")[0].strip()
            first_var_coeff = int(first_var.replace("*x",""))
            lhs_expr = eval(lhs.strip())
            rhs_expr = eval(rhs.strip())
            equation = Eq(lhs_expr, rhs_expr)
            label = f'${latex(equation)}$'
            solution = solve(equation, y)
            equation_in_terms_of_y = solution[0]
            y_values = [eval(str(equation_in_terms_of_y)) for x in x_values]
            plt.plot(x_values, y_values, label=label)
        except IndexError:
            plt.plot(float(eval(str(rhs_expr))/(first_var_coeff))* np.ones_like(x_values), np.linspace(0,abs(max_y),2000),label = label)

    # Set the plot limits and labels
    plt.xlim(0, abs(max_x))
    plt.ylim(0, abs(max_y))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    
