
#ifndef CALLOSE_H
#define CALLOSE_H

#include "config.h"
#include "network.h"
#include <vector>

/*
 * =====================================================================================
 *                          CLASS CALLOSE
 * =====================================================================================
 * Models the dynamics of the host defense response (callose deposition).
 * Responsible for callose production in response to infection and its natural
 * degradation over time.
 * 
 * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: June 15, 2025
 * Last Modified: September 21,2025.
 * =====================================================================================
 */

class callose {
private:
    std::vector<std::vector<double>> C; // matrix that stores the callose concentration
    int L; // grid dimension
    double alphaC, deltaC, Climit; //model parameters (copied from config)
public:
    callose(const config& cfg); //constructor that initializes the model with simulation parameters
    void initialize(); // resets the callose grid to zero.
    void update(const std::vector<std::vector<double>>& I, const network& net); //updates the callose concentration in each cell based on the local infection signal
    double get_mean() const; //calculates the average callose concentration across the entire grid
    std::vector<std::vector<double>>& get_matrix(); //returns a reference to the callose matrix for other classes to read
};


// --- Functions Bodies ---

inline callose::callose(const config& cfg)
    : L(cfg.L), alphaC(cfg.alphaC), deltaC(cfg.deltaC), Climit(cfg.Climit) {
    C.assign(L, std::vector<double>(L, 0.0));
}

inline void callose::initialize() { C.assign(L, std::vector<double>(L, 0.0)); }

inline void callose::update(const std::vector<std::vector<double>>& I, const network& net) {
    std::vector<std::vector<double>> newC = C;

    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            newC[i][j] -= deltaC * C[i][j];
        }
    }

    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            if (I[i][j] > 0) {
                for (auto const& [ni, nj] : net.get_neighbors(i, j)) {
                    if (I[ni][nj] == 0) {
                        double signal = net.get_local_signal(ni, nj, I);
                        double production = alphaC * net.hill_function(signal);
                        newC[ni][nj] += production;
                    }
                }
            }
        }
    }

    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < L; ++j) {
            if (newC[i][j] > Climit) {
                newC[i][j] = Climit;
            }
            if (newC[i][j] < 0) {
                newC[i][j] = 0;
            }
        }
    }
    C = newC;
}

inline double callose::get_mean() const {
    double total = 0.0;
    for (const auto& row : C) {
        for (double val : row) {
            total += val;
        }
    }
    return total / (L * L);
}

inline std::vector<std::vector<double>>& callose::get_matrix() { return C; }

#endif