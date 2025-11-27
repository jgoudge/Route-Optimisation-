def read_input(input_file):
    """
    Read an instance file in the specified format and convert it into
    internal data structures for further processing.

    Parameters
    ----------
    input_file : str
        Path to an existing input file describing the instance, including
        the graph, restaurants, customers, orders, bots, and time settings.

    Returns
    -------
    dict
        A dictionary containing structured data parsed from the input.
        Expected keys include (but are not limited to):
        - "nodes": list or dict representing graph nodes
        - "edges": adjacency list/dict describing travel times
        - "restaurants": dict of restaurant nodes
        - "customers": dict of customer nodes
        - "orders": dict mapping order IDs to (restaurant, customer, deadline)
        - "bots": dict mapping bot IDs to starting positions
        - "parameters": any global parameters (e.g., time format, scoring)

    Notes
    -----
    The exact data structures used must be documented in the accompanying PDF.
    The function only parses data; it performs no validation beyond format checks.
    """
    return 

def write_solution(solution, output_file):
    """
    Write a solution to disk using the required output format.

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
    assignment’s time format and travel times between nodes.
    """
    return 
    
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