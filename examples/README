# RT-cNEO Examples

Progressive examples demonstrating RT-NEO and RT-cNEO simulations.

## Quick Start

```bash
python 03_comparison.py
```

Runs both RT-NEO and RT-cNEO, generates comparison plots, calculates metrics, saves to comparison_results/

## Examples

01_basic_rtneo.py - Pure quantum dynamics (no constraints)
02_basic_rtcneo.py - Constrained quantum dynamics
03_comparison.py - RT-NEO vs RT-cNEO comparison with metrics
04_field_scan.py - Field strength parameter scan
05_barrier_analysis.py - PES barrier diagnostic
06_time_dependent_fock.py - Static vs time-dependent Fock comparison

## Output

comparison.py output:
```
comparison_results/
├── comparison_full.png         # 4-panel plot
├── constraint_analysis.png     # Constraint forces
├── comparison_summary.txt      # Metrics
├── rtneo_trajectory.csv
└── rtcneo_trajectory.csv
```

Basic examples output: rtneo_basic_trajectory.csv, rtcneo_basic_trajectory.csv

## Requirements

- Python 3.8+
- NumPy, SciPy, Matplotlib
- PySCF-NEO (Yang's fork)

Installation:
```bash
git clone https://github.com/theorychemyang/pyscf
cd pyscf && pip install -e .
cd /path/to/RT_cNEO && pip install -e .
```

## Usage Notes

- Start with 03_comparison.py
- Use max_time=100.0 for quick tests
- Use sto-3g for speed, 6-31g* for production
- Enable use_time_dependent_fock=True for accuracy (slower)

## Documentation

- ../QUICKSTART.md
- ../DOCS/theory/RT_CNEO_COMPLETE.md
