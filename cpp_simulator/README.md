# 🍊 Pepcitrus UNICAMP 2025: Citrus Greening Cellular Automaton Model (SIC) + Treatment Simulator

![Language: C++](https://img.shields.io/badge/Language-C++-blue.svg)
![Model: Citrus Greening Simulation](https://img.shields.io/badge/Model-Citrus%20Greening%20Simulation-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Abstract

This repository contains the source code for the computational model developed by team **Pepcitrus UNICAMP** for the iGEM 2025 competition. Our project introduces a cellular automaton-based model that simulates the progression of Citrus Greening within the plant's phloem. It serves as a "virtual laboratory" to investigate pathogen dynamics, host immune responses, and the therapeutic efficacy of our antimicrobial peptide, CTX. This model was designed to bridge the gap between fundamental research and practical, field-relevant disease management strategies.

---

## Table of Contents

1.  [About the Project](#about-the-project)
2.  [Model Features](#model-features)
3.  [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Compilation](#compilation)
4.  [How to Run the Simulation](#how-to-run-the-simulation)
5.  [Model Architecture](#model-architecture)
6.  [Simulation Output](#simulation-output)
7.  [License](#license)
8.  [Contact & Acknowledgments](#contact--acknowledgments)

---

## About the Project

Citrus Greening, or HLB, is the most destructive disease threatening global citrus production. While vector control is essential, it alone is insufficient to save already infected trees. Our iGEM project, Pepcitrus, aims to develop a novel therapeutic based on an antimicrobial peptide (CTX) to treat infected plants from the inside out.

To guide our experimental design and understand the complex dynamics of the disease, we developed this computational model. It allows us to explore spatial-temporal patterns of bacterial spread, quantify the impact of the plant's immune response (callose deposition), and, most importantly, generate testable hypotheses about the efficacy and optimal application strategy for our CTX peptide and other treatments like Oxytetracycline.

For a full description of our project, please visit our **Official iGEM Wiki**.

## Model Features

* **Spatial-Temporal Dynamics:** Utilizes a 2D cellular automaton to model how the infection spreads from cell to cell over time.
* **Modular Design:** The system is broken down into logical, interacting modules:
    1.  `Infection`: Manages bacterial growth, death, and spatial spread.
    2.  `Callose`: Simulates the primary host defense mechanism.
    3.  `Therapeutic`: Models the pharmacokinetics and pharmacodynamics of treatments.
* **Detailed Pharmacodynamics:** Accurately models the distinct mechanisms of action for our **bactericidal** peptide (CTX) and a benchmark **bacteriostatic** antibiotic (Oxytetracycline).
* **Highly Configurable:** All key biological and simulation parameters are centralized in the `config.h` file, allowing for easy experimentation and calibration without altering the core logic.
* **Efficient & Portable:** Written in modern C++ for high performance, with no external dependencies beyond a standard C++ compiler.

## Getting Started

Follow these instructions to compile and run the simulator on your local machine.

### Prerequisites

You will need a C++ compiler that supports the C++17 standard. We recommend `g++`.

* **On Ubuntu/Debian:**
    ```sh
    sudo apt-get update
    sudo apt-get install build-essential
    ```
* **On macOS:** Install Xcode Command Line Tools.
    ```sh
    xcode-select --install
    ```
* **On Windows:** We recommend using WSL (Windows Subsystem for Linux) and following the Ubuntu instructions.

### Compilation

1.  Clone the repository:
    ```sh
    git clone https://github.com/LaraHissa/Pepcitrus-Unicamp-project-iGEM-2025.git
    cd cpp_simulator
    ```

2.  Compile the source code using the `main.cpp` file.
    ```sh
    g++ main.cpp -o simulator -std=c++17
    ```
    * `-o simulator`: Specifies the output executable name.
    * `-std=c++17`: Ensures C++17 standard compatibility.
 

## How to Run the Simulation

Once compiled, you can run the simulation from your terminal. The program will present an interactive menu to choose the desired treatment scenario.

1.  Execute the compiled program:
    ```sh
    ./simulator
    ```

2.  You will be prompted to select a scenario. The available options are:
    * `control`: Simulates the disease progression with no drug treatment.
    * `ctx`: Simulates the application of our bactericidal CTX peptide after an initial infection period.
    * `tetra`: Simulates the application of the bacteriostatic Oxytetracycline antibiotic.

3.  After you enter your choice, the simulation will begin. Progress will be printed to the console, and output data will be saved to the directory from which you ran the program.

## Model Architecture

The code is organized into several header files (`.h`) for clarity and modularity:

* `config.h`: The central control panel. **Modify parameters here to run different experiments.**
* `constants.h`: Defines fixed biological and numerical constants that are not meant to be changed between experiments.
* `network.h`: Manages the 2D grid topology and neighborhood interactions.
* `infection.h`: Contains the `infection` class, which models all bacterial population dynamics.
* `callose.h`: Contains the `callose` class, modeling the host defense response.
* `therapeutic.h`: A utility class for pharmacokinetic (PK) calculations.
* `simulation.h`: The main coordinator class that manages the time loop and interactions between all other components.
* `main.cpp`: The program's entry point, containing the user menu and initialization logic.

## Simulation Output

The simulation generates two primary forms of output:

1.  **Time-Series Data:** A single CSV file named `results_[treatment].csv` (e.g., `results_ctx.csv`). It contains the average state of the grid at each time step.
    * `time`: The current time step (day).
    * `mean_infection`: The average bacterial load across all cells.
    * `mean_callose`: The average callose level across all cells.
    * `drug_concentration`: The current systemic drug concentration.

2.  **Frame-by-Frame Grid Data:** A new directory named `data_[treatment]` is created. Inside, it saves a snapshot of the entire grid state at each time step in a separate CSV file (`frame_xxxxx.csv`). This data can be used to generate videos and spatial plots of the simulation.
    * `i, j`: The coordinates of the cell on the grid.
    * `infection, callose, drug`: The state values for that specific cell.

## License & Attribution

Developed by the **iGEM UNICAMP 2025 Team** 
Part of the **PepCitrus Project**, focused on computational modeling of *Citrus Greening (Huanglongbing)* and antibiotic treatment strategies. 
© 2025 iGEM UNICAMP. 
Licensed under the [MIT License](https://opensource.org/licenses/MIT). 


## Contact & Acknowledgments

This model was developed by **Pepcitrus UNICAMP iGEM 2025 team**.

For questions or collaborations, please contact us at `l171513@dac.unicamp.br` or `igem@unicamp.br`.

We would like to thank the iGEM Foundation and all the sponsors for making this competition possible.
