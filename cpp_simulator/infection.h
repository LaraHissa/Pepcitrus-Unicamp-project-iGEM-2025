#ifndef INFECTION_H
#define INFECTION_H

#include "config.h"
#include "network.h"
#include "constants.h" 
#include <vector>
#include <random>
#include <cmath>
#include <algorithm>
#include <chrono>   

/*
 * =====================================================================================
 *                                  CLASS INFECTION
 * =====================================================================================
 * Models the bacterial population dynamics on the 2D grid.
 * Handles local growth, natural death, spatial spreading, and responses
 * to treatments and host defense.
 * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: June 14, 2025
 * Last Modified: September 21, 2025.
 * =====================================================================================
 */

class infection {
private:
    std::vector<std::vector<double>> I; //matrix that stores the infection load in each grid site
    int L;
    // --- Model Parameters (copied from config) ---
    double r, Imax, d, deltaI; 
    std::mt19937 gen;
    std::uniform_real_distribution<> dis;

public:
    infection(const config& cfg); //constructor that initializes the model with simulation parameters
    void initialize(); //resets the grid and starts the infection at a single random point
    void spread(const std::vector<std::vector<double>>& C, double beta, double inhibitionFactor, const network& net); //models the spatial spread of the infection to neighboring cells
    void update(const std::vector<std::vector<double>>& C, double drugConc, bool isBactericidal, const drug_params& drugParams);  //updates the infection load in each cell according to local dynamics.
    double get_mean() const;  //calculates the average infection load across the entire grid
    std::vector<std::vector<double>>& get_matrix(); //returns a reference to the infection matrix for other classes to read
};

// --- Functions Bodies ---

inline infection::infection(const config& cfg)
    : L(cfg.L), r(cfg.r), Imax(cfg.Imax), d(cfg.d), deltaI(cfg.deltaI), dis(0.0, 1.0) {
    I.assign(L, std::vector<double>(L, 0.0));
    gen.seed(std::chrono::high_resolution_clock::now().time_since_epoch().count());
}

inline void infection::initialize() {
    I.assign(L, std::vector<double>(L, 0.0));
    int i0 = gen() % L;
    int j0 = gen() % L;
    I[i0][j0] = model_constants::INITIAL_INFECTION_LOAD;
}

inline void infection::spread(const std::vector<std::vector<double>>& C, double beta, double inhibitionFactor, const network& net) {
    std::vector<std::vector<double>> newI = I;
    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            if (I[i][j] > 0) {
                for (auto [ni, nj] : net.get_neighbors(i, j)) {
                    if (newI[ni][nj] == 0) {
                        double prob = beta * (1.0 - inhibitionFactor) * exp(-5 * C[ni][nj]);
                        if (dis(gen) < prob) {
                            newI[ni][nj] = model_constants::SPREAD_INFECTION_LOAD; 
                        }
                    }
                }
            }
        }
    }
    I = newI;
}

inline void infection::update(const std::vector<std::vector<double>>& C, double drugConc, bool isBactericidal, const drug_params& drugParams) {
    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            if (I[i][j] <= 0) continue;
            
            double growth = r * I[i][j] * (1.0 - I[i][j] / Imax);
            double naturalDeath = deltaI * I[i][j];
            double baseCalloseEffect = d * C[i][j] * I[i][j];
            
            double dI = 0.0;

            if (drugConc < 1e-9) {
                dI = growth - naturalDeath - baseCalloseEffect;

            } else {
                if (isBactericidal) {
                    double killFraction = pow(drugConc / drugParams.EC50, drugParams.hillN) /
                                          (pow(drugConc / drugParams.EC50, drugParams.hillN) + 1.0);
                    killFraction *= drugParams.killScale;
                    dI = growth - naturalDeath - baseCalloseEffect - (std::min(1.0, killFraction) * I[i][j]);

                } else {
                    double inhibition = pow(drugConc / drugParams.EC50, drugParams.hillN) /
                                        (pow(drugConc / drugParams.EC50, drugParams.hillN) + 1.0);
                    inhibition *= drugParams.killScale;
                    inhibition = std::min(1.0, inhibition);

                    double effectiveGrowth = growth * (1.0 - inhibition);
                    double activeClearingEffect = (model_constants::TETRACYCLINE_ACTIVE_CLEARING * inhibition) * I[i][j];
                    
                    dI = effectiveGrowth - naturalDeath - baseCalloseEffect - activeClearingEffect;
                }
            }

            I[i][j] += dI;
            if (I[i][j] < model_constants::NUMERICAL_EXTINCTION_THRESHOLD) I[i][j] = 0.0;
            if (I[i][j] > Imax) I[i][j] = Imax;
        }
    }
}

inline double infection::get_mean() const {
    double total = 0.0;
    for (const auto& row : I) {
        for (double val : row) {
            total += val;
        }
    }
    return total / (L * L);
}

inline std::vector<std::vector<double>>& infection::get_matrix() { return I; }

#endif