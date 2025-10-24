# RT-cNEO: Real-Time constrained Nuclear-Electronic Orbital Dynamics

**Production-ready implementation** of RT-cNEO - a synthesis of RT-NEO quantum dynamics and cNEO classical trajectory extraction for simulating quantum proton transfer.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: SOLID](https://img.shields.io/badge/code%20style-SOLID-green.svg)](https://en.wikipedia.org/wiki/SOLID)

---

## 🚀 Quick Start: RT-NEO vs RT-cNEO Comparison

```python
from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters

# Setup parameters
params = SimulationParameters(
    time_step=0.1,
    max_time=500.0,
    field_strength=0.02
)

# Run comprehensive comparison
study = ComparisonStudy(params)
rtneo_results, rtcneo_results = study.run_full_comparison()

# Generate report with plots and analysis
study.print_summary()
study.generate_report()  # Creates comparison_results/ directory
```

**That's it!** This runs BOTH methods and generates comprehensive comparison plots and metrics.

---

## ✨ What's New in v1.0.0

### 🎯 **NEW: Comprehensive Comparison Tools**
- **ComparisonStudy** class - one-line RT-NEO vs RT-cNEO comparison
- Automatic generation of 4-panel comparison plots
- Quantitative metrics: smoothness ratio, correlation, energy drift
- Publication-quality visualizations

### 🏗️ **Clean Package Structure**
- Modular design following SOLID principles
- Organized into logical subpackages: `core`, `strategies`, `dynamics`, `analysis`
- Easy to extend and maintain

### 📦 **Proper Installation**
```bash
pip install -e .
```

### 📚 **Progressive Examples**
- `01_basic_rtneo.py` - Pure quantum dynamics
- `02_basic_rtcneo.py` - Constrained dynamics
- `03_comparison.py` - **⭐ Comprehensive RT-NEO vs RT-cNEO comparison**

---

## 📖 Overview

### What is RT-cNEO?

**RT-cNEO** combines two published methods:

1. **RT-NEO** (Zhao et al., 2020) - Real-time quantum dynamics of electrons + quantum nuclei
2. **cNEO** (Xu & Yang, 2020) - Constrained NEO for classical trajectory extraction

**Key Innovation**: Quantum time evolution with constraint potential to extract smooth classical trajectories while preserving quantum character (excited states, superpositions).

### Core Mechanism

```
H(t) = H₀ + f_constraint(t)·R̂ + V_external(t)·R̂

where:
  f_constraint = 2·(F_smooth - F_quantum)    [critical damping]
  F_smooth = exponential smoothing of F_quantum
  V_external = time-dependent driving field
```

**Critical insight**: Adds constraint as POTENTIAL (modifies H), does NOT minimize energy (which would collapse to ground state).

---

## 📥 Installation

### Prerequisites

```bash
# Python 3.8 or later
python --version

# Install Yang's PySCF-NEO fork
git clone https://github.com/theorychemyang/pyscf
cd pyscf
pip install -e .
```

### Install RT-cNEO

```bash
cd RT_cNEO
pip install -e .
```

### Verify Installation

```python
from rtcneo import SimulationFactory
from rtcneo.analysis import ComparisonStudy
print("✓ RT-cNEO installed successfully!")
```

---

## 🎓 Examples

### Example 1: Basic RT-NEO (Pure Quantum)

```python
from rtcneo import SimulationFactory, SimulationParameters

params = SimulationParameters(time_step=0.1, max_time=500.0)
simulator = SimulationFactory.create_simulator(params)

# Run pure quantum dynamics (no constraint)
results = simulator.run_rtneo()
print(f"Final position: {results.get_final_position():.3f} Å")
```

### Example 2: Basic RT-cNEO (Constrained)

```python
# Same setup, but with constraint forces
results = simulator.run_rtcneo()
print(f"Final position: {results.get_final_position():.3f} Å")
print(f"Smoothness: {results.count_barrier_crossings()} barrier crossings")
```

### Example 3: Comprehensive Comparison (⭐ Recommended!)

```bash
cd examples
python 03_comparison.py
```

This generates:
- `comparison_full.png` - 4-panel comparison (position, energy, velocity, phase space)
- `constraint_analysis.png` - RT-cNEO constraint force analysis
- `comparison_summary.txt` - Detailed metrics
- CSV data files for both methods

**Perfect for publications and understanding the difference between the methods!**

---

## 🏗️ Package Structure

```
rtcneo/
├── core/                   # Core physics
│   ├── constants.py       # Physical constants, dataclasses
│   ├── molecular_system.py
│   ├── ground_state.py
│   └── propagator.py
├── strategies/             # Strategy pattern implementations
│   ├── fields.py          # External field strategies
│   ├── potentials.py      # PES strategies
│   └── constraint.py      # Constraint force calculation
├── dynamics/               # Simulation engine
│   ├── simulator.py
│   ├── factory.py
│   └── state.py
├── analysis/               # Analysis and visualization
│   ├── comparison.py      # ⭐ NEW: RT-NEO vs RT-cNEO comparison
│   ├── analyzer.py
│   └── visualizer.py
└── utils/                  # Utilities
    ├── environment.py
    └── diagnostics.py
```

---

## 🔬 Physics Features

### ✅ Implemented

- **Quantum propagation**: Proper unitary time evolution
- **Constraint as potential**: Preserves quantum character
- **External field support**: Time-dependent fields for driving dynamics
- **Multiple field strategies**: Gaussian pulse, linear ramp, cosine ramp, etc.
- **Real ab initio forces**: PySCF-NEO gradient potential
- **Time-dependent Fock**: Optional exact formalism (slower but accurate)

### 📊 Comparison Metrics

The new `ComparisonStudy` class calculates:
- **Smoothness ratio**: How much smoother RT-cNEO is vs RT-NEO
- **Trajectory correlation**: Pearson correlation between methods
- **Final position difference**: Agreement on transfer outcome
- **Energy drift comparison**: Conservation quality
- **Barrier crossing count**: Trajectory smoothness indicator

---

## 📚 Documentation

### Quick Links

- **[examples/README.md](examples/README.md)** - Progressive examples guide
- **[docs/theory/RT_CNEO_COMPLETE.md](docs/theory/RT_CNEO_COMPLETE.md)** - Theoretical foundations (30K)
- **[docs/REFACTORING_SUMMARY.md](docs/REFACTORING_SUMMARY.md)** - Detailed refactoring summary
- **Legacy**: `rt_cneo_clean.py` - Original monolithic implementation (still works!)

### Key Concepts

**RT-NEO vs RT-cNEO:**
- **RT-NEO**: Pure quantum dynamics, can have rapid oscillations
- **RT-cNEO**: Smoothed trajectory while preserving quantum character
- **Use comparison module** to quantitatively assess differences!

**External Field Requirement:**
- Symmetric systems (FHF⁻) need external field to break symmetry
- Typical strength: 0.01-0.02 au ≈ 0.5-1.0 V/Å
- Multiple field strategies available

**Time-Dependent Fock:**
```python
params = SimulationParameters(
    use_time_dependent_fock=True  # Exact formalism (10-100× slower)
)
```
- **Default (False)**: Static Fock, fast, valid for short time
- **Enabled (True)**: Time-dependent Fock, slow, accurate for all cases

---

## 🎯 When to Use RT-cNEO

### ✅ Suitable For

- Method development and benchmarking
- Short time dynamics (< 100 fs with static Fock)
- Excited state dynamics (preserves quantum character!)
- Understanding constraint mechanisms
- Comparing quantum vs classical-like trajectories

### ⚠️ Known Approximations (Default Mode)

1. **Static Fock matrix**: Electron-proton coupling not updated
   - Valid for: short time, small amplitude
   - **Solution**: Set `use_time_dependent_fock=True` for exact formalism

2. **Constraint force formula**: `f = 2(F_smooth - F_quantum)`
   - Factor of 2 derived from critical damping theory
   - See `docs/theory/RT_CNEO_COMPLETE.md` Section 5 for proof

---

## 📈 Performance

**Typical runtimes** (FHF⁻, 500 steps, MacBook Pro M1):

| Configuration | RT-NEO | RT-cNEO |
|--------------|--------|---------|
| Static Fock (default) | ~2-3 min | ~3-5 min |
| Time-dependent Fock | ~30-60 min | ~45-90 min |

**Recommendation**: Use static Fock for development, time-dependent for production.

---

## 🤝 Contributing

We follow SOLID principles and Clean Code practices:

```python
# Example: Adding a new field strategy
from rtcneo.strategies import FieldStrategy

class MyCustomField(FieldStrategy):
    def calculate_field(self, time: float) -> float:
        return ... # Your implementation
```

All contributions should include:
- Type hints
- Comprehensive docstrings
- Unit tests (in `tests/`)
- Example usage (in `examples/`)

---

## 📄 Citation

If you use RT-cNEO in your research, please cite:

**RT-NEO Method:**
```bibtex
@article{zhao2020rtneo,
  title={Real-time nuclear-electronic orbital dynamics},
  author={Zhao, L. and Wildman, A. and Tully, J.C. and Hammes-Schiffer, S.},
  journal={J. Chem. Phys.},
  volume={152},
  pages={224111},
  year={2020}
}
```

**cNEO Method:**
```bibtex
@article{xu2020cneo,
  title={Constrained nuclear-electronic orbital density functional theory},
  author={Xu, X. and Yang, Y.},
  journal={J. Chem. Phys.},
  volume={152},
  pages={084107},
  year={2020}
}
```

---

## 🔗 Related Methods

- **Ehrenfest-cNEO** (Liu et al., 2025) - Different from RT-cNEO!
  - Uses Ehrenfest dynamics (classical nuclei from start)
  - RT-cNEO: quantum nuclei + constraint potential

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/RT_cNEO/issues)
- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🎉 Acknowledgments

- **PySCF-NEO**: Yang's group for the NEO implementation
- **RT-NEO**: Hammes-Schiffer group for the original method
- **cNEO**: Yang group for the constrained NEO method

---

**Status**: ✅ Production-ready (v1.0.0)
**Last Updated**: October 2025
**Maintainer**: Federico Zahariev
