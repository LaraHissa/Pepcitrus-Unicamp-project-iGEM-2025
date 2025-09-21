#ifndef CONSTANTS_H
#define CONSTANTS_H

/*
 * =====================================================================================
 * MODEL'S FUNDAMENTAL CONSTANTS
 * =====================================================================================
 * This file defines the fixed and non-adjustable constants of the model.
 * These values represent biological hypotheses or numerical parameters
 * intrinsic to the simulation and should not be altered between different
 * runs of the same experiment.
 *
 * For adjustable experiment parameters, see the config.h file.
 *  
 * Created by: Pepcitrus Unicamp - iGEM project 
 * Created on: September 15, 2025
 * Last Modified: September 21,2025.
 * =====================================================================================
 */

 namespace model_constants {

    constexpr double INITIAL_INFECTION_LOAD = 0.1;      // Initial infection load applied to a single cell at the beginning.
    constexpr double SPREAD_INFECTION_LOAD = 0.05;         // Infection load transferred to a neighboring cell during a spread event.
    constexpr double CALLOSE_SIGNAL_EC50 = 0.5;            // Half-activation point (EC50) for callose production via the Hill function.
    constexpr double CALLOSE_HILL_COEFFICIENT = 2.0;       // Hill coefficient for callose production, determines the "steepness" of the response.
    constexpr double TETRACYCLINE_ACTIVE_CLEARING = 0.015; // Active bacterial clearing factor induced by bacteriostatic treatment (Tetracycline).
    constexpr double NUMERICAL_EXTINCTION_THRESHOLD = 1e-3; // Threshold below which bacterial load is considered zero.

}

#endif 