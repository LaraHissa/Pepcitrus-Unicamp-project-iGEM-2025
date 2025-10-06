# infection.py

import numpy as np
from .network import Network
from . import constants

"""
=============================================================================
CLASS INFECTION
=============================================================================
Models the bacterial population dynamics (growth, death, spread) on the 2D grid.
=============================================================================
"""

class Infection:
    def __init__(self, cfg):
        # Parameters copied from config object
        self.L = cfg.L
        self.r = cfg.r
        self.Imax = cfg.Imax
        self.d = cfg.d
        self.deltaI = cfg.deltaI
        
        # Infection matrix (NumPy array)
        self.I = np.zeros((self.L, self.L))

    def initialize(self):
        """Resets the grid and starts the infection at a single random point."""
        self.I.fill(0.0)
        
        # Random starting point
        i0, j0 = np.random.randint(0, self.L, 2)
        self.I[i0, j0] = constants.INITIAL_INFECTION_LOAD

    def spread(self, C, beta, inhibition_factor, net: Network):
        """
        Models the spatial spread of the infection (stochastic).
        Uses C++ logic: P_spread = beta * (1 - inhibFactor) * exp(-5 * C_target)
        """
        newI = np.copy(self.I)
        
        for i in range(self.L):
            for j in range(self.L):
                if self.I[i, j] > 0: # Only infected cells spread
                    for ni, nj in net.get_neighbors(i, j):
                        # Check if target cell is currently uninfected (I[ni, nj] == 0)
                        if newI[ni, nj] < constants.NUMERICAL_EXTINCTION_THRESHOLD: 
                            C_target = C[ni, nj]
                            
                            # Permeability factor: exp(-5 * C)
                            permeability_factor = np.exp(-constants.CALLOSE_SPREAD_SENSITIVITY * C_target)
                            
                            # Full Probability
                            prob = beta * (1.0 - inhibition_factor) * permeability_factor
                            
                            # Stochastic Trial
                            if np.random.rand() < prob:
                                newI[ni, nj] = constants.SPREAD_INFECTION_LOAD 
        self.I = newI

    def update(self, C, drug_conc, is_bactericidal, drug_params):
        """
        Updates the infection load in each cell (Intra-cellular dynamics/ODE integration).
        C++ EDO: dI/dt = Growth - NaturalDeath - CalloseEffect - DrugEffect
        """
        for i in range(self.L):
            for j in range(self.L):
                I_ij = self.I[i, j]
                if I_ij <= constants.NUMERICAL_EXTINCTION_THRESHOLD: 
                    self.I[i, j] = 0.0
                    continue

                C_ij = C[i, j]
                
                # --- General Terms ---
                logistic_growth = self.r * I_ij * (1.0 - I_ij / self.Imax)
                natural_death = self.deltaI * I_ij
                callose_effect = self.d * C_ij * I_ij
                
                dI = 0.0
                
                if drug_conc < 1e-9:
                    # Case 1: No Drug
                    dI = logistic_growth - natural_death - callose_effect
                else:
                    # Calculate Hill factor for drug effect (E_hill)
                    EC50 = drug_params['EC50']
                    hillN = drug_params['hillN']
                    killScale = drug_params['killScale']
                    
                    E_hill = np.power(drug_conc / EC50, hillN) / (np.power(drug_conc / EC50, hillN) + 1.0)
                    E_factor = min(1.0, E_hill * killScale)

                    if is_bactericidal:
                        # Case 2: CTX (Bactericidal - increased mortality)
                        kill_rate = E_factor
                        dI = logistic_growth - natural_death - callose_effect - (kill_rate * I_ij)
                    else:
                        # Case 3: TETRACYCLINE (Bacteriostatic - reduced growth)
                        
                        # Apply inhibition to growth term
                        effective_growth = logistic_growth * (1.0 - E_factor)
                        
                        # Apply active clearing term (Tetracycline only)
                        active_clearing_rate = constants.TETRACYCLINE_ACTIVE_CLEARING * E_factor
                        active_clearing_effect = active_clearing_rate * I_ij
                        
                        dI = effective_growth - natural_death - callose_effect - active_clearing_effect
                
                # Update and clamp values
                self.I[i, j] += dI
                self.I[i, j] = np.clip(self.I[i, j], 0.0, self.Imax)
                
                if self.I[i, j] < constants.NUMERICAL_EXTINCTION_THRESHOLD:
                    self.I[i, j] = 0.0

    def get_mean(self):
        """Calculates the average infection load across the entire grid."""
        return np.mean(self.I)

    def get_matrix(self):
        """Returns the infection matrix (NumPy array)."""
        return self.I