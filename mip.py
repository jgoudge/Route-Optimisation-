
def optimize_mip(input_file, output_file, model_file=""):
    """
    Solve the route-optimization problem using a (mixed-)integer programming
    formulation and Gurobi.

    Parameters
    ----------
    input_file : 
        Path to an existing input file describing the instance to be solved.
        The format follows the specification provided for the assignment.
    
    output_file : 
        Path to the location where the solution file will be written.
        The function will create or overwrite this file with the computed solution.
    
    model_file : 
        Path to a file where the constructed Gurobi model (*.lp or *.mps*)
        will be written. If an empty string (default), no model file is exported.

    Returns
    -------
    None
        The function writes the solution to `output_file` and optionally writes
        the Gurobi model to `model_file`. No value is returned.

    Notes
    -----
    - The function builds a complete IP model with appropriately named
        decision variables and constraints for readability in the Gurobi model file.
    - The function then optimizes the model using Gurobi and exports the 
        resulting solution.
    """
    
    return