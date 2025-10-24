#!/usr/bin/env python3
"""
Basic RT-cNEO Example

Demonstrates constrained quantum dynamics (RT-cNEO) for FHF- proton transfer.
Includes constraint forces to extract smooth classical trajectory!

Usage:
    python 02_basic_rtcneo.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from legacy monolithic module
from rt_cneo_clean import (
    SimulationFactory,
    SimulationParameters,
    TrajectoryAnalyzer,
    GaussianPulseField
)


def main():
    """Run basic RT-cNEO simulation."""

    print("\n" + "="*80)
    print(" RT-cNEO: Constrained Quantum Dynamics")
    print(" (Quantum + constraint forces → smooth classical trajectory)")
    print("="*80)

    # Setup parameters
    params = SimulationParameters(
        time_step=0.1,
        max_time=500.0,
        field_strength=0.02,
        smoothing_time=20.0,        # RT-cNEO smoothing parameter!
        fluorine_distance=2.3,
        basis_set='sto-3g',
        proton_basis='pb4d'
    )

    print(f"\nRT-cNEO smoothing time: {params.smoothing_time} au")
    print("  (Controls how strongly quantum trajectory is smoothed)")

    # Setup field
    field = GaussianPulseField(center=50.0, width=20.0, amplitude=params.field_strength)

    # Create simulator
    print("\nCreating simulator...")
    simulator = SimulationFactory.create_simulator(
        parameters=params,
        field_strategy=field,
        use_simplified=False
    )

    # Run RT-cNEO
    print("\nRunning RT-cNEO simulation...")
    results = simulator.run_rtcneo()

    # Analyze
    print("\n" + "="*70)
    print(" Results")
    print("="*70)

    analyzer = TrajectoryAnalyzer()
    analysis = analyzer.analyze(results)
    analyzer.print_analysis(analysis)

    # Additional RT-cNEO metrics
    import numpy as np
    avg_constraint = np.mean(np.abs(results.constraint_forces))
    max_constraint = np.max(np.abs(results.constraint_forces))
    print(f"\nConstraint Force Statistics:")
    print(f"  Average magnitude: {avg_constraint*1000:.3f} ×10⁻³ au")
    print(f"  Maximum magnitude: {max_constraint*1000:.3f} ×10⁻³ au")

    # Save trajectory
    np.savetxt(
        "rtcneo_basic_trajectory.csv",
        np.column_stack([
            results.times,
            results.positions,
            results.energies,
            results.constraint_forces
        ]),
        header="Time(au), Position(Å), Energy(au), ConstraintForce(au)",
        delimiter=",",
        fmt="%.6e"
    )
    print(f"\nTrajectory saved to: rtcneo_basic_trajectory.csv")


if __name__ == "__main__":
    main()
