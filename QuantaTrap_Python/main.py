import os
import glob
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fitting import perform_cgcd

DATA_DIR = 'data'
REPORTS_DIR = 'reports'

def process_file(filepath):
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    print(f"Processing {filename}...")
    
    # 1. Read data
    try:
        # Assuming space, tab, or comma separated values (Temperature, Intensity)
        df = pd.read_csv(filepath, sep=r'[,\s]+', engine='python', header=None, comment='#')
        if df.shape[1] < 2:
            print(f"  -> Skipping {filename}: Not enough columns.")
            return
        T = df.iloc[:, 0].values
        I = df.iloc[:, 1].values
    except Exception as e:
        print(f"  -> Error reading {filename}: {e}")
        return

    # Sort by temperature
    sort_idx = np.argsort(T)
    T = T[sort_idx]
    I = I[sort_idx]

    # Baseline subtraction (simple min subtraction)
    I = df.iloc[:, 1].values.astype(float)

    # 2. Perform CGCD (Deconvolution)
    peaks = perform_cgcd(T, I, max_peaks=5)

    # 3. Plotting & Presentation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Glow Curve & CGCD
    ax1.plot(T, I, label='Original TL curve', color='gray', linewidth=2)
    # (Here optionally to mask fitting TL peaks)
    # sum_I = np.zeros_like(I, dtype=float)
    #
    # colors = ['#ef4444', '#f59e0b', '#10b981', '#06b6d4', '#8b5cf6', '#ec4899']
    #
    # for i, p in enumerate(peaks):
    #     color = colors[i % len(colors)]
    #     ax1.plot(T, p['data'], '--', color=color, label=f"{p['id']} (Tm={p['Tm']:.1f}K)")
    #     sum_I += p['data']
    #
    # if peaks:
    #     ax1.plot(T, sum_I, 'b:', label='Fitted Sum', linewidth=2)
    #
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('TL Intensity (a.u.)')
    ax1.set_title(f'Glow Curve & CGCD - {name}')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Plot 2: Trap Distribution (Quantum Concept)
    E_axis = T / 500.0  # E = T/500
    # ax2.plot(E_axis, I, label='Total g(E)', color='#8b5cf6', linewidth=2)

    sum_I = np.zeros_like(I, dtype=float)

    colors = ['#ef4444', '#f59e0b', '#10b981', '#06b6d4', '#8b5cf6', '#ec4899']

    if peaks:
        ax2.plot(E_axis, sum_I, 'b:', label='QuantaTrap', linewidth=2)
        
    for i, p in enumerate(peaks):
        color = colors[i % len(colors)]
        ax2.plot(E_axis, p['data'], '--', color=color)
    
    ax2.set_xlabel('Energy E (eV)')
    ax2.set_ylabel('Density of States g(E)')
    ax2.set_title('Trap Distribution (Quantum Concept)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    
    # 4. Save Reports
    # Save PDF
    pdf_path = os.path.join(REPORTS_DIR, f'{name}_report.pdf')
    plt.savefig(pdf_path)
    plt.close()

    # Save CSV
    csv_path = os.path.join(REPORTS_DIR, f'{name}_results.csv')
    results_list = [{'Peak': p['id'], 'Tm (K)': p['Tm'], 'Im (a.u.)': p['Im'], 'Energy (eV)': p['E']} for p in peaks]
    results_df = pd.DataFrame(results_list)
    results_df.to_csv(csv_path, index=False)

    # Save JSON
    json_path = os.path.join(REPORTS_DIR, f'{name}_results.json')
    json_data = {
        'filename': filename,
        'peaks': [{'id': p['id'], 'Tm': float(p['Tm']), 'Im': float(p['Im']), 'E': float(p['E'])} for p in peaks]
    }
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=4)

    print(f"  -> Saved reports: {pdf_path}, {csv_path}, {json_path}")

def generate_sample_data():
    """Generates a sample glow curve file if the data directory is empty."""
    sample_file = os.path.join(DATA_DIR, 'sample_glow_curve.csv')
    if not os.path.exists(sample_file):
        print("Generating sample data...")
        T = np.linspace(300, 700, 400)
        # Create two overlapping peaks
        I1 = 100 * np.exp(1 + 23.21*(T-450)/450 - np.exp(23.21*(T-450)/450))
        I2 = 80 * np.exp(1 + 23.21*(T-520)/520 - np.exp(23.21*(T-520)/520))
        I = I1 + I2 + np.random.normal(0, 2, len(T)) # Add noise
        
        df = pd.DataFrame({'Temperature': T, 'Intensity': I})
        df.to_csv(sample_file, index=False)
        print(f"  -> Created {sample_file}")

def main():
    # Ensure directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Generate sample data if needed
    generate_sample_data()

    # Find all CSV and TXT files in the data folder
    files = glob.glob(os.path.join(DATA_DIR, '*.csv')) + glob.glob(os.path.join(DATA_DIR, '*.txt'))
    
    if not files:
        print(f"No data files found in '{DATA_DIR}/'. Please add some .csv or .txt files.")
        return

    print(f"Found {len(files)} files to process.\n")
    
    for f in files:
        process_file(f)
        
    print("\nAll processing complete. Check the 'reports' folder for results.")

if __name__ == '__main__':
    main()
