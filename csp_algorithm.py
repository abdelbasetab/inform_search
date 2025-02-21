class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        """
        Initializes a CSP instance.
        
        variables: a list of variable names.
        domains: a dict mapping each variable to a list of possible values.
        neighbors: a dict mapping each variable to a list of other variables that share a constraint.
        constraint: a function f(var1, value1, var2, value2) -> bool that returns True if the assignment 
                    between var1 and var2 does not violate the constraint.
        """
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint = constraint

    def is_consistent(self, var, value, assignment):
        """
        Checks whether assigning 'value' to 'var' is consistent with the current assignment.
        """
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if not self.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True


def backtracking_search(csp):
    """
    Performs backtracking search to find a solution for the given CSP.
    """
    return backtrack({}, csp)


def backtrack(assignment, csp):
    # If every variable has been assigned, return the assignment as the solution.
    if len(assignment) == len(csp.variables):
        return assignment

    # Select an unassigned variable (here, simply the first one found).
    unassigned = [v for v in csp.variables if v not in assignment]
    var = unassigned[0]

    # Try every value in the domain of the variable.
    for value in csp.domains[var]:
        if csp.is_consistent(var, value, assignment):
            # Tentatively assign the value.
            assignment[var] = value

            # Recursively continue with this assignment.
            result = backtrack(assignment, csp)
            if result is not None:
                return result

            # If the assignment did not lead to a solution, backtrack.
            del assignment[var]

    # No valid assignment found for this branch.
    return None


# Example: Map Coloring Problem for Australia
if __name__ == '__main__':
    # Variables represent the regions.
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

    # Each region can be colored with one of three colors.
    domains = {
        'WA': ['red', 'green', 'blue'],
        'NT': ['red', 'green', 'blue'],
        'SA': ['red', 'green', 'blue'],
        'Q':  ['red', 'green', 'blue'],
        'NSW':['red', 'green', 'blue'],
        'V':  ['red', 'green', 'blue'],
        'T':  ['red', 'green', 'blue']
    }

    # Neighbors indicate which regions are adjacent (and hence must have different colors).
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q':  ['NT', 'SA', 'NSW'],
        'NSW':['SA', 'Q', 'V'],
        'V':  ['SA', 'NSW', 'T'],
        'T':  ['V']
    }

    # The constraint function: neighboring regions must have different colors.
    def different_values_constraint(var1, value1, var2, value2):
        return value1 != value2

    # Create a CSP instance.
    csp_instance = CSP(variables, domains, neighbors, different_values_constraint)

    # Solve the CSP using backtracking search.
    solution = backtracking_search(csp_instance)
    if solution:
        print("Solution found:")
        for var in variables:
            print(f"{var}: {solution[var]}")
    else:
        print("No solution found.")
