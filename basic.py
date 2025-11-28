from datetime import datetime, timedelta
from dataclasses import dataclass
import networkx as nx 
import matplotlib.pyplot as plt

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
    Data structure representing a directed graph
    
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

def find_transit_time(start, end, graph):
    transit_time = 0 
    DG = nx.DiGraph()
    DG.add_weighted_edges_from(graph)
    transit_time = nx.dijkstra_path_length(DG, start, end)
    return transit_time 

def print_graph(graph):
    # turn instance graph into a networkx directed graph and print it
    DG = nx.DiGraph()
    DG.add_weighted_edges_from(graph)

    pos = nx.spring_layout(DG, seed=42) 
    nx.draw_networkx_nodes(DG, pos, node_size=700, node_color='lightblue')

    # Draw edges with arrows
    nx.draw_networkx_edges(DG, pos, arrowstyle='->', arrowsize=20)

    # Draw node labels
    nx.draw_networkx_labels(DG, pos, font_size=12, font_weight='bold')

    # Draw edge weights
    edge_labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)

    # Show the plot
    plt.title("Directed Graph (DiGraph) with Weights")
    plt.axis('off')  # optional: turn off the axes
    plt.show()
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
    """
    # Read input and solution file 
    inst = read_input(input_file)
    solution = read_solution(solution_file)
    
    arrival_times = {}
    time = inst.time_horizon['start']
    time_dt = datetime.combine(datetime.today(), time)
    
    # For each bot in solution, for each order in bot's list
    for bot in solution:
        start_location = inst.bots[bot]
        for order in solution[bot]:
            # Get order details from instance
            restaurant_location = inst.orders[order]["Restaurant location"]
            customer_location = inst.orders[order]["Customer Location"]
            print(f"\nBot {bot} starting at location {start_location} for order {order} at time {time_dt.time()}")
            
            # get the ready time and convert to datetime object 
            ready_time = inst.orders[order]["Ready time"]
            ready_dt = datetime.combine(datetime.today(), ready_time)
            print(f"order ready time is at {ready_dt.time()}")
            
            # Find transit time from start to restaurant
            transit_time = find_transit_time(start_location, restaurant_location, inst.graph)
            time_dt += timedelta(minutes=transit_time)
            print(f"found transit time of {transit_time} minutes, arrival at restaurant {restaurant_location} at time {time_dt.time()}")
            
            # one minute to enter restaurant 
            time_dt += timedelta(minutes=1)
            print(f"add 1 minute to enter restaurant the time is now {time_dt.time()}")
            
            # check if the order time is ready or if have to wait 
            if time_dt < ready_dt:
                print(f"waiting for order to be ready at {ready_dt.time()} ... ")
                time_dt = ready_dt
                print(f"the time is now {time_dt.time()}")   
            else:
                print("no waiting needed, order is ready")
                
            #add 1 minute to exit restaurant and use current time
            time_dt += timedelta(minutes=1)
            print("adding 1 minute to exit restaurant time is now ", time_dt.time())
            
            # find transit time from restaurant to customer
            transit_time = find_transit_time(restaurant_location, customer_location, inst.graph)
            time_dt += timedelta(minutes=transit_time)
            arrival_time = time_dt
            arrival_times[order] = time_dt.strftime("%H:%M")
            print(f"found transit time of {transit_time} minutes, arrival to customer at time {time_dt.time()}")
            
            # self check adds 5 minutes for delivery process 
            time_dt += timedelta(minutes=5)
            print("adding 5 minutes for delivery process time is now ", time_dt.time())
            
            # starting location is now the current customer position 
            start_location = customer_location
            start_dt = time_dt
            
    # Check for unserved orders
    for orders in inst.orders:
        if orders not in arrival_times:
            arrival_times[orders] = "unserved"
            
    return arrival_times

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
    arrival_t = arrival_times(input_file, solution_file)

    # For each bot in solution, for each order in bot's list
    for bot in solution:
        start_location = inst.bots[bot]
        for order in solution[bot]:
            # get the ready time and convert to datetime object 
            ready_time = inst.orders[order]["Ready time"]
            ready_dt = datetime.combine(datetime.today(), ready_time)
            
            # get the arrival time at customer from previously computed arrival times
            arrival_dt = datetime.combine(datetime.today(), datetime.strptime(arrival_t[order], "%H:%M").time())
            minutes_delta = (arrival_dt - ready_dt).total_seconds() / 60

            # calculate the freshness score using the difference and freshness function
            freshness_fnc = inst.orders[order]["Freshness Function"]
            total_score += freshness_function(minutes_delta, freshness_fnc)
            
    # Check for unserved orders
    for order in arrival_t:
        if arrival_t[order] == "unserved":
            freshness_fnc = inst.orders[order]["Freshness Function"]
            total_score += freshness_function(float('inf'), freshness_fnc) 

    print(f"=== solution value ===\n{total_score}\n")
    print("=== arrival times ===")
    
    for item in sorted(arrival_t):
        print(f"{item} : {arrival_t[item]}")

    #print_graph(inst.graph)
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

    
def instruction_file(input_file, solution_file, output_path):
    """
    Write a step-by-step instruction file for a specific PizzaBot.

    Parameters
    ----------
    input_file : str
        Path to an input instance file describing the graph and orders.

    solution_file : str
        Path to a solution file specifying bot routes and assigned orders.
        
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
    instance = read_input(input_file)
    solution = read_solution(solution_file)
    
    #make directed graph
    DG = nx.DiGraph()
    DG.add_weighted_edges_from(instance.graph)

    with open(output_path, "w") as f:
        for bots in solution:
            location = instance.bots[bots]
            print("\n=== instructions ===")
            print(f"[{bots}]")
            f.write(f"[{bots}]\n")
            
            for order in solution[bots]:
                # get restaurant location  
                restaurant_location = inst.orders[order]["Restaurant location"]

                # get all nodes from position to restaurant 
                path = nx.dijkstra_path(DG, location, restaurant_location)

                for node in path[1:]:
                    print("go to " + node)
                    f.write("go to " + node + "\n")
                    location = node
                
                # at the restaurant 
                print("collect food")
                f.write("collect food\n")
                
                # get customer location
                customer_location = inst.orders[order]["Customer Location"]
                
                # get all nodes from restaurant to customer 
                path = nx.dijkstra_path(DG, location, customer_location)

                for node in path[1:]:
                    print("go to " + node)
                    f.write("go to " + node + "\n")
                    location = node

                # at the customer
                print("deliver food")
                f.write("deliver food\n")
    return 

if __name__ == "__main__":
    inst = read_input("Examples/instance1")
    #write_instance(inst, "Examples/output_instance1.txt")
    evaluate("Examples/instance1", "Examples/instance1_sol")
    #arrival_times("Examples/instance1", "Examples/instance1_sol")
    instruction_file("Examples/instance1", "Examples/instance1_sol", "Examples/instance1-instructions.txt")
    
    