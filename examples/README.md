# RT-cNEO Examples

This directory contains progressive examples demonstrating RT-NEO and RT-cNEO simulations.

## Quick Start

### Run RT-NEO vs RT-cNEO Comparison (Recommended!)

```bash
python 03_comparison.py
```

This single script:
- Runs BOTH RT-NEO and RT-cNEO simulations
- Generates comprehensive comparison plots
- Calculates quantitative metrics
- Saves all results to `comparison_results/`

**Perfect for understanding the difference between pure quantum dynamics (RT-NEO) and constrained trajectory extraction (RT-cNEO)!**

## Example Descriptions

### Basic Examples

**01_basic_rtneo.py** - Pure quantum dynamics
- No constraint forces
- Just quantum time evolution
- Shows quantum oscillations and delocalization

**02_basic_rtcneo.py** - Constrained quantum dynamics
- Adds constraint forces
- Extracts smooth classical trajectory
- Still preserves quantum character!

**03_comparison.py** - Comprehensive comparison study ⭐
- **START HERE!** Best way to understand the methods
- Runs both RT-NEO and RT-cNEO
- Generates 4-panel comparison plots
- Calculates smoothness ratio, correlation, etc.
- Saves comprehensive report

### Advanced Examples

**04_field_scan.py** - Field strength parameter study
- Scan different external field strengths
- Find optimal field for proton transfer
- Compare RT-NEO vs RT-cNEO across conditions

**05_barrier_analysis.py** - PES barrier diagnostic
- Scan actual NEO-HF potential energy surface
- Calculate barrier height
- Recommend field strength for transfer

**06_time_dependent_fock.py** - Exact formalism
- Enable time-dependent Fock matrices
- Slower but accurate for all timescales
- Compares static vs time-dependent Fock

## Output Files

All examples create output files:

### From comparison.py
```
comparison_results/
├── comparison_full.png         # 4-panel comparison plot
├── constraint_analysis.png     # RT-cNEO constraint forces
├── comparison_summary.txt      # Detailed metrics
├── rtneo_trajectory.csv        # RT-NEO data
└── rtcneo_trajectory.csv       # RT-cNEO data
```

### From basic examples
```
rtneo_basic_trajectory.csv      # RT-NEO trajectory data
rtcneo_basic_trajectory.csv     # RT-cNEO trajectory data
```

## System Requirements

- Python 3.8+
- NumPy, SciPy, Matplotlib
- PySCF-NEO (Yang's fork)

## Installation

```bash
# Clone Yang's PySCF-NEO
git clone https://github.com/theorychemyang/pyscf
cd pyscf
pip install -e .

# Install RT-cNEO
cd /path/to/RT_cNEO
pip install -e .
```

## Tips

1. **Start with `03_comparison.py`** - gives you the full picture
2. Run on shorter timescales first (`max_time=100.0`) for quick tests
3. Use `sto-3g` basis for speed, `6-31g*` for production
4. Enable `use_time_dependent_fock=True` for quantitative accuracy (slower)

## Questions?

See the main documentation:
- `../QUICKSTART.md` - Getting started guide
- `../docs/REFACTORING_SUMMARY.md` - Complete refactoring summary
- `../docs/theory/RT_CNEO_COMPLETE.md` - Theoretical foundations
