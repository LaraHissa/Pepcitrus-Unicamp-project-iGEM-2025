
#ifndef THERAPEUTIC_H
#define THERAPEUTIC_H

#include <cmath>

/*
 * =============================================================================
 *                              CLASS THERAPEUTIC
 * =============================================================================
 * A utility class for pharmacokinetic (PK) calculations.
 * This class provides static methods to model how drug concentration
 * changes over time within the host system.
 * 
 * Created by: Pepcitrus Unicamp - iGEM project
 * Created on: July 28, 2025
 * Last Modified: September 21,2025.
 * =============================================================================
 */


class therapeutic {
public:
    // calculates drug concentration over time using a simplified PK model
    static double get_concentration(double dose, double timeSinceDose, double Tmax, double halfLife) {
        if (timeSinceDose < 0.0) return 0.0;
        if (timeSinceDose <= Tmax) return dose * (timeSinceDose / Tmax);
        double k = log(2.0) / halfLife;
        return dose * exp(-k * (timeSinceDose - Tmax));
    }
};

#endif