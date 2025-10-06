# constants.py

"""
=====================================================================================
MODEL'S FUNDAMENTAL CONSTANTS
=====================================================================================
This file defines the fixed and non-adjustable constants of the model, 
representing core biological or numerical hypotheses.

For adjustable experiment parameters, see the config module.
=====================================================================================
"""

# --- Initial Conditions and Spread ---
INITIAL_INFECTION_LOAD = 0.1         # Initial infection load applied to a single cell at the beginning.
SPREAD_INFECTION_LOAD = 0.05         # Infection load transferred to a neighboring cell during a spread event.

# --- Callose Dynamics (Hill Function Parameters) ---
CALLOSE_SIGNAL_EC50 = 0.5            # Half-activation point (EC50) for callose production via the Hill function.
CALLOSE_HILL_COEFFICIENT = 2.0       # Hill coefficient for callose production.

# --- Therapeutic Parameters ---
TETRACYCLINE_ACTIVE_CLEARING = 0.015 # Active bacterial clearing factor induced by bacteriostatic treatment (Tetracycline).

# --- Numerical Stability ---
NUMERICAL_EXTINCTION_THRESHOLD = 1e-3 # Threshold below which bacterial load is considered zero.

# --- Hardcoded value used in Infection::spread (permeability) ---
# Represents the exponential sensitivity of spread to callose barrier.
CALLOSE_SPREAD_SENSITIVITY = 5.0