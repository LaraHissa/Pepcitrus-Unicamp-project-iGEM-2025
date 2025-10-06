# 🍊 PepCitrus UNICAMP 2025 – Integrated Simulation Framework

![Language: C++ & Python](https://img.shields.io/badge/Languages-C++%20%26%20Python-blue.svg)
![Model: Citrus Greening](https://img.shields.io/badge/Model-Citrus%20Greening%20Simulation-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This repository contains the complete computational modeling framework developed by the **iGEM UNICAMP 2025 Team** for the **PepCitrus Project**.  
It simulates the progression and treatment of **Citrus Greening** disease using cellular automata producing both numerical and visual results.

The system is divided into **three main directories**, each serving a specific purpose but designed to work seamlessly together.

---

1. `cpp_simulator/` — Core Simulation Engine (C++)

This is the **core of the project**, the high-performance cellular automaton that models infection spread and treatment effects.

- Written in **C++** for maximum **speed and efficiency**.  
- Generates all simulation outputs (CSV files and spatial data).  
- Directly feeds the Python analysis module with structured data.

We recommend run our simulation in C++ version because:
- It runs simulations **significantly faster** than the Python version.  
- It produces **consistent, high-precision outputs** ready for post-processing.  

For detailed build and usage instructions, see [`cpp_simulator/README.md`](cpp_simulator/README.md).

---

## 2. `analysis/` — Data Analysis & Visualization (Python)

This folder contains the **data analysis tools** that take the raw simulation results from the C++ engine and convert them into:
- ** Time evolution Plots (PDFs)** showing infection and callose trends over time.
- **Simulation videos (MP4)** showing the spatial spread and drug effects.

The scripts in this directory are **automatically linked** to the C++ simulator’s output folders.  
After each simulation, you can run `analyze.py` to generate the plots and videos — no manual data handling required.

For more information, see [`analysis/README.md`](analysis/README.md).

---

## 3. `python_version/` — Educational Python Implementation

This is a **simplified, pure Python version** of the simulator.  
It reproduces the same cellular automaton logic as the C++ version, but in a slower and more readable form ideal for:
- Students or collaborators who are **not familiar with C++**.  
- Quick tests or demonstrations without compiling the main code.  
- Prototyping and parameter experimentation.

⚠️ **Note:**  
This version is not optimized for performance — large-scale simulations may run significantly slower than the C++ version.

---

## Integration Workflow

The three parts of the system are designed to work together:

```
[C++ Simulator]  →  generates data  →  [Python Analysis]  →  produces plots & videos
                         │
                         └── [Python Version] (optional for understanding & testing)
```



##  Related Links

-  **Model Description & Results (iGEM Wiki):**  
  [https://2025.igem.wiki/unicamp-brazil/model](https://2025.igem.wiki/unicamp-brazil/model)

---

## License & Attribution

Developed by the **iGEM UNICAMP 2025 Team**  
Part of the **PepCitrus Project**, focused on computational modeling of  and antibiotic treatment strategies.  

© 2025 iGEM UNICAMP.  
Licensed under the [MIT License](https://opensource.org/licenses/MIT).  
Feel free to use, modify, and distribute with proper attribution.
