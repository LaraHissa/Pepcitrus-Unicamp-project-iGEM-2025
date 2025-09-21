#ifndef SIMULATION_H
#define SIMULATION_H

#include "config.h"
#include "infection.h"
#include "callose.h"
#include "therapeutic.h"
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <cmath>
#include <filesystem>
#include <iomanip>
#include <sstream>

/*
 * ==============================================================================
 *                             CLASS SIMULATION
 * ===============================================================================
 * The main class that coordinates the entire simulation.
 * It initializes the components, manages the main time loop, applies treatments,
 * and logs the output data.
 * 
 * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: August , 2025
 * Last Modified: September 19,2025.
 * ==================================================================================
 */

class simulation {
private:
// --- Model Components ---
    config cfg; 
    network net;
    infection infection_obj;
    callose callose_obj;     
    std::vector<int> doseTimes;  //vector to store the time points of drug administration
    
    // calculates the total drug concentration at the current time, summing the effects of all previous doses
    double calculate_total_concentration(const drug_params& params, int globalTime, int treatmentStart) const; 
    
    // Helper function to save the combined state of all grids to a single file
    void save_combined_data(
        const std::vector<std::vector<double>>& infection,
        const std::vector<std::vector<double>>& callose,
        const std::vector<std::vector<double>>& drug,
        const std::string& filename
    );

public:
    simulation(); //constructor that initializes the simulation and all its components 
    void run(const std::string& treatment); //executes the full simulation for a specific treatment scenario
};


// --- Functions Bodies ---

inline simulation::simulation() : cfg(), net(cfg.L, cfg.signalR), infection_obj(cfg), callose_obj(cfg) {}

inline double simulation::calculate_total_concentration(const drug_params& params, int globalTime, int treatmentStart) const {
    double totalConcentration = 0.0;
    for (int doseTime : doseTimes) {
        double timeSinceDose = globalTime - (treatmentStart + doseTime);
        totalConcentration += therapeutic::get_concentration(params.dose, timeSinceDose, params.Tmax, params.halfLife);
    }
    return totalConcentration;
}

inline void simulation::save_combined_data(
    const std::vector<std::vector<double>>& infection,
    const std::vector<std::vector<double>>& callose,
    const std::vector<std::vector<double>>& drug,
    const std::string& filename) {
    
    std::ofstream outfile(filename);
    outfile << "i,j,infection,callose,drug\n";

    int L = infection.size();
    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            outfile << i << "," << j << ","
                    << infection[i][j] << ","
                    << callose[i][j] << ","
                    << drug[i][j] << "\n";
        }
    }
    outfile.close();
}


inline void simulation::run(const std::string& treatment) {
    infection_obj.initialize();
    callose_obj.initialize();
    doseTimes.clear();

    std::string data_dir = "data_" + treatment;
    std::filesystem::create_directory(data_dir);
    std::cout << "Saving frame data to directory: " << data_dir << std::endl;

    std::ofstream file("results_" + treatment + ".csv");
    file << "time,mean_infection,mean_callose,drug_concentration\n";

    int treatmentStart = cfg.steps;
    int totalSteps = cfg.steps + cfg.extraSteps;

    for (int t = 0; t < totalSteps; ++t) {
        double drugConc = 0.0;
        double inhibitionFactor = 0.0;
        
        if (treatment != "control" && t == treatmentStart) {
            doseTimes.push_back(0);
        }

     
        if (treatment == "tetra") {
            drugConc = calculate_total_concentration(cfg.TETRACYCLINEparams, t, treatmentStart);
            if (drugConc > 1e-9) {
                const auto& p = cfg.TETRACYCLINEparams;
                inhibitionFactor = pow(drugConc / p.EC50, p.hillN) / (pow(drugConc / p.EC50, p.hillN) + 1.0);
                inhibitionFactor = std::min(1.0, inhibitionFactor * p.killScale);
            }
        }
        infection_obj.spread(callose_obj.get_matrix(), cfg.beta, inhibitionFactor, net);

     
        if (treatment == "ctx") {
            drugConc = calculate_total_concentration(cfg.CTXparams, t, treatmentStart);
            infection_obj.update(callose_obj.get_matrix(), drugConc, true, cfg.CTXparams);
        } else {
            
            infection_obj.update(callose_obj.get_matrix(), (treatment == "tetra" ? drugConc : 0.0), false, cfg.TETRACYCLINEparams);
        }
        
       
        callose_obj.update(infection_obj.get_matrix(), net);

        double meanI = infection_obj.get_mean();
        double meanC = callose_obj.get_mean();
        file << t << "," << meanI << "," << meanC << "," << drugConc << "\n";

        if (t % 500 == 0) {
            std::cout << "Step " << t << " | Mean Infection: " << meanI
                 << " | Mean Callose: " << meanC << " | Drug: " << drugConc << "\n";
        }

        std::stringstream ss;
        ss << std::setfill('0') << std::setw(5) << t; 

        std::vector<std::vector<double>> drug_grid(cfg.L, std::vector<double>(cfg.L, drugConc));
        
        save_combined_data(
            infection_obj.get_matrix(),
            callose_obj.get_matrix(),
            drug_grid,
            data_dir + "/frame_" + ss.str() + ".csv"
        );
    }
    file.close();
    std::cout << "Simulation finished. Results saved to: results_" << treatment << ".csv\n";
}

#endif