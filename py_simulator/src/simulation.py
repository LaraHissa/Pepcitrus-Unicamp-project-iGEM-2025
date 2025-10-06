# simulation.py

import numpy as np
import os
import csv
from .config import Config
from .network import Network
from .infection import Infection
from .callose import Callose
from .therapeutic import Therapeutic

"""
==============================================================================
CLASS SIMULATION
==============================================================================
The main class that coordinates the entire simulation.
Initializes components, manages the time loop, applies treatments, and logs data.
==================================================================================
"""

class Simulation:
    def __init__(self, cfg: Config):
        # --- Model Components ---
        self.cfg = cfg
        self.net = Network(cfg.L, cfg.signalR)
        self.infection_obj = Infection(cfg)
        self.callose_obj = Callose(cfg)
        
        # --- Treatment Tracking ---
        self.dose_times = []  # Stores time steps when a dose was applied

    def calculate_total_concentration(self, params, global_time, treatment_start):
        """
        Calculates the total drug concentration at the current time by summing 
        the effects of all previous doses, using the Therapeutic class.
        """
        total_concentration = 0.0
        for dose_time in self.dose_times:
            # timeSinceDose = globalTime - (treatmentStart + doseTime)
            time_since_dose = global_time - (treatment_start + dose_time)
            
            total_concentration += Therapeutic.get_concentration(
                params['dose'], time_since_dose, params['Tmax'], params['halfLife']
            )
        return total_concentration

    def save_combined_data(self, infection, callose, drug_conc, filename):
        """
        Helper function to save the combined state of all grids to a single file.
        drug_conc is a scalar, but needs to be expanded to an L x L grid for file structure.
        """
        # Create output directory if it doesn't exist (assuming frame data structure)
        data_dir = os.path.dirname(filename)
        os.makedirs(data_dir, exist_ok=True)
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["i", "j", "infection", "callose", "drug"])
            
            L = self.cfg.L
            for i in range(L):
                for j in range(L):
                    writer.writerow([i, j, infection[i, j], callose[i, j], drug_conc])


    def run(self, treatment_scenario):
        """
        Executes the full simulation for a specific treatment scenario.
        """
        self.infection_obj.initialize()
        self.callose_obj.initialize()
        self.dose_times.clear()

        # Define data output paths
        data_dir = f"data_{treatment_scenario}"
        results_file = f"results_{treatment_scenario}.csv"
        
        print(f"Saving frame data to directory: {data_dir}")

        with open(results_file, 'w', newline='') as f_results:
            writer = csv.writer(f_results)
            writer.writerow(["time", "mean_infection", "mean_callose", "drug_concentration"])

            treatment_start = self.cfg.steps
            total_steps = self.cfg.steps + self.cfg.extraSteps
            
            is_bactericidal = (treatment_scenario == "ctx")

            for t in range(total_steps):
                drug_conc = 0.0
                inhibition_factor = 0.0
                
                # 1. Drug Administration (Single dose at treatment_start, t == treatmentStart)
                if treatment_scenario != "control" and t == treatment_start:
                    self.dose_times.append(0) # Store relative time of dose application

                # 2. Calculate Drug Concentration and Inhibition Factor
                current_drug_params = None
                if treatment_scenario == "tetra":
                    current_drug_params = self.cfg.TETRACYCLINEparams
                elif treatment_scenario == "ctx":
                    current_drug_params = self.cfg.CTXparams

                if current_drug_params:
                    # Get concentration from all previous doses
                    drug_conc = self.calculate_total_concentration(current_drug_params, t, treatment_start)
                    
                    # Calculate inhibition factor based on TETRA parameters (used for Spread)
                    if treatment_scenario == "tetra" and drug_conc > 1e-9:
                        p = self.cfg.TETRACYCLINEparams
                        E_hill = self.net.hill_function(drug_conc, p['EC50'], p['hillN'])
                        inhibition_factor = min(1.0, E_hill * p['killScale'])

                # 3. Infection Spread (Stochastic step)
                beta = self.cfg.beta
                self.infection_obj.spread(self.callose_obj.get_matrix(), beta, inhibition_factor, self.net)

                # 4. Intra-cellular Update (Deterministic step)
                if treatment_scenario == "ctx":
                    # CTX uses bactericidal logic (drugConc != 0 if a dose was applied)
                    self.infection_obj.update(self.callose_obj.get_matrix(), drug_conc, True, self.cfg.CTXparams)
                else:
                    # TETRA uses bacteriostatic logic (drugConc is the non-zero value if tetra)
                    conc_for_update = drug_conc if treatment_scenario == "tetra" else 0.0
                    self.infection_obj.update(self.callose_obj.get_matrix(), conc_for_update, False, self.cfg.TETRACYCLINEparams)
                
                # 5. Callose Update
                self.callose_obj.update(self.infection_obj.get_matrix(), self.net)

                # 6. Log Data (Mean values for plot)
                meanI = self.infection_obj.get_mean()
                meanC = self.callose_obj.get_mean()
                writer.writerow([t, meanI, meanC, drug_conc])

                # 7. Save Frame Data (For video generation)
                if t % 1 == 0: # Save every day (frame)
                    # Frame filename format: frame_00000.csv
                    frame_filename = os.path.join(data_dir, f"frame_{t:05d}.csv")
                    self.save_combined_data(
                        self.infection_obj.get_matrix(),
                        self.callose_obj.get_matrix(),
                        drug_conc,
                        frame_filename
                    )

                if t % 500 == 0:
                    print(f"Step {t} | Mean Infection: {meanI:.4f} | Mean Callose: {meanC:.4f} | Drug: {drug_conc:.4f}")

            print(f"Simulation finished. Results saved to: {results_file}")