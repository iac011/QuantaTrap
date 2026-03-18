# QuantaTrap Python Project

This is a local Python implementation of the QuantaTrap Thermoluminescence (TL) analysis tool. It processes TL glow curves, performs Computerized Glow Curve Deconvolution (CGCD) to quantify continuous trap distributions, and generates comprehensive reports.

## Project Structure

```
QuantaTrap_Python/
├── main.py            # 1. Main entry point: reads data, plots TL curves, generates reports
├── fitting.py         # 2. CGCD algorithm for multi-peak fitting and Trap Distribution
├── data/              # 3. Folder for input CSV/TXT files (Temperature, Intensity)
├── reports/           # 4. Folder for output reports (CSV, PDF, JSON)
└── requirements.txt   # Python dependencies
```

## Setup Instructions

1. Ensure you have Python 3.8+ installed on your system.
2. Open a terminal or command prompt in this directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Place your raw TL glow curve data files (`.csv` or `.txt`) inside the `data/` folder.
   - The files should contain two columns: **Temperature** and **Intensity** (separated by commas, spaces, or tabs).
   - *Note: If the `data/` folder is empty, the script will automatically generate a sample file (`sample_glow_curve.csv`) for testing.*
2. Run the main script:
   ```bash
   python main.py
   ```
3. Check the `reports/` folder for the output. For each input file, you will get:
   - `[filename]_report.pdf`: High-quality plots of the Glow Curve, CGCD fit, and Trap Distribution.
   - `[filename]_results.csv`: A table of the deconvoluted peaks (Energy, Tm, Intensity).
   - `[filename]_results.json`: A structured JSON file containing the peak data for programmatic use.