

#ifndef NETWORK_H
#define NETWORK_H

#include "constants.h"
#include <vector>
#include <utility>
#include <cmath>
#include <algorithm>

/*
 * =============================================================================
 *                              CLASS NETWORK
 * =============================================================================
 * Manages the 2D grid topology and neighborhood interactions. 
 * Also includes some mathematical functions
 * 
 * Created by: Pepcitrus Unicamp - iGEM project 
 * Created on: June 11, 2025
 * Last Modified: September 21,2025.
 * ==========================================================================
 */


class network {
private:
    int gridSize; //grid dimension  
    int signalRadius; //signal percpetion radius

public:
    network(int L, int R); //constructor that initizalizes the network with its dimensions
    std::vector<std::pair<int, int>> get_neighbors(int i, int j) const; // returns the 4 direct neighbors of a cell
    double get_local_signal(int i, int j, const std::vector<std::vector<double>>& I) const; //calculates the average infection signal in a neighborhood
    double hill_function(double x, 
                         double x0 = model_constants::CALLOSE_SIGNAL_EC50, 
                         double n = model_constants::CALLOSE_HILL_COEFFICIENT) const; 
};


// --- Functions Bodies ---
inline network::network(int L, int R) : gridSize(L), signalRadius(R) {}

inline std::vector<std::pair<int, int>> network::get_neighbors(int i, int j) const {
    std::vector<std::pair<int, int>> result;
    int dx[] = {1, -1, 0, 0};
    int dy[] = {0, 0, 1, -1};
    for (int k = 0; k < 4; ++k) {
      
        int li = (i + dx[k] + gridSize) % gridSize;
        int lj = (j + dy[k] + gridSize) % gridSize;
        result.push_back({li, lj});
    }
    return result;
}
inline double network::get_local_signal(int i, int j, const std::vector<std::vector<double>>& I) const {
    double total = 0.0;
    int count = 0;
    for (int di = -signalRadius; di <= signalRadius; ++di) {
        for (int dj = -signalRadius; dj <= signalRadius; ++dj) {
            if (abs(di) + abs(dj) <= signalRadius) {
                int li = i + di;
                int lj = j + dj;
                if (li >= 0 && li < gridSize && lj >= 0 && lj < gridSize) {
                    total += I[li][lj];
                    count++;
                }
            }
        }
    }
    return total / std::max(count, 1);
}

inline double network::hill_function(double x, double x0, double n) const {
    double x_n = pow(x, n);   
    double x0_n = pow(x0, n); 
    return x_n / (x_n + x0_n );
}

#endif