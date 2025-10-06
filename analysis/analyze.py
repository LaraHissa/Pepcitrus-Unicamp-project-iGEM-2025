import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
import os
import json
from tqdm import tqdm
from matplotlib.ticker import AutoMinorLocator

# -------------------- Global Configuration --------------------
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Palatino"]
})

# --- Directory Configuration ---
# **CORREÇÃO:** Define o caminho para a pasta que contém os dados (cpp_simulator), 
# assumindo que o script é executado DE DENTRO da pasta 'analyses'.
SIMULATOR_ROOT = os.path.join('..', 'cpp_simulator')
CONFIG_FILE = os.path.join('..', 'config_analysis.json') # Assume o config.json também está fora da pasta analyses

# --- Video Parameters (Fixed, internal to the code) ---
GLOBAL_FPS = 50
GLOBAL_GRID_SIZE = 50
GLOBAL_UPSCALE_FACTOR = 12
GLOBAL_FRAME_WIDTH = GLOBAL_GRID_SIZE * GLOBAL_UPSCALE_FACTOR
GLOBAL_FRAME_HEIGHT = GLOBAL_GRID_SIZE * GLOBAL_UPSCALE_FACTOR
GLOBAL_SECONDS_TO_HOLD_END_FRAME = 5 
GLOBAL_SLOW_MOTION_DURATION = 150 
GLOBAL_SLOW_MOTION_FACTOR = 4     

# -------------------- Utility Functions --------------------


def load_analysis_config(file_path=CONFIG_FILE):
    """
    Loads configuration parameters from a JSON file using the correct relative path.
    """
    default_params = {
        "effect_window_days": 150,
        "treatment_start_day": 1000,
        "num_years_treatment": 4
    }

    if not os.path.exists(file_path):
        print(f"WARNING: Configuration file '{file_path}' not found. Using default hardcoded plot values.")
        return default_params
        
    with open(file_path, 'r') as f:
        try:
            config = json.load(f)
            params = {key: config.get(key, default_params[key]) for key in default_params}
            print(f"Configuration loaded successfully from {file_path}")
            print(f"Plot parameters being used: {params}")
            return params
        except json.JSONDecodeError:
            print(f"ERROR: Could not decode JSON from {file_path}. Check file format.")
            return default_params

# -------------------- Plotting Functions --------------------
def load_data(scenario):
    """
    Loads the time series CSV data specific to the scenario from the SIMULATOR_ROOT.
    """
    # CORREÇÃO: Constrói o caminho completo para o arquivo CSV de resultados
    file_path = os.path.join(SIMULATOR_ROOT, f"results_{scenario.lower()}.csv")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Time series data file '{file_path}' not found.")
        
    df = pd.read_csv(file_path)
    df['days'] = df['time'] * 1.0 
    return df

def plot_data(df, scenario, plot_params):
    """
    Plots the chosen treatment scenario and saves the figure as PDF.
    """
    effect_window = plot_params['effect_window_days']  
    treatment_start = plot_params['treatment_start_day'] 
    num_years = plot_params['num_years_treatment']
    
    applications = [treatment_start + i*365 for i in range(num_years)]
    
    fig, ax = plt.subplots(figsize=(14,6))
    
    ax.plot(df['days'], df['mean_infection'], label=r'Infection ($\bar{I}$)', color='red', linewidth=2)
    ax.plot(df['days'], df['mean_callose'], label=r'Callose ($\bar{C}$)', color='#CC9900', linewidth=2)
    
    if scenario.lower() in ['tetra', 'ctx']:
        application_day = applications[0]
        
        if application_day in df['days'].values:
            infection_val = df.loc[df['days']==application_day, 'mean_infection'].values[0]
            
            if scenario.lower() == 'tetra':
                ax.axvspan(application_day, application_day + effect_window, color='green', alpha=0.3, label=r'Tetracycline effect (150 days)')
            
            ax.plot(application_day, infection_val,
                    marker='*', color='green', markersize=15, label=r'Start of Treatment')
    
    start_day = 4*30
    end_day   = 10*30
    ax.axvspan(start_day, end_day, color='blue', alpha=0.2, label=r'Symptoms Emerge (4-10 months)')
    
    ax.set_xlim(left=0)
    ax.set_ylim(0, 1.0)
    
    total_days = df['days'].max()
    num_years_total = int(np.ceil(total_days/365))
    
    ticks_years = np.arange(0, (num_years_total+1)*365, 365)
    labels_years = [f'{i} yr' if i==1 else f'{i} yrs' for i in range(num_years_total+1)]
    
    ax.set_xticks(ticks_years)
    ax.set_xticklabels(labels_years, fontsize=14, rotation=45)
    
    minor_ticks = np.arange(0, total_days, 30)
    ax.set_xticks(minor_ticks, minor=True)

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='both', which='major', direction='in', top=True, right=True, length=8)
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.tick_params(axis='both', which='minor', direction='in', top=True, right=True, length=4)
    
    ax.set_xlabel(r'Time since initial infection (days)', fontsize=16)
    ax.set_ylabel(r'Normalized Concentration ($\bar{I}/\bar{C}$)', fontsize=16)
    ax.set_title(f'Disease Progression: {scenario.capitalize()} Scenario', fontsize=18)
    
    ax.legend(fontsize=12)
    plt.tight_layout()
    
    # O arquivo PDF de saída é salvo no diretório de execução (analyses/)
    output_file = f'plot_results_{scenario.lower()}.pdf'
    plt.savefig(output_file, format='pdf')
    print(f"Figure saved as {output_file}")


# -------------------- Video Generation Functions --------------------

def create_video_frame_continuous(data_file):
    """
    Creates a single BGR video frame by mixing colors based on infection, callose, and drug.
    """
    df = pd.read_csv(data_file)
    try:
        infection_grid = df.pivot(index='i', columns='j', values='infection').values
        callose_grid = df.pivot(index='i', columns='j', values='callose').values
        drug_grid = df.pivot(index='i', columns='j', values='drug').values 
    except KeyError as e:
        print(f"KeyError processing video frame: {e}")
        return None

    canvas_bgr = np.zeros((GLOBAL_GRID_SIZE, GLOBAL_GRID_SIZE, 3), dtype=np.uint8)
    drug_max_val = 50.0 
    
    green_channel_values = (np.clip(drug_grid / drug_max_val, 0, 1) + callose_grid)
    canvas_bgr[..., 1] = (np.clip(green_channel_values, 0, 1) * 255).astype(np.uint8)
    red_channel_values = (infection_grid + callose_grid)
    canvas_bgr[..., 2] = (np.clip(red_channel_values, 0, 1) * 255).astype(np.uint8)

    large_frame = cv2.resize(canvas_bgr, (GLOBAL_FRAME_WIDTH, GLOBAL_FRAME_HEIGHT), interpolation=cv2.INTER_NEAREST)
    
    bar_height = 50
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)
    font_thickness = 2
    
    try:
        time_step = int(os.path.basename(data_file).split('_')[1].split('.')[0])
    except:
        time_step = 0
    
    text = f'Time: {time_step} days'
    cv2.rectangle(large_frame, (0, 0), (GLOBAL_FRAME_WIDTH, bar_height), (0, 0, 0), -1)
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x = (GLOBAL_FRAME_WIDTH - text_width) // 2
    text_y = (bar_height + text_height) // 2
    cv2.putText(large_frame, text, (text_x, text_y), font, font_scale, font_color, font_thickness)
    
    return large_frame

def generate_simulation_video(scenario, treatment_start_day):
    """
    Generates a video from frame CSVs for the specified scenario.
    """
    # CORREÇÃO: Usa SIMULATOR_ROOT para construir o caminho correto para a pasta de dados.
    DATA_DIR = os.path.join(SIMULATOR_ROOT, f'data_{scenario.lower()}')
    VIDEO_FILENAME = f'simulation_{scenario.lower()}.mp4'
    
    print(f"\n--- Starting Video Generation for '{scenario.upper()}' ---")
    
    if not os.path.isdir(DATA_DIR):
        print(f"ERROR: Data directory '{DATA_DIR}' not found. Cannot generate video.")
        return 

    # Garante que a ordenação dos arquivos seja numérica
    data_files = sorted(glob.glob(os.path.join(DATA_DIR, 'frame_*.csv')), 
                        key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

    if not data_files:
        print(f"ERROR: No data files found in '{DATA_DIR}'.")
        return

    print(f"Found {len(data_files)} frames. Initializing video writer for '{VIDEO_FILENAME}'...")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # O arquivo de vídeo de saída é salvo no diretório de execução (analyses/)
    video_writer = cv2.VideoWriter(VIDEO_FILENAME, fourcc, GLOBAL_FPS, (GLOBAL_FRAME_WIDTH, GLOBAL_FRAME_HEIGHT))

    last_frame_processed = None

    TREATMENT_START_DAY = treatment_start_day 
    SLOW_MOTION_DURATION = GLOBAL_SLOW_MOTION_DURATION
    SLOW_MOTION_FACTOR = GLOBAL_SLOW_MOTION_FACTOR
    
    slow_motion_end_day = TREATMENT_START_DAY + SLOW_MOTION_DURATION
    
    for file_path in tqdm(data_files, desc="Processing frames"):
        bgr_frame = create_video_frame_continuous(file_path)
        
        if bgr_frame is None:
            continue

        try:
            time_step = int(os.path.basename(file_path).split('_')[1].split('.')[0])
        except:
            time_step = -1

        if TREATMENT_START_DAY <= time_step < slow_motion_end_day:
            for _ in range(SLOW_MOTION_FACTOR):
                video_writer.write(bgr_frame)
        else:
            video_writer.write(bgr_frame)
        
        last_frame_processed = bgr_frame
    
    if last_frame_processed is not None:
        num_extra_frames = int(GLOBAL_FPS * GLOBAL_SECONDS_TO_HOLD_END_FRAME)
        print(f"\nHolding the final frame for {GLOBAL_SECONDS_TO_HOLD_END_FRAME} seconds...")
        for _ in tqdm(range(num_extra_frames), desc="Adding final pause"):
            video_writer.write(last_frame_processed)
    
    video_writer.release()
    print(f"Video '{VIDEO_FILENAME}' created successfully!")
    print(f"--- Video Generation Finished for '{scenario.upper()}' ---")


# -------------------- Interactive Main Loop --------------------
def main():
    print("="*55)
    print(" Pepcitrus Unicamp - iGEM Project Simulation Analysis Tool")
    print("-"*55)
    print(f" Data will be loaded from the root: '{SIMULATOR_ROOT}/'")
    print(" Note: Data files must be organized inside this folder.")
    print("-"*55)
    print(" Reading plotting parameters from 'config_analysis.json'.")
    print(" The config file is expected at the root (not inside analyses/).")
    print("="*55 + "\n")
    
    plot_params = load_analysis_config()
    treatment_start_day = plot_params.get('treatment_start_day', 1000)

    while True:
        print("\nSelect a scenario (Plot and Video will run for the chosen option):")
        print("  'control' -> No drug treatment")
        print("  'ctx'     -> CTX (bactericidal) treatment")
        print("  'tetra'   -> Tetracycline (bacteriostatic) treatment")
        print("  'all'     -> Run all scenarios")
        print("  'exit'    -> Quit the program")
        user_input = input("Enter your choice: ").strip().lower()
        
        scenarios = []
        if user_input in ['control', 'ctx', 'tetra']:
            scenarios = [user_input]
        elif user_input == 'all':
            scenarios = ['control', 'ctx', 'tetra']
        elif user_input == 'exit':
            print("\nExiting the plots. Goodbye!")
           
            break
        else:
            print("\n--- Invalid choice. Please select 'control', 'ctx', 'tetra', 'all', or 'exit'. ---")
            continue
            
        for scenario in scenarios:
            print(f"\n[SCENARIO: {scenario.upper()}] Starting full analysis...")
            
            df_current = None
            
            # 1. Load Data for Plotting
            try:
                df_current = load_data(scenario)
            except FileNotFoundError as e:
                print(f"ERROR: {e}. Cannot generate plot for this scenario.")
            
            # 2. Plot Generation
            if df_current is not None:
                plot_data(df_current, scenario, plot_params)
            
            # 3. Video Generation
            generate_simulation_video(scenario, treatment_start_day)
        
        print(f"\nAnalysis complete for {', '.join(scenarios)}.")

if __name__ == "__main__":
    main()
