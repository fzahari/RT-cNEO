# RT-cNEO: Real-Time constrained Nuclear-Electronic Orbital Dynamics

RT-cNEO combines RT-NEO quantum dynamics and cNEO classical trajectory extraction for simulating quantum proton transfer.

## Quick Start

```python
from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters

params = SimulationParameters(
    time_step=0.1,
    max_time=500.0,
    field_strength=0.02
)

study = ComparisonStudy(params)
rtneo_results, rtcneo_results = study.run_full_comparison()
study.print_summary()
study.generate_report()
```

## Overview

RT-cNEO combines two published methods:

1. RT-NEO (Zhao et al., 2020) - Real-time quantum dynamics of electrons and quantum nuclei
2. cNEO (Xu & Yang, 2020) - Constrained NEO for classical trajectory extraction

Core mechanism:

```
H(t) = H₀ + f_constraint(t)·R̂ + V_external(t)·R̂

where:
  f_constraint = 2·(F_smooth - F_quantum)    [critical damping]
  F_smooth = exponential smoothing of F_quantum
  V_external = time-dependent driving field
```

Constraint is added as potential (modifies H), not energy minimization. Preserves quantum character (excited states, superpositions).

## Installation

Prerequisites:
```bash
# Python 3.8+
git clone https://github.com/theorychemyang/pyscf
cd pyscf && pip install -e .
```

Install:
```bash
cd RT_cNEO
pip install -e .
```

Verify:
```python
from rtcneo import SimulationFactory
from rtcneo.analysis import ComparisonStudy
```

## Examples

Basic RT-NEO:
```python
from rtcneo import SimulationFactory, SimulationParameters

params = SimulationParameters(time_step=0.1, max_time=500.0)
simulator = SimulationFactory.create_simulator(params)
results = simulator.run_rtneo()
```

Basic RT-cNEO:
```python
results = simulator.run_rtcneo()
print(f"Barrier crossings: {results.count_barrier_crossings()}")
```

Comparison:
```bash
python examples/03_comparison.py
```

Generates: comparison_full.png (4-panel plot), constraint_analysis.png, comparison_summary.txt, CSV data files

## Package Structure

```
rtcneo/
├── core/          # Constants, molecular system, ground state, propagator
├── strategies/    # Fields, potentials, constraints (strategy pattern)
├── dynamics/      # Simulator, factory, state
├── analysis/      # ComparisonStudy, visualization
└── utils/         # Environment, diagnostics
```

## Features

Implemented:
- Quantum propagation (unitary time evolution)
- Constraint as potential (preserves quantum character)
- External field support (time-dependent)
- Multiple field strategies (Gaussian pulse, linear ramp, cosine ramp)
- Ab initio forces (PySCF-NEO)
- Time-dependent Fock (optional, exact formalism)

ComparisonStudy metrics:
- Smoothness ratio
- Trajectory correlation
- Final position difference
- Energy drift
- Barrier crossing count

## Documentation

- examples/README.md - Examples guide
- DOCS/theory/RT_CNEO_COMPLETE.md - Theory
- rt_cneo_clean.py - Original monolithic implementation

Key concepts:

RT-NEO vs RT-cNEO:
- RT-NEO: Pure quantum dynamics, rapid oscillations possible
- RT-cNEO: Smoothed trajectory, preserves quantum character

External field requirement:
- Symmetric systems (FHF-) need external field to break symmetry
- Typical: 0.01-0.02 au (0.5-1.0 V/Å)

Time-dependent Fock:
- `use_time_dependent_fock=False` (default): Static Fock, fast, valid for short times
- `use_time_dependent_fock=True`: Time-dependent Fock, 10-100x slower, accurate

## Usage

Method development and benchmarking:
- Short time dynamics (<100 fs with static Fock)
- Excited state dynamics
- Constraint mechanism studies
- Quantum vs classical trajectory comparison

Approximations (default mode):
1. Static Fock matrix - electron-proton coupling not updated. Use `use_time_dependent_fock=True` for exact formalism.
2. Constraint force: `f = 2(F_smooth - F_quantum)`. Factor of 2 from critical damping theory (see DOCS/theory/RT_CNEO_COMPLETE.md Section 5).

## Performance

FHF-, 500 steps, MacBook Pro M1:

| Configuration | RT-NEO | RT-cNEO |
|--------------|--------|---------|
| Static Fock | 2-3 min | 3-5 min |
| Time-dependent Fock | 30-60 min | 45-90 min |

Use static Fock for development, time-dependent for production.

## Extending

Add field strategies:
```python
from rtcneo.strategies import FieldStrategy

class MyCustomField(FieldStrategy):
    def calculate_field(self, time: float) -> float:
        return ...
```

## Citation

RT-NEO method:
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

cNEO method:
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

## Related Methods

Ehrenfest-cNEO (Liu et al., 2025): Uses Ehrenfest dynamics (classical nuclei from start). RT-cNEO uses quantum nuclei with constraint potential.

## License

MIT License - see LICENSE

## Acknowledgments

Supported by National Science Foundation Grant No. OSI-2435255.

- PySCF-NEO: Yang's group
- RT-NEO: Hammes-Schiffer group
- cNEO: Yang group

Maintainer: Federico Zahariev
