# RT-cNEO Quick Start

## Installation and Run

```bash
pip install -e .
cd examples
python 03_comparison.py
```

## Output

comparison_results/:
- comparison_full.png: 4-panel plot (position, energy, velocity, phase space)
- constraint_analysis.png: RT-cNEO constraint forces
- comparison_summary.txt: Quantitative metrics
- rtneo_trajectory.csv: RT-NEO data
- rtcneo_trajectory.csv: RT-cNEO data with constraint forces

## Code Usage

```python
from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters

params = SimulationParameters(
    time_step=0.1,
    max_time=500.0,
    field_strength=0.02
)

study = ComparisonStudy(params)
rtneo, rtcneo = study.run_full_comparison()
study.print_summary()
study.generate_report()
```

## Documentation

- examples/README.md: Examples
- DOCS/theory/RT_CNEO_COMPLETE.md: Theory
