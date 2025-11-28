from basic import instruction_file, evaluate, arrival_times
from mip import optimize_mip

for i in range(1, 9):
    inst_name = f"instance{i}"
    sol_given = f"{inst_name}_sol"
    sol_MIP = f"{inst_name}_sol-MIP"

    print(f"========= {inst_name}  START =========\n")

    instruction_file(inst_name, sol_given, f"{inst_name}-instructions")
    
    print(f"*** ARRIVAL TIMES {sol_given} ***")
    for o, t in arrival_times(inst_name, sol_given).items():
        print(f"{o}: {t}")

    print("\n********* BEGIN OPTIMIZING *********")
    optimize_mip(inst_name, sol_MIP)
    print("********** END OPTIMIZING **********\n")


    print(f"VALUE COMPUTED SOLTUION ({sol_MIP}): {evaluate(inst_name, sol_MIP)}") 
    print(f"VALUE GIVEN SOLUTION ({sol_given}): {evaluate(inst_name, sol_given)}\n") 

    print(f"========= {inst_name} FINISH =========\n\n")