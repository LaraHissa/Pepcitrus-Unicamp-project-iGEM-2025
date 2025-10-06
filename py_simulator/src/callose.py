# callose.py

import numpy as np
from .network import Network

"""
=============================================================================
CLASS CALLOSE
=============================================================================
Models the dynamics of the host defense response (callose deposition).
Callose is produced by healthy neighbors in response to the infection signal.
=============================================================================
"""

class Callose:
    def __init__(self, cfg):
        # Parameters copied from config object
        self.L = cfg.L
        self.alphaC = cfg.alphaC
        self.deltaC = cfg.deltaC
        self.Climit = cfg.Climit
        
        # Callose matrix (NumPy array)
        self.C = np.zeros((self.L, self.L))

    def initialize(self):
        """Resets the callose grid to zero."""
        self.C.fill(0.0)

    def update(self, I, net: Network):
        """
        Updates the callose concentration based on local signal and degradation.
        C++ EDO: dC/dt = alphaC * H(S_local) - deltaC * C
        """
        # 1. Apply natural degradation to all cells (first term of the C++ loop)
        newC = self.C - self.deltaC * self.C
        
        # 2. Trigger production at the infection front (Iterative part)
        for i in range(self.L):
            for j in range(self.L):
                if I[i, j] > 0: # If this cell is infected (source of signal)
                    # Look at its neighbors (target for production)
                    for ni, nj in net.get_neighbors(i, j):
                        if I[ni, nj] == 0: # If the neighbor is HEALTHY...
                            
                            # Get local signal around the healthy neighbor (Manhattan distance)
                            signal = net.get_local_signal(ni, nj, I)
                            
                            # Calculate production via Hill function
                            production = self.alphaC * net.hill_function(signal)
                            
                            newC[ni, nj] += production
                            
        # 3. Enforce physical limits (Climit and 0)
        self.C = np.clip(newC, 0.0, self.Climit)

    def get_mean(self):
        """Calculates the average callose concentration across the entire grid."""
        return np.mean(self.C)

    def get_matrix(self):
        """Returns the callose matrix (NumPy array)."""
        return self.C