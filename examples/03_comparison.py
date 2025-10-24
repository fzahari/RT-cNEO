#!/usr/bin/env python3
"""
RT-NEO vs RT-cNEO Comparison Example

This script demonstrates the comprehensive comparison tools for RT-NEO and RT-cNEO.
This is the EASIEST way to compare the two methods!

Usage:
    python 03_comparison.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rtcneo.analysis import ComparisonStudy
from rtcneo.core import SimulationParameters
from rtcneo.strategies import GaussianPulseField


def main():
    """Run comprehensive RT-NEO vs RT-cNEO comparison."""

    print("\n" + "="*80)
    print(" RT-NEO vs RT-cNEO COMPARISON")
    print(" Easy-to-use demonstration of quantum vs constrained dynamics")
    print("="*80)

    # ========================================================================
    # STEP 1: Setup simulation parameters
    # ========================================================================
    print("\n[Step 1/4] Setting up simulation parameters...")

    params = SimulationParameters(
        time_step=0.1,               # Time step in au (~0.0024 fs)
        max_time=500.0,              # Total simulation time in au (~12 fs)
        field_strength=0.02,         # External field strength in au (~1 V/Å)
        smoothing_time=20.0,         # RT-cNEO smoothing timescale in au
        fluorine_distance=2.3,       # F-F distance in Angstroms
        basis_set='sto-3g',          # Electronic basis set (fast for demo)
        proton_basis='pb4d',         # Nuclear basis (4 Gaussians for proton)
        use_time_dependent_fock=False  # Static Fock for speed (set True for accuracy)
    )

    print(f"  Time step: {params.time_step} au")
    print(f"  Total time: {params.max_time} au (~{params.max_time/41.341:.1f} fs)")
    print(f"  Field strength: {params.field_strength} au (~{params.field_strength*51.4:.1f} V/Å)")
    print(f"  Smoothing time: {params.smoothing_time} au")

    # ========================================================================
    # STEP 2: Setup external field strategy
    # ========================================================================
    print("\n[Step 2/4] Configuring external field...")

    # Gaussian pulse - naturally decays, good for proton transfer
    field = GaussianPulseField(
        center=50.0,                 # Pulse center time in au
        width=20.0,                  # Pulse width in au
        amplitude=params.field_strength
    )

    print(f"  Using Gaussian pulse field")
    print(f"  Pulse center: 50 au, width: 20 au")

    # ========================================================================
    # STEP 3: Create comparison study and run both methods
    # ========================================================================
    print("\n[Step 3/4] Running simulations...")
    print("  This will run BOTH RT-NEO and RT-cNEO automatically!")

    study = ComparisonStudy(
        parameters=params,
        field_strategy=field,
        potential_strategy=None  # Use default (auto-selects PySCF or model)
    )

    # This single command runs BOTH simulations!
    rtneo_results, rtcneo_results = study.run_full_comparison(verbose=True)

    # ========================================================================
    # STEP 4: Analyze and visualize results
    # ========================================================================
    print("\n[Step 4/4] Analyzing results...")

    # Print comprehensive summary
    study.print_summary()

    # Generate full report with plots and data files
    print("\nGenerating comprehensive report...")
    study.generate_report(output_dir="comparison_results")

    print("\n" + "="*80)
    print(" COMPARISON COMPLETE!")
    print("="*80)
    print("\nResults saved in: comparison_results/")
    print("  - comparison_full.png         (4-panel comparison plot)")
    print("  - constraint_analysis.png     (RT-cNEO constraint analysis)")
    print("  - comparison_summary.txt      (detailed text summary)")
    print("  - rtneo_trajectory.csv        (RT-NEO data)")
    print("  - rtcneo_trajectory.csv       (RT-cNEO data)")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
