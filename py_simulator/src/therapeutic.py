# therapeutic.py

import numpy as np

"""
=============================================================================
CLASS THERAPEUTIC
=============================================================================
A utility class for pharmacokinetic (PK) calculations.
Models how drug concentration changes over time (linear absorption, exponential elimination).
=============================================================================
"""

class Therapeutic:
    @staticmethod
    def get_concentration(dose, time_since_dose, Tmax, halfLife):
        """
        Calculates drug concentration over time using a simplified PK model.
        Assumes linear absorption and first-order elimination.
        """
        if time_since_dose < 0.0:
            return 0.0

        # --- Absorption Phase ---
        if time_since_dose <= Tmax:
            # D(t') = D_peak * (t' / Tmax)
            return dose * (time_since_dose / Tmax)
        
        # --- Elimination Phase ---
        else:
            # k = ln(2) / halfLife
            k = np.log(2.0) / halfLife
            # D(t') = D_peak * exp(-k * (t' - Tmax))
            return dose * np.exp(-k * (time_since_dose - Tmax))