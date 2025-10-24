# Migration Guide: Old → New RT-cNEO

**Quick Reference**: How to update your code to use the new modular structure.

---

## Option 1: Keep Using Monolithic Version (Easiest!)

**Your old code still works - no changes needed!**

```python
# This continues to work exactly as before
from rt_cneo_clean import (
    SimulationFactory,
    SimulationParameters,
    GaussianPulseField,
    TrajectoryAnalyzer
)

# Run as usual
params = SimulationParameters(...)
simulator = SimulationFactory.create_simulator(params)
results = simulator.run_rtneo()
```

**No migration required!** The file `rt_cneo_clean.py` is still there and functional.

---

## Option 2: Use New Modular Package (Recommended!)

### Benefits
- Cleaner imports
- Better organization
- **New comparison tools** ⭐
- Easier to extend
- Pip installable

### Installation

```bash
cd RT_cNEO
pip install -e .
```

### Import Changes

**Old monolithic imports:**
```python
from rt_cneo_clean import (
    SimulationFactory,
    SimulationParameters,
    GaussianPulseField,
    TrajectoryAnalyzer
)
```

**New modular imports:**
```python
from rtcneo import SimulationFactory, SimulationParameters
from rtcneo.strategies import GaussianPulseField
from rtcneo.analysis import TrajectoryAnalyzer
```

### Example Migration

**Old Code:**
```python
from rt_cneo_clean import *

params = SimulationParameters(time_step=0.1, max_time=500.0)
simulator = SimulationFactory.create_simulator(params)

rtneo_results = simulator.run_rtneo()
rtcneo_results = simulator.run_rtcneo()

# Manual plotting...
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(rtneo_results.times, rtneo_results.positions, label='RT-NEO')
ax.plot(rtcneo_results.times, rtcneo_results.positions, label='RT-cNEO')
plt.legend()
plt.savefig('comparison.png')
```

**New Code (Using Comparison Module):**
```python
from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters

params = SimulationParameters(time_step=0.1, max_time=500.0)

# One command does everything!
study = ComparisonStudy(params)
rtneo_results, rtcneo_results = study.run_full_comparison()
study.generate_report()  # Creates comprehensive plots + analysis!
```

**Much cleaner!** The comparison module creates publication-quality 4-panel plots automatically.

---

## Option 3: Use NEW Comparison Tools (Best for Research!)

The **killer feature** of the refactoring is the comparison module.

### Quick Comparison

```python
from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters

params = SimulationParameters(
    time_step=0.1,
    max_time=500.0,
    field_strength=0.02
)

study = ComparisonStudy(params)
study.run_full_comparison()     # Runs both RT-NEO and RT-cNEO
study.print_summary()            # Prints metrics to console
study.generate_report()          # Creates plots and CSV files
```

### What You Get

**Console output:**
```
COMPARISON SUMMARY
==========================================
Final Positions:
  RT-NEO:   0.234 Å
  RT-cNEO:  0.198 Å

Trajectory Smoothness:
  RT-cNEO is 3.45× smoother than RT-NEO

Barrier Crossings:
  RT-NEO:  12 crossings
  RT-cNEO: 2 crossings
```

**Files created** in `comparison_results/`:
- `comparison_full.png` - 4-panel comparison plot
- `constraint_analysis.png` - Constraint force analysis
- `comparison_summary.txt` - Detailed metrics
- `rtneo_trajectory.csv` - RT-NEO data
- `rtcneo_trajectory.csv` - RT-cNEO data

**Perfect for publications!**

---

## Common Migration Patterns

### Pattern 1: Basic Simulation

**Old:**
```python
from rt_cneo_clean import SimulationFactory, SimulationParameters

params = SimulationParameters(...)
sim = SimulationFactory.create_simulator(params)
results = sim.run_rtneo()
```

**New (identical!):**
```python
from rtcneo import SimulationFactory, SimulationParameters

params = SimulationParameters(...)
sim = SimulationFactory.create_simulator(params)
results = sim.run_rtneo()
```

### Pattern 2: Custom Field

**Old:**
```python
from rt_cneo_clean import GaussianPulseField, SimulationFactory

field = GaussianPulseField(center=50.0, width=20.0, amplitude=0.02)
sim = SimulationFactory.create_simulator(params, field_strategy=field)
```

**New:**
```python
from rtcneo.strategies import GaussianPulseField
from rtcneo import SimulationFactory

field = GaussianPulseField(center=50.0, width=20.0, amplitude=0.02)
sim = SimulationFactory.create_simulator(params, field_strategy=field)
```

### Pattern 3: Analysis

**Old:**
```python
from rt_cneo_clean import TrajectoryAnalyzer

analyzer = TrajectoryAnalyzer()
analysis = analyzer.analyze(results)
analyzer.print_analysis(analysis)
```

**New (same API!):**
```python
from rtcneo.analysis import TrajectoryAnalyzer

analyzer = TrajectoryAnalyzer()
analysis = analyzer.analyze(results)
analyzer.print_analysis(analysis)
```

---

## Import Cheat Sheet

| Component | Old Import | New Import |
|-----------|-----------|------------|
| **Core** |
| SimulationFactory | `from rt_cneo_clean import` | `from rtcneo import` |
| SimulationParameters | `from rt_cneo_clean import` | `from rtcneo.core import` |
| **Field Strategies** |
| GaussianPulseField | `from rt_cneo_clean import` | `from rtcneo.strategies import` |
| LinearRampField | `from rt_cneo_clean import` | `from rtcneo.strategies import` |
| **Analysis** |
| TrajectoryAnalyzer | `from rt_cneo_clean import` | `from rtcneo.analysis import` |
| **NEW: Comparison** |
| ComparisonStudy | N/A (didn't exist!) | `from rtcneo.analysis import` ⭐ |

---

## Recommendation

**For existing scripts**: No changes needed! Keep using `rt_cneo_clean.py`.

**For new work**: Use the new modular package, especially the **comparison module**!

```bash
# Just run this to get started
cd examples
python 03_comparison.py
```

This demonstrates the power of the new comparison tools and generates example output.

---

## Questions?

- **Old code broken?** It shouldn't be! The old file still exists.
- **New imports not working?** Run `pip install -e .` first.
- **Want to use comparison module?** See `examples/03_comparison.py`

---

**Author**: Federico Zahariev
**Date**: October 24, 2025
