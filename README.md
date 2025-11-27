**PizzaBot Route Optimisation – MIP Solver (Gurobi)**

This project implements a complete pipeline for reading PizzaBot routing instances, building a (mixed-)integer programming model with Gurobi, solving for an optimal assignment and routing plan, evaluating solutions, and producing step-by-step instruction files for each bot.

It includes:

Data structures for storing all instance information

File readers/writers for the specified input/output formats

Evaluation functions (freshness score, arrival times)

Instruction file generation

A full Gurobi IP model for route optimisation
