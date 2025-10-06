#include "simulation.h"
#include <iostream>
#include <string>
#include <limits> 
#include <vector>  
#include <chrono>   
#include <thread>   

/*
 * =====================================================================================
 *                            Main Entry Point (main.cpp)
 * =====================================================================================
 * This file contains the 'main' function, which is the program's entry point.
 * It presents an interactive menu for the user to choose a simulation scenario,
 * creates the main simulation object, and calls the 'run()' method.
 * * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: June 11, 2025
 * Last Modified: October 6, 2025 (Refactored for Interactive Loop and 'all' option).
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
    
    
    std::vector<std::string> scenariosToRun;
    std::string userInput;
    bool keepRunning = true;

    while (keepRunning) {
        
        scenariosToRun.clear(); 
        
        std::cout << "Please select a simulation scenario or action:\n";
        std::cout << "  'control' -> No drug treatment\n";
        std::cout << "  'ctx'     -> CTX (bactericidal) treatment\n";
        std::cout << "  'tetra'   -> Tetracycline (bacteriostatic) treatment\n";
        std::cout << "  'all'     -> Run all scenarios (control, ctx, tetra)\n";
        std::cout << "  'exit'    -> Quit the program\n";
        std::cout << "Enter your choice: " << std::flush;

        std::cin >> userInput;
        
      
        if (userInput == "ctx" || userInput == "tetra" || userInput == "control") {
            scenariosToRun.push_back(userInput);
        } else if (userInput == "all") {
            scenariosToRun = {"control", "ctx", "tetra"};
        } else if (userInput == "exit") {
            keepRunning = false;
        } else {
            std::cout << "\n--- Invalid choice. Please try again. ---\n\n";
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue; 
        }

        if (!scenariosToRun.empty()) {
            
            std::cout << "\nInput accepted! Initializing simulation(s)..." << std::endl;
            std::cout << "This may take a moment. Please wait..." << std::endl << std::endl;
            
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            
            for (const std::string& treatment : scenariosToRun) {
                
                std::cout << ">>> Running scenario: " << treatment << " <<<" << std::endl;
                
                simulation sim;
                sim.run(treatment);
                
                std::cout << "Scenario '" << treatment << "' finished.\n";
            }
            
            std::cout << "\nAll selected simulations completed. Returning to menu.\n" << std::endl;
        }
    }
    
    std::cout << "\nProgram finished. Thank you for using our model!\n";
    return 0;
}