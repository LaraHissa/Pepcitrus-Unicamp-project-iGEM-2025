#include "simulation.h"
#include <iostream>
#include <string>
#include <limits> 
#include <chrono>   
#include <thread>   

/*
 * =====================================================================================
 *                           Main Entry Point (main.cpp)
 * =====================================================================================
 * This file contains the 'main' function, which is the program's entry point.
 * It presents an interactive menu for the user to choose a simulation scenario,
 * creates the main simulation object, and calls the 'run()' method.
 * 
 * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: June 11, 2025
 * Last Modified: September 19,2025.
 * =====================================================================================
 */

int main() {
   
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    
    std::cout << "======================================================\n";
    std::cout << "      Welcome to the SIC + Treatment Simulator!\n";
    std::cout << "------------------------------------------------------\n";
    std::cout << " This program first models the biological interaction\n";
    std::cout << " between an infection and the host's callose defense (SIC).\n\n";
    std::cout << " You can then introduce treatments to observe\n";
    std::cout << " their effect on the simulation's outcome.\n";
    std::cout << "------------------------------------------------------\n\n";
    std::cout << " Created by: Pepcitrus Unicamp - iGEM project \n";
    std::cout << "======================================================\n\n";
    
    std::string treatment;
    bool validInput = false;

    while (!validInput) {
        std::cout << "Please select a treatment scenario to run:\n";
        std::cout << "  'control' -> No drug treatment\n";
        std::cout << "  'ctx'     -> CTX (bactericidal) treatment\n";
        std::cout << "  'tetra'   -> Tetracycline (bacteriostatic) treatment\n";
        std::cout << "Enter your choice: " << std::flush;

        std::string userInput;
        std::cin >> userInput;
        if (userInput == "ctx" || userInput == "tetra" || userInput == "control") {
            treatment = userInput;
            validInput = true;
            
        } else {
            std::cout << "\n--- Invalid choice. Please try again. ---\n\n";
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
    }
    std::cout << "\nInput accepted! Initializing simulation for scenario '" << treatment << "'..." << std::endl;
    std::cout << "This may take a moment. Please wait..." << std::endl << std::endl;
    
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    // --- Simulation Execution ---
    
    simulation sim;
    sim.run(treatment);
    std::cout << "\nProgram finished. Thank you for using our model!\n";

    return 0;
}