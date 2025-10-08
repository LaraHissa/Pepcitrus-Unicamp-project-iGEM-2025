# run_simulation.py

import sys
from simulation import Simulation
from config import Config

"""
=====================================================================================
MAIN ENTRY POINT (run_simulation.py)
=====================================================================================
This script serves as the program's entry point.
It presents an interactive menu for the user to choose a simulation scenario,
and executes the 'run()' method for the selected scenario(s).
=====================================================================================
"""

def main():
    
    # ------------------ Initialization Message ------------------
    print("="*54)
    print("      Welcome to the SIC + Treatment Simulator!")
    print("-"*54)
    print(" This program models the biological interaction between an")
    print(" infection and the host's callose defense (SIC).")
    print("\n You can then introduce treatments to observe")
    print(" their effect on the simulation's outcome.")
    print("-"*54)
    print(" Created by: Pepcitrus Unicamp - iGEM project")
    print("="*54 + "\n")
    
    # Initialize Configuration once
    cfg = Config()
    
    scenarios_to_run = []
    user_input = ""
    keep_running = True

    while keep_running:
        
        scenarios_to_run.clear() 
        
        # --- Display Menu ---
        print("Please select a simulation scenario or action:")
        print("  'control' -> No drug treatment")
        print("  'ctx'     -> CTX (bactericidal) treatment")
        print("  'tetra'   -> Oxytetracycline (bacteriostatic) treatment")
        print("  'all'     -> Run all scenarios (control, ctx, tetra)")
        print("  'exit'    -> Quit the program")
        user_input = input("Enter your choice: ").strip().lower()
        
        # --- Determine Action/Scenario ---
        if user_input in ["ctx", "tetra", "control"]:
            scenarios_to_run.append(user_input)
        elif user_input == "all":
            scenarios_to_run = ["control", "ctx", "tetra"]
        elif user_input == "exit":
            keep_running = False
            
        else:
            print("\n--- Invalid choice. Please try again. ---\n")
            continue 

        # --- Execute Scenarios ---
        if not scenarios_to_run:
            if user_input == "exit":
                break # Exit gracefully if 'exit' was the only input
            continue # Go back to menu if input was invalid

        print("\nInput accepted! Initializing simulation(s)...")
        print("This may take a moment. Please wait...\n")
        
        
        for treatment in scenarios_to_run:
            
            print(f">>> Running scenario: {treatment} <<<")
            
            # --- Simulation Execution ---
            # Instantiate the simulation object, passing the configuration
            sim = Simulation(cfg) 
            sim.run(treatment)
            
            print(f"Scenario '{treatment}' finished.")
        
        # Pause/wait is unnecessary in Python interactive loop, just print feedback
        print("\nAll selected simulations completed. Returning to menu.\n")
        
    
    print("\nProgram finished. Thank you for using our model!\n")
    # Note: In Python, returning 0 is the default success, no explicit sys.exit() needed.

if __name__ == "__main__":
    main()
