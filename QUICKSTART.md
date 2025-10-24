# RT-cNEO Quick Start Guide

**Welcome!** This guide gets you running RT-NEO vs RT-cNEO comparisons in 5 minutes.

---

## 🚀 Super Quick Start

```bash
# 1. Install
pip install -e .

# 2. Run comparison example
cd examples
python 03_comparison.py

# 3. View results
open comparison_results/comparison_full.png
```

**Done!** You now have comprehensive RT-NEO vs RT-cNEO comparison plots.

---

## 📊 What You Get

The comparison script generates:

```
comparison_results/
├── comparison_full.png          # 4-panel comparison plot
│   ├── Position trajectories (RT-NEO vs RT-cNEO)
│   ├── Energy evolution
│   ├── Velocity comparison
│   └── Phase space plot
│
├── constraint_analysis.png      # RT-cNEO constraint forces
├── comparison_summary.txt       # Quantitative metrics
├── rtneo_trajectory.csv         # RT-NEO data
└── rtcneo_trajectory.csv        # RT-cNEO data (with constraint forces)
```

---

## 💻 Using in Your Code

```python
from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters

# Setup
params = SimulationParameters(
    time_step=0.1,
    max_time=500.0,
    field_strength=0.02
)

# Run BOTH methods
study = ComparisonStudy(params)
rtneo, rtcneo = study.run_full_comparison()

# Get metrics
study.print_summary()

# Generate report
study.generate_report()
```

---

## 📖 Next Steps

1. **See all examples**: `examples/README.md`
2. **Read full documentation**: `docs/REFACTORING_SUMMARY.md`
3. **Understand theory**: `docs/theory/RT_CNEO_COMPLETE.md`
4. **Migration guide**: `docs/MIGRATION_GUIDE.md`

---

**Author**: Federico Zahariev
**Date**: October 2025
