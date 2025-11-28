from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass 
class problem_instance:
    """
    Data structure representing a complete problem instance.
    
    Attributes
    -----------
    bots : dict 
        A dictionary mapping bot IDs to their starting locations.
    graph : list
        A list of edges in the graph, each represented as a tuple
        (tail, head, transit_time).
    time_horizon : dict
        A dictionary with keys "start" and "end" mapping to datetime.time
        objects representing the time horizon.
    orders : list
        A list of orders, each represented as an order dataclass instance.
    """
    bots: dict 
    graph: list 
    time_horizon: dict
    orders: list

@dataclass 
class graph:
    """
    Data structure representing a 
    
    """
    tail: str
    head: str
    transit_time: int
    
@dataclass 
class bot:
    """
    Data structure representing a PizzaBot.
    
    Attributes
    -----------
    id : str
        Unique identifier for the bot.
    location : str
        Starting location of the bot.
    """
    id: str
    location: str
    
@dataclass 
class time_horizon:
    """
    Data structure representing the time horizon for the problem instance.
    
    Attributes
    -----------
    start : str
        Start time of the time horizon in the format (AA:BB) HH:MM.
    end : str
        End time of the time horizon in the format (CC:DD) HH:MM.
    """
    start: datetime.time
    end: datetime.time

@dataclass
class order:
    """
    Data structure representing a customer order.
    
    Attributes
    -----------
    id : str
        Unique identifier for the order.
    restaurant_location : str
        Location of the restaurant preparing the order.
    customer_location : str
        Location of the customer receiving the order.
    ready_time : datetime.time
        Time when the order is ready for pickup in datetime format HH:MM.
    """
    id: str
    restaurant_location: str
    customer_location: str
    ready_time: datetime.time
    freshness_function: list 


# Custom exception for parsing errors
class ParsingError(Exception):
    """Custom exception for errors encountered during parsing of input files."""
    def __init__(self, filename, line, note=""):
        self.filename = filename
        self.line = line
        self.message = f"Error parsing file {filename} at line: {line}. {note}"
        super().__init__(self.message)

        
def parse_freshness(freshness_values):
    """
    Takes the original freshness values from the input file and converts them
    to a list of tuples representing the piecewise constant freshness function.
    
    Parameters
    ----------
    freshness_values : list of str
        List of strings in the format "start:score" representing the freshness
        score function.
        
    Returns
    -------
    freshness_function : list of tuples
        A list of tuples (start_t, end_t, score) representing the piecewise
        constant freshness function.
    """
    pairs = []
    freshness_function = []
    
    # Convert input strings to (start, score) pairs
    for item in freshness_values:
        start, score = item.split(":")
        pairs.append((int(start), int(score)))
    
    # Create piecewise constant function intervals
    for index in range(len(pairs) - 1):
        start_t = pairs[index][0]
        end_t = pairs[index + 1][0]
        score = pairs[index][1]
        freshness_function.append((start_t, end_t, score))
    
    # Handle the last interval extending to infinity
    last_t, last_score = pairs[-1]
    freshness_function.append((last_t, float('inf'), last_score))

    return freshness_function

def read_input(input_file: str) -> problem_instance:
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
    problem_instance
        A data structure encapsulating all relevant information from the
        input file, including bots, graph, time horizon, and orders.
    """
    
    graph = []
    time_horizon = {}
    orders = {}
    bots = {}
    section = None
    
    # Read the input file line by line
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            
            # Check for section headers
            if line.startswith("[") and line.endswith("]"):
                match line:
                    case "[bots]":
                        section = "bots"
                    case "[graph]":
                        section = "graph" 
                    case "[time horizon]":
                        section = "time horizon"        
                    case "[orders]":
                        section = "orders"
                continue #skip to next line (content after header)   
            try: 
                if section == "bots":
                    bot_id, location = line.split(";")
                    bots[bot_id] = location
                elif section == "graph":
                    tail, head, transit = line.split(";")
                    graph.append((tail, head, int(transit)))
                    
                elif section == "time horizon":
                    label, time = line.split(" ")
                    time = datetime.strptime(time, "%H:%M").time()
                    time_horizon[label] = time
                    
                elif section == "orders":
                    order_id, restaurant, customer, ready_time, *f_vals = line.split(";")
                    freshness = parse_freshness(f_vals)
                    ready_time = datetime.strptime(ready_time, "%H:%M").time()
                    orders[order_id] = {
                        "Restaurant location": restaurant,
                        "Customer Location": customer,
                        "Ready time": ready_time,
                        "Freshness Function": freshness
                    }
                else: 
                    raise ParsingError(input_file, line, "Found data outside any section")
            
            except (TypeError, ValueError):
                raise(ParsingError(input_file, line))

    inst = problem_instance(bots=bots, graph=graph, 
                            time_horizon=time_horizon, orders=orders)
    return inst

def write_instance(instance: problem_instance, output_file: str):
    """
    Write a problem instance to an output file in the specified format.

    Parameters
    ----------
    instance : problem_instance
        The problem instance data structure containing bots, graph,
        time horizon, and orders.

    output_file : str
        Path where the instance file should be written. File will be created
        or overwritten.

    Returns
    -------
    None
        The function writes the instance to the file but returns nothing.
    """
    with open(output_file, "w") as file:   
        # Write graph section
        file.write("[graph]\n")
        for tail, head, transit_time in instance.graph:
            file.write(f"{tail};{head};{transit_time}\n")
        file.write("\n")
        
        # Write bots section
        file.write("[bots]\n")
        for bot_id, location in instance.bots.items():
            file.write(f"{bot_id};{location}\n")
        file.write("\n")
        
        # Write time horizon section
        file.write("[time horizon]\n")
        for label, time_obj in instance.time_horizon.items():
            time_str = time_obj.strftime("%H:%M")
            file.write(f"{label} {time_str}\n")
        file.write("\n")

        # Write orders section
        file.write("[orders]\n")
        for order, details in instance.orders.items():
            ready_time_str = details["Ready time"].strftime("%H:%M")
            freshness_parts = [
                f"{start}:{score}" for start, end, score in details["Freshness Function"]
            ]
            freshness_str = ";".join(freshness_parts)
            file.write(f"{order};{details['Restaurant location']};"
                    f"{details['Customer Location']};{ready_time_str};"
                    f"{freshness_str}\n")
    return 

def read_solution(solution_file: str) -> dict:
    # Read solution file stores solution as a dictionary
    # bot_id : [order_id1, order_id2, ...]
    solution = {}
    
    with open(solution_file, 'r') as file:
        for line in file:
            read_line = line.strip()
            bot_id , *order_ids = read_line.split(";")
            solution[bot_id] = order_ids    
    return solution

def freshness_function(arrival_difference, freshness_list):
    """
    Compute the freshness score based on arrival time difference and the provided freshness function
    of the order provided. 
    
    Parameters
    ----------
    arrival_difference : int
        The time difference between the order ready time and the arrival time at the customer.
    freshness_list : list of tuples
        A list of tuples (start_t, end_t, score) representing the piecewise
        constant freshness function.
    
    Returns
    -------
    score: int
        The freshness score based on the arrival time difference.
    """
    for interval in freshness_list:
        int_start, int_end, score = interval 
        #print(f"Checking interval {int_start} to {int_end} with score {score}")
        if arrival_difference >= int_start and arrival_difference < int_end:
            return score 

    return score 


def evaluate(input_file, solution_file):
    """
    Evaluate a solution by returning its total freshness score 

    Parameters
    ----------
    input_file : str
        Path to an input instance file.

    solution_file : str
        Path to a solution file in the required output format.
    Returns
    -------
    int
        The total freshness score achieved by the solution file.
    """
    # Read input and solution file 
    inst = read_input(input_file)
    solution = read_solution(solution_file)
    
    # Initialize total score
    total_score = 0
    start_time = inst.time_horizon['start']
    print(f"Start time is {start_time}")
    start_dt = datetime.combine(datetime.today(), start_time)
    

    # For each bot in solution, for each order in bot's list
    for bot in solution:
        print(solution[bot])
        start_location = inst.bots[bot]
        for order in solution[bot]:
            # Get order details from instance
            print(f"Getting order details {order} executed by {bot}")
            #start_location = inst.bots[bot]
            restaurant_location = inst.orders[order]["Restaurant location"]
            customer_location = inst.orders[order]["Customer Location"]
            print(f"Starting at {start_location} the restaurant is at {restaurant_location} and customer at {customer_location}")
            
            # get the ready time and convert to datetime object 
            ready_time = inst.orders[order]["Ready time"]
            ready_dt = datetime.combine(datetime.today(), ready_time)

            # Find transit time from start to restaurant
            print("Finding transit time from start to restaurant")
            for edges in inst.graph:
                if edges[0] == start_location and edges[1] == restaurant_location:
                    transit_time = edges[2]
                    print(f"Found edge {edges} with transit time {transit_time}")
                    break
                #else:
                    #print("there are no directly connected routes and need to connect via other nodes")
            
            # time after transit to restaurant
            time_dt = start_dt + timedelta(minutes=transit_time)
            
            # one minute to enter restaurant 
            print("adding 1 minute to enter restaurant")
            time_dt += timedelta(minutes=1)
            print(f"the time is now {time_dt.time()}")
            
            
            if time_dt < ready_dt:
                print(f"waiting for order to be ready at {ready_dt.time()}")
                time_dt = ready_dt
                print(f"the time is now {time_dt.time()}")
                # add one minute to exit the restaurant
                time_dt += timedelta(minutes=1)
                print("adding 1 minute to exit restaurant time is now ", time_dt.time())
                
            else:
                print("no waiting needed, order is ready")
                #add 1 minute to exit restaurant and use current time
                time_dt += timedelta(minutes=1)
            
            # Find transit time from restaurant to customer
            print("Finding transit time from restaurant to customer")
            print(f"looking for edge from {restaurant_location} to {customer_location}")
            for edges in inst.graph:
                if edges[0] == restaurant_location and edges[1] == customer_location:
                    transit_time = edges[2]
                    print(f"Found edge {edges} with transit time {transit_time}")
                    break
                #else:
                    #print("there are no directly connected routes and need to connect via other nodes")
            
            # time after transit to customer
            time_dt += timedelta(minutes=transit_time)
            arrival_time = time_dt
            print("arrived at customer at time ", time_dt.time())
            
            # self check adds 5 minutes for delivery process 
            time_dt += timedelta(minutes=5)
            print("adding 5 minutes for delivery process time is now ", time_dt.time())
            minutes_delta = (arrival_time - ready_dt).total_seconds() / 60
            
            # calculate the freshness score using the difference and freshness function
            freshness_fnc = inst.orders[order]["Freshness Function"]
            print(f"difference to arrival time = {minutes_delta} with freshness function {freshness_fnc}")
            score = freshness_function(minutes_delta, freshness_fnc)
            total_score += score
            
            # starting location is now the current customer position 
            start_location = customer_location
            

    print(f"Total freshness score: {total_score}")
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
    
    ### if the bot arrives at restuarant at time T0 
        # departs from restaurant at T1 =  max{start time + 1, T0 +2}
        # arrives at the customer T2 = T1 + travel time from restaurant to customer
        # when is it ready for the next customer T3 = T2 + 5 
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
    inst = read_input("Examples/instance1")
    #write_instance(inst, "Examples/output_instance1.txt")
    evaluate("Examples/instance1", "Examples/instance1_sol")
    