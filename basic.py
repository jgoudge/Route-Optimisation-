from datetime import datetime


def read_input(input_file):
    """
    Read an instance file in the specified format and convert it into
    internal data structures for further processing.

    Parameters
    ----------
    input_file : str
        Path to an existing input file describing the instance, including
        the bots, graph, orders and time horizon.

    Returns
    -------
    bots : dict 
        A dictionary mapping bot IDs to their starting locations.
    graph : list of tuples
        A list of edges in the graph, each represented as a tuple
        (tail, head, transit_time).
    time_horizon : dict
        A dictionary with keys "start" and "end" mapping to datetime.time
        objects representing the time horizon.
    orders : dict
        A dictionary mapping order IDs to their details, including
        restaurant location, customer location, ready time, and freshness function.
    """
    bots = {}
    graph = []
    time_horizon = {}
    orders = {}
    
    section = "None"
    
    with open(input_file, 'r') as file:
        for line in file:
            read_line = line.strip()
        
            if read_line == "[bots]":
                section = "bots"
                continue 
            elif read_line == "[graph]":
                section = "graph"
                continue 
            elif read_line == "[time horizon]":
                section = "time horizon"
                continue 
            elif read_line == "[orders]":
                section = "orders"
                continue
                
            if section == "bots" and read_line != "":
                # id ; location
                bot_id, location = read_line.split(";")
                bots[bot_id] = location
                
            elif section == "time horizon" and read_line != "":
                # label (start or end); time in HH:MM format
                label, time_string = read_line.split(" ")
                time_object = datetime.strptime(time_string, "%H:%M").time()
                time_horizon[label] = time_object
                
            elif section == "orders" and read_line != "":
                # id; restaurant_location; customer_location; ready_time; a0; p0; a1; p2 ... ak; pk 
                # a0 ... ak specifies freshness score function. 
                order_id, restaurant_location, customer_location, ready_time, *freshness_function = read_line.split(";")
                orders [order_id] = {"Restaurant location": restaurant_location, 
                                    "Customer Location": customer_location, 
                                    "Ready time": ready_time,
                                    "Freshness Function": freshness_function}
                
            elif section == "graph" and read_line != "":
                # tail ; head ; transit_time 
                # -----> at the moment just an edge list good for Gurobi MIP model
                # ---> might need to implement an adjacency list or matrix for heuristic solution
                tail, head, transit_time = read_line.split(";")
                graph.append((tail, head, int(transit_time)))
    
    return bots, graph, time_horizon, orders

def evaluate(input_file, solution_file):
    """
    Evaluate a solution by returning its total freshness score and any
    additional diagnostic information.

    Parameters
    ----------
    input_file : str
        Path to an input instance file.

    solution_file : str
        Path to a solution file in the required output format.

    Returns
    -------
    dict
        A dictionary containing evaluation metrics, including:
        - "score": total freshness score
        - "arrival_times": dict of order → arrival time or "unserved"
        - any additional metrics optionally included

    Notes
    -----
    This function acts as a wrapper combining:
    - value()
    - arrival_times()
    """
    bots, graph, time_horizon, orders = read_input(input_file)
    print(bots)
    
    #with open(solution_file, 'r') as file_object:
        #solution_data = file_object.read()
    
    #print(solution_data)
    
    return 


def write_solution(solution, output_file):
    """
    Write a solution using the required output format.

    Parameters
    ----------
    solution : dict
        Data structure representing the solution. Expected to map each bot ID
        to a list of actions or assigned orders in the required specification.
        The exact structure is defined in the assignment PDF.

    output_file : str
        Path where the solution file should be written. File will be created
        or overwritten.

    Returns
    -------
    None
        The function writes the solution to the file but returns nothing.

    Notes
    -----
    This function must produce output *exactly* in the required format,
    since it will be evaluated by automated scripts.
    """
        
    return 

def value(input_file, solution_file):
    """
    Compute the total freshness score of a provided solution.

    Parameters
    ----------
    input_file : str
        Path to an input instance file.

    solution_file : str
        Path to a solution file describing bot assignments and routes.

    Returns
    -------
    float
        The total freshness score of the solution. Higher is better.

    Notes
    -----
    The function must:
    - read and parse both input and solution files,
    - simulate bot movements,
    - compute arrival times,
    - compute freshness contribution for each delivered order,
    - sum these values into an overall score.
    """
    
    return 

def arrival_times(input_file, solution_file):
    """
    Compute arrival times for each order served in a solution.

    Parameters
    ----------
    input_file : str
        Path to an input instance file.

    solution_file : str
        Path to a solution file in the required format.

    Returns
    -------
    dict
        A dictionary mapping each order ID to either:
        - a string "HH:MM" representing the arrival time at the customer, or
        - the string "unserved" if the order was not fulfilled.

    Notes
    -----
    The function must simulate all bot routes exactly in the sequence
    specified in the solution file. Time must be handled using the
    assignment's time format and travel times between nodes.
    """
    return 
    
def instruction_file(input_file, solution_file, x, output_path):
    """
    Write a step-by-step instruction file for a specific PizzaBot.

    Parameters
    ----------
    input_file : str
        Path to an input instance file describing the graph and orders.

    solution_file : str
        Path to a solution file specifying bot routes and assigned orders.

    x : str
        The ID of the bot for which instructions should be produced.

    output_path : str
        Path where the instruction text file should be written.

    Returns
    -------
    None
        Writes a file containing human-readable movement and action steps.

    File Format
    -----------
    The file must contain a section beginning with:
        [<bot_id>]

    Each subsequent line must be one of the following commands:
        go to <node_id>
        collect food
        deliver food

    Notes
    -----
    - "go to" lines must list *every* intermediate node on the shortest path.
    - "collect food" is written upon reaching the restaurant of an assigned order.
    - "deliver food" is written upon reaching the customer of that order.
    - The function must process orders in the exact sequence given in the solution.
    """
    return 

if __name__ == "__main__":
    evaluate("Examples/input.txt", "Examples/solution.txt")