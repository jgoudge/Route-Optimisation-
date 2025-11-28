import gurobipy as gp
import basic
from gurobipy import GRB
from datetime import datetime, timedelta

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
    instance = basic.read_input(input_file)
    
    # create a new Gurobi model
    model = gp.Model("pizza_routing")
    
    # contruct time expanded network, T is the time horizon 
    print(instance.time_horizon['start'])
    start = instance.time_horizon['start']
    end = instance.time_horizon['end']
    #T = set(range(start,end))
    print(start)
    T = range((end - start).seconds // 60 + 1)
    T = set(range(1800,2000+1))
    print(T)
    
    
    #objective is to minimize the total time taken to deliver all pizzas
    #model.setObjective( ... , GRB.MINIMIZE)
    
    
    
    #constraints and decision variables to be added here
    # there will be a flow constraint as the graph is directed 
    # subtour??? 
    # linking constraints 
    # capacity or time window constraints -> which there will be? 
    
    
    # writes the solution to output_file
    #write_solution(solution, output_file)
    
    # if third argument is provided, write the model to file
    # model.write(model_file) if model_file != "" else None
    
    return

if __name__ == "__main__":
    optimize_mip("Examples/instance1","/Examples/instance1_sol-MIP",None)