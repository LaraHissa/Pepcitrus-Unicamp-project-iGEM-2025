# 🍊 Pepcitrus UNICAMP 2025: Citrus Greening Cellular Automaton Model (SIC) + Treatment Simulator

![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)
![Dependencies: NumPy](https://img.shields.io/badge/Dependencies-NumPy-D00064.svg)
![Model: Citrus Greening Simulation](https://img.shields.io/badge/Model-Citrus%20Greening%20Simulation-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Abstract

This repository contains the source code for the computational model developed by team **Pepcitrus UNICAMP** for the iGEM 2025 competition. Our project introduces a cellular automaton-based model that simulates the progression of Citrus Greening within the plant's phloem. It serves as a "virtual laboratory" to investigate pathogen dynamics, host immune responses, and the therapeutic efficacy of our antimicrobial peptide, CTX. This model was designed to bridge the gap between fundamental research and practical, field-relevant disease management strategies. (Initial model in C++, translated to Python for accessibility).

---

## Table of Contents

1. [About the Project](#about-the-project)
2. [Model Features](#model-features)
3. [Getting Started](#getting-started)
   * [Prerequisites](#prerequisites)
   * [Project Structure](#project-structure)
4. [How to Run the Simulation](#how-to-run-the-simulation)
5. [Model Architecture](#model-architecture)
6. [Simulation Output](#simulation-output)
7. [License](#license)
8. [Contact & Acknowledgments](#contact--acknowledgments)

---

## About the Project

Citrus Greening is the most destructive disease threatening global citrus production. While vector control is essential, it alone is insufficient to save already infected trees. Our iGEM project, Pepcitrus, aims to develop a novel therapeutic based on an antimicrobial peptide (CTX) to treat infected plants from the inside out.

To guide our experimental design and understand the complex dynamics of the disease, we developed this computational model. It allows us to explore spatial-temporal patterns of bacterial spread, quantify the impact of the plant's immune response (**callose deposition**), and, most importantly, generate testable hypotheses about the efficacy and optimal application strategy for our CTX peptide and other treatments like Oxytetracycline.

For a full description of our project, please visit our **Official iGEM Wiki**.

---

## Model Features

* **Spatial-Temporal Dynamics:** Uses a **2D cellular automaton** (50x50 grid) to model how the infection spreads from cell to cell over time. 
* **Modular Design:** The system is broken down into logical, interacting modules (`Infection`, `Callose`, `Therapeutic`). 
* **Pharmacodynamics:** Accurately models the distinct mechanisms of action for our **bactericidal** peptide (CTX) and a benchmark **bacteriostatic** antibiotic (Oxytetracycline). 
* **Highly Configurable:** All key biological and simulation parameters are centralized in the **`config.py`** file for easy experimentation. 
* **Performance:** Written in Python and utilizes **NumPy** for efficient grid operations and fast matrix calculations.

---

## Getting Started

Follow these instructions to set up and run the simulator on your local machine.

### Prerequisites

You need **Python 3** and the **NumPy** library.

1. **Install Python:** Ensure you have Python 3 installed. 
2. **Install NumPy:** Open your terminal and install the required dependency:
   ```bash
   pip install numpy
   ```

---

### Project Structure

The project uses a standard Python package structure. The core logic resides in the `src/` directory, which allows for clean relative imports.

```
py_simulator/
├── run_simulation.py     <-- Main execution script
└── src/                  <-- Core simulation package
    ├── __init__.py       <-- Required for Python (can be empty)
    ├── constants.py
    ├── config.py
    ├── therapeutic.py
    ├── infection.py
    ├── callose.py
    ├── network.py
    └── simulation.py
```

---

## How to Run the Simulation

The simulation is executed through an interactive command-line menu.

1. **Navigate** to the main project directory (`py_simulator/`):
   ```bash
   cd py_simulator
   ```

2. **Execute** the main script using Python 3:
   ```bash
   python3 run_simulation.py
   ```

3. You will be prompted to **select a scenario**. The available options are:
   * `control`: Simulates the disease progression with no drug treatment. 
   * `ctx`: Simulates the application of our bactericidal CTX peptide. 
   * `tetra`: Simulates the application of the bacteriostatic Oxytetracycline antibiotic. 
   * `all`: Runs all three scenarios sequentially.

---

## Model Architecture

The code is organized into several modules within the `src` package:

* **`config.py`** — The central control panel. Modify parameters here to run different experiments. 
* **`constants.py`** — Defines fixed, non-adjustable biological and numerical constants. 
* **`network.py`** — Manages the 2D grid topology (Von Neumann neighbors) and mathematical functions (e.g., Hill function). 
* **`infection.py`** — Contains the `Infection` class, which models bacterial population dynamics (growth, death, and spatial spread). 
* **`callose.py`** — Contains the `Callose` class, modeling the host's immune defense response dynamics. 
* **`therapeutic.py`** — A utility class for Pharmacokinetic (PK) calculations (drug concentration over time). 
* **`simulation.py`** — The main coordination class that manages the time loop and orchestrates interactions between all components.

---

## Simulation Output

The simulation generates two primary forms of output data, saved directly into the execution folder:

1. **Time-Series Data:** 
   A single CSV file named `results_[treatment].csv` (e.g., `results_ctx.csv`). 
   It contains the average state of the grid at each time step — useful for plotting trends. 
   Columns:
   * `time`: The current time step (day) 
   * `mean_infection`: The average bacterial load across all cells 
   * `mean_callose`: The average callose level across all cells 
   * `drug_concentration`: The current systemic drug concentration 

2. **Frame-by-Frame Grid Data:** 
   A new directory named `data_[treatment]` is created. Inside, it saves a snapshot of the entire grid state at each time step in a separate CSV file (`frame_xxxxx.csv`). 
   Columns:
   * `i, j`: The coordinates of the cell on the grid 
   * `infection, callose, drug`: The state values for that specific cell 

---

## License & Attribution

Developed by the **iGEM UNICAMP 2025 Team**, as part of the **PepCitrus Project**, focused on computational modeling of *Citrus Greening (Huanglongbing)* and antibiotic treatment strategies. 

© 2025 iGEM UNICAMP. 
Licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Contact & Acknowledgments

This model was developed by **Pepcitrus UNICAMP iGEM 2025 team**.

For questions or collaborations, please contact: 
 `l171513@dac.unicamp.br` or `igem@unicamp.br`

We would like to thank the iGEM Foundation and all our sponsors for making this competition possible.
