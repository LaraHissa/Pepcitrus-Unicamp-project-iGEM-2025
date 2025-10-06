#ifndef CONFIG_H
#define CONFIG_H

/*
 * =====================================================================================
 *                      CENTRAL SIMULATION CONFIGURATION
 * =====================================================================================
 * This file serves as the control panel for all experiments. 
 * Modify the values in the 'config' and 'drug_params' structs below to adjust the simulation's behavior.
 * 
 *  Key Sections:
 * -ENVIRONMENT AND DURATION: Grid size and simulation time steps;
 * -INFECTION DYNAMICS: Growth and spread rates of the bacteria;
 * -HOST RESPONSE: Parameters for callose production, degradation, and signaling radius;
 * -DRUG PROPERTIES: Doses, potencies and half-lives of the treatments.
 * 
 * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: June 11, 2025
 * Last Modified: September 21,2025.
 *                  
 *         Have fun! :)
 * =====================================================================================
 */

// Describes the properties of a medicine treatment
struct drug_params {
    double dose;        // normalized dose applied
    double EC50;        // potency (concentration for 50% effect)
    double hillN;       // hill coefficient
    double killScale;   // maximum efficacy factor
    double Tmax;        // time to reach max concentration
    double halfLife;    // effect duration (halfLife in time steps)
};

//Central struct that groups all simulation settings
struct config {
    // --- Grid and Time ---
    int L = 50;                  // grid dimension (LxL)
    int steps = 1000;            // time steps (in days) before treatment
    int extraSteps = 1500;       // time steps (in days) after treatment

    // --- Infection Dynamics ---
    double beta = 0.08;          // base spread probability
    double r = 0.15;             // growth rate
    double Imax = 1.0;           // cell's carrying capacity (max load)
    double d = 0.7;              // efficacy of callose in suppressing infection
    double deltaI = 0.001;       // natural death rate of the 'bacteria'

    // --- Defense Dynamics (Callose) ---
    double alphaC = 0.6;        // callose production rate
    double deltaC = 0.001;        // callose degradation rate 
    double Climit = 1.0;         // max callose level per cell
    int signalR = 6;             // signaling radius to activate defense

    // --- Treatment Settings ---
    drug_params CTXparams = {15.0 / 80.0, 0.40, 2.0, 3.0, 14.0, 100.0};
    drug_params TETRACYCLINEparams = {150.0 / 80.0, 1.0, 2.0, 3.0, 14.0, 200.0};

   
};


#endif
