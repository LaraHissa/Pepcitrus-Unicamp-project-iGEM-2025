# network.py

import numpy as np
from . import constants

"""
=============================================================================
CLASS NETWORK
=============================================================================
Manages the 2D grid topology, neighborhood interactions (Von Neumann, Manhattan), 
and common mathematical functions (Hill function).
==========================================================================
"""

class Network:
    def __init__(self, L, R):
        self.grid_size = L
        self.signal_radius = R

    def get_neighbors(self, i, j):
        """
        Returns the 4 direct neighbors (Von Neumann) with periodic boundary conditions.
        """
        neighbors = []
        dx = [1, -1, 0, 0]  # Vertical (i) displacement
        dy = [0, 0, 1, -1]  # Horizontal (j) displacement
        
        for k in range(4):
            # Applies periodic boundary conditions (wraps around)
            ni = (i + dx[k] + self.grid_size) % self.grid_size
            nj = (j + dy[k] + self.grid_size) % self.grid_size
            neighbors.append((ni, nj))
        return neighbors

    def get_local_signal(self, i, j, I):
        """
        Calculates the average infection signal (I) in a diamond-shaped neighborhood (Manhattan distance).
        Note: I is expected to be a NumPy array.
        """
        total = 0.0
        count = 0
        
        R = self.signal_radius
        
        # Iterates over the square box defined by R
        for di in range(-R, R + 1):
            for dj in range(-R, R + 1):
                # Check for Manhattan distance condition: |di| + |dj| <= R
                if abs(di) + abs(dj) <= R:
                    li = i + di
                    lj = j + dj
                    
                    # Check for non-periodic boundaries (signal does not wrap around)
                    if 0 <= li < self.grid_size and 0 <= lj < self.grid_size:
                        total += I[li, lj]
                        count += 1
                        
        return total / max(count, 1)

    def hill_function(self, x, x0=constants.CALLOSE_SIGNAL_EC50, n=constants.CALLOSE_HILL_COEFFICIENT):
        """
        Calculates the general Hill function: x^n / (x^n + x0^n).
        Supports NumPy array input (x) for vectorized calculation.
        """
        x_n = np.power(x, n)
        x0_n = np.power(x0, n)
        return x_n / (x_n + x0_n)