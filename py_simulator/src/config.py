# config.py

"""
=====================================================================================
CENTRAL SIMULATION CONFIGURATION
=====================================================================================
This file serves as the control panel for all experiments.
It defines simulation parameters, dynamic rates, and treatment properties.
=====================================================================================
"""

# --- Drug Parameter Structure (Equivalent to C++ struct drug_params) ---
def get_drug_params(dose, EC50, hillN, killScale, Tmax, halfLife):
    """Returns a dictionary representing a drug's properties."""
    return {
        'dose': dose,
        'EC50': EC50,
        'hillN': hillN,
        'killScale': killScale,
        'Tmax': Tmax,
        'halfLife': halfLife,
    }

# --- Central Configuration (Equivalent to C++ struct config) ---
class Config:
    def __init__(self):
        # --- Grid and Time ---
        self.L = 50                 # grid dimension (LxL)
        self.steps = 1000           # time steps (in days) before treatment
        self.extraSteps = 1500      # time steps (in days) after treatment

        # --- Infection Dynamics ---
        self.beta = 0.07            # base spread probability
        self.r = 0.15               # growth rate
        self.Imax = 1.0             # cell's carrying capacity (max load)
        self.d = 0.7                # efficacy of callose in suppressing infection
        self.deltaI = 0.001         # natural death rate of the 'bacteria'

        # --- Defense Dynamics (Callose) ---
        self.alphaC = 0.6           # callose production rate
        self.deltaC = 0.01          # callose degradation rate 
        self.Climit = 1.0           # max callose level per cell
        self.signalR = 6            # signaling radius to activate defense

        # --- Treatment Settings (Dynamic parameters) ---
        # Note: Doses are normalized in the original C++ code (e.g., 15.0 / 80.0)
        self.CTXparams = get_drug_params(
            dose=15.0 / 80.0, EC50=0.40, hillN=2.0, killScale=3.0, Tmax=14.0, halfLife=100.0
        )
        self.TETRACYCLINEparams = get_drug_params(
            dose=150.0 / 80.0, EC50=1.0, hillN=2.0, killScale=3.0, Tmax=14.0, halfLife=200.0
        )