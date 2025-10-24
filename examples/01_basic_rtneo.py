#!/usr/bin/env python3
"""
Basic RT-NEO Example

Demonstrates pure quantum dynamics (RT-NEO) for FHF- proton transfer.
No constraint forces - just quantum time evolution!

Usage:
    python 01_basic_rtneo.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from legacy monolithic module (will be updated when refactoring complete)
from rt_cneo_clean import (
    SimulationFactory,
    SimulationParameters,
    TrajectoryAnalyzer,
    GaussianPulseField
)


def main():
    """Run basic RT-NEO simulation."""

    print("\n" + "="*80)
    print(" RT-NEO: Pure Quantum Dynamics")
    print(" (No trajectory smoothing - just quantum time evolution)")
    print("="*80)

    # Setup parameters
    params = SimulationParameters(
        time_step=0.1,
        max_time=500.0,
        field_strength=0.02,
        fluorine_distance=2.3,
        basis_set='sto-3g',
        proton_basis='pb4d'
    )

    # Setup field
    field = GaussianPulseField(center=50.0, width=20.0, amplitude=params.field_strength)

    # Create simulator
    print("\nCreating simulator...")
    simulator = SimulationFactory.create_simulator(
        parameters=params,
        field_strategy=field,
        use_simplified=False
    )

    # Run RT-NEO
    print("\nRunning RT-NEO simulation...")
    results = simulator.run_rtneo()

    # Analyze
    print("\n" + "="*70)
    print(" Results")
    print("="*70)

    analyzer = TrajectoryAnalyzer()
    analysis = analyzer.analyze(results)
    analyzer.print_analysis(analysis)

    # Save trajectory
    import numpy as np
    np.savetxt(
        "rtneo_basic_trajectory.csv",
        np.column_stack([results.times, results.positions, results.energies]),
        header="Time(au), Position(Å), Energy(au)",
        delimiter=",",
        fmt="%.6e"
    )
    print(f"\nTrajectory saved to: rtneo_basic_trajectory.csv")


if __name__ == "__main__":
    main()
