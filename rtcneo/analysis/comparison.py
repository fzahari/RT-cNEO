"""
Comprehensive RT-NEO vs RT-cNEO comparison tools.

This module provides high-level tools for comparing pure quantum dynamics (RT-NEO)
with constrained trajectory extraction (RT-cNEO).
"""

from typing import Dict, Optional, Tuple
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Import from monolithic version for now (will be refactored)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from rt_cneo_clean import (
        SimulationFactory,
        SimulationResults,
        TrajectoryAnalyzer,
        SimulationParameters
    )
    RTCNEO_AVAILABLE = True
except ImportError:
    RTCNEO_AVAILABLE = False
    print("Warning: rt_cneo_clean not available. Using fallback mode.")


class ComparisonMetrics:
    """Calculate quantitative metrics comparing RT-NEO and RT-cNEO."""

    @staticmethod
    def calculate_smoothness_ratio(rtneo_results: SimulationResults,
                                   rtcneo_results: SimulationResults) -> float:
        """
        Calculate how much smoother RT-cNEO trajectory is compared to RT-NEO.

        Returns ratio > 1 if RT-cNEO is smoother.
        """
        dt = rtneo_results.times[1] - rtneo_results.times[0]

        # Calculate accelerations (second derivative of position)
        rtneo_vel = np.diff(rtneo_results.positions) / dt
        rtcneo_vel = np.diff(rtcneo_results.positions) / dt

        rtneo_accel = np.diff(rtneo_vel) / dt
        rtcneo_accel = np.diff(rtcneo_vel) / dt

        # Smoothness = inverse of acceleration variance
        rtneo_roughness = np.std(rtneo_accel)
        rtcneo_roughness = np.std(rtcneo_accel)

        if rtcneo_roughness > 0:
            return rtneo_roughness / rtcneo_roughness
        return float('inf')

    @staticmethod
    def calculate_final_position_difference(rtneo_results: SimulationResults,
                                           rtcneo_results: SimulationResults) -> float:
        """Calculate difference in final positions (Angstroms)."""
        return abs(rtneo_results.get_final_position() - rtcneo_results.get_final_position())

    @staticmethod
    def calculate_trajectory_correlation(rtneo_results: SimulationResults,
                                        rtcneo_results: SimulationResults) -> float:
        """Calculate Pearson correlation between trajectories."""
        return np.corrcoef(rtneo_results.positions, rtcneo_results.positions)[0, 1]

    @staticmethod
    def calculate_energy_drift_comparison(rtneo_results: SimulationResults,
                                         rtcneo_results: SimulationResults) -> Dict[str, float]:
        """Compare energy conservation between methods."""
        rtneo_drift = np.std(rtneo_results.energies) / np.abs(np.mean(rtneo_results.energies))
        rtcneo_drift = np.std(rtcneo_results.energies) / np.abs(np.mean(rtcneo_results.energies))

        return {
            'rtneo_drift': rtneo_drift,
            'rtcneo_drift': rtcneo_drift,
            'drift_ratio': rtneo_drift / rtcneo_drift if rtcneo_drift > 0 else float('inf')
        }


class ComparisonPlotter:
    """Create publication-quality comparison plots."""

    @staticmethod
    def plot_full_comparison(rtneo_results: SimulationResults,
                            rtcneo_results: SimulationResults,
                            save_path: Optional[str] = None) -> plt.Figure:
        """
        Create comprehensive 4-panel comparison plot.

        Panels:
        1. Position trajectories
        2. Energy evolution
        3. Velocity comparison
        4. Phase space (position vs velocity)
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Panel 1: Position trajectories
        ax1 = axes[0, 0]
        ax1.plot(rtneo_results.times, rtneo_results.positions,
                'r-', alpha=0.7, linewidth=1.5, label='RT-NEO (quantum)')
        ax1.plot(rtcneo_results.times, rtcneo_results.positions,
                'b-', linewidth=2, label='RT-cNEO (constrained)')
        ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax1.axhline(y=0.3, color='g', linestyle=':', alpha=0.3, label='Transfer threshold')
        ax1.set_xlabel('Time (au)', fontsize=11)
        ax1.set_ylabel('Proton Position (Å)', fontsize=11)
        ax1.set_title('Trajectory Comparison', fontsize=12, fontweight='bold')
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Panel 2: Energy evolution
        ax2 = axes[0, 1]
        rtneo_e0 = rtneo_results.energies[0]
        rtcneo_e0 = rtcneo_results.energies[0]
        ax2.plot(rtneo_results.times, (rtneo_results.energies - rtneo_e0) * 27.2114,
                'r-', alpha=0.7, linewidth=1.5, label='RT-NEO')
        ax2.plot(rtcneo_results.times, (rtcneo_results.energies - rtcneo_e0) * 27.2114,
                'b-', linewidth=2, label='RT-cNEO')
        ax2.set_xlabel('Time (au)', fontsize=11)
        ax2.set_ylabel('Energy Change (eV)', fontsize=11)
        ax2.set_title('Energy Conservation', fontsize=12, fontweight='bold')
        ax2.legend(loc='best', fontsize=9)
        ax2.grid(True, alpha=0.3)

        # Panel 3: Velocity comparison
        ax3 = axes[1, 0]
        dt = rtneo_results.times[1] - rtneo_results.times[0]
        rtneo_vel = np.diff(rtneo_results.positions) / dt
        rtcneo_vel = np.diff(rtcneo_results.positions) / dt
        time_vel = rtneo_results.times[:-1]

        ax3.plot(time_vel, rtneo_vel, 'r-', alpha=0.7, linewidth=1.5, label='RT-NEO')
        ax3.plot(time_vel, rtcneo_vel, 'b-', linewidth=2, label='RT-cNEO')
        ax3.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax3.set_xlabel('Time (au)', fontsize=11)
        ax3.set_ylabel('Velocity (Å/au)', fontsize=11)
        ax3.set_title('Velocity Evolution', fontsize=12, fontweight='bold')
        ax3.legend(loc='best', fontsize=9)
        ax3.grid(True, alpha=0.3)

        # Panel 4: Phase space
        ax4 = axes[1, 1]
        ax4.plot(rtneo_results.positions[:-1], rtneo_vel,
                'r-', alpha=0.5, linewidth=1, label='RT-NEO')
        ax4.plot(rtcneo_results.positions[:-1], rtcneo_vel,
                'b-', linewidth=1.5, label='RT-cNEO')
        ax4.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        ax4.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax4.set_xlabel('Position (Å)', fontsize=11)
        ax4.set_ylabel('Velocity (Å/au)', fontsize=11)
        ax4.set_title('Phase Space', fontsize=12, fontweight='bold')
        ax4.legend(loc='best', fontsize=9)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Comparison plot saved to: {save_path}")

        return fig

    @staticmethod
    def plot_constraint_analysis(rtcneo_results: SimulationResults,
                                 save_path: Optional[str] = None) -> plt.Figure:
        """Create detailed analysis of constraint forces in RT-cNEO."""
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))

        # Panel 1: Constraint force over time
        ax1 = axes[0]
        ax1.plot(rtcneo_results.times, rtcneo_results.constraint_forces * 1000,
                'g-', linewidth=1.5)
        ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax1.set_xlabel('Time (au)', fontsize=11)
        ax1.set_ylabel('Constraint Force (×10⁻³ au)', fontsize=11)
        ax1.set_title('RT-cNEO Constraint Force Evolution', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Panel 2: Constraint force vs position
        ax2 = axes[1]
        scatter = ax2.scatter(rtcneo_results.positions, rtcneo_results.constraint_forces * 1000,
                             c=rtcneo_results.times, cmap='viridis', s=10, alpha=0.6)
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax2.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        ax2.set_xlabel('Position (Å)', fontsize=11)
        ax2.set_ylabel('Constraint Force (×10⁻³ au)', fontsize=11)
        ax2.set_title('Constraint Force vs Position (colored by time)', fontsize=12, fontweight='bold')
        cbar = plt.colorbar(scatter, ax=ax2)
        cbar.set_label('Time (au)', fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Constraint analysis plot saved to: {save_path}")

        return fig


class ComparisonStudy:
    """
    High-level interface for comprehensive RT-NEO vs RT-cNEO comparison studies.

    This is the main class users should interact with for comparison work.
    """

    def __init__(self, parameters: SimulationParameters,
                 field_strategy=None,
                 potential_strategy=None):
        """
        Initialize comparison study.

        Args:
            parameters: Simulation parameters to use
            field_strategy: Optional custom field strategy
            potential_strategy: Optional custom potential strategy
        """
        if not RTCNEO_AVAILABLE:
            raise ImportError("rt_cneo_clean module not available")

        self.parameters = parameters
        self.field_strategy = field_strategy
        self.potential_strategy = potential_strategy

        self.rtneo_results = None
        self.rtcneo_results = None
        self.metrics = None

    def run_full_comparison(self, verbose: bool = True) -> Tuple[SimulationResults, SimulationResults]:
        """
        Run both RT-NEO and RT-cNEO simulations.

        Returns:
            (rtneo_results, rtcneo_results)
        """
        if verbose:
            print("\n" + "="*80)
            print(" RT-NEO vs RT-cNEO COMPARISON STUDY")
            print("="*80)

        # Create simulator
        simulator = SimulationFactory.create_simulator(
            parameters=self.parameters,
            field_strategy=self.field_strategy,
            potential_strategy=self.potential_strategy,
            use_simplified=False
        )

        # Run RT-NEO
        if verbose:
            print("\n[1/2] Running RT-NEO (pure quantum dynamics)...")
        self.rtneo_results = simulator.run_rtneo()

        # Run RT-cNEO
        if verbose:
            print("\n[2/2] Running RT-cNEO (constrained dynamics)...")
        self.rtcneo_results = simulator.run_rtcneo()

        # Calculate metrics
        self.metrics = self._calculate_all_metrics()

        if verbose:
            print("\n" + "="*80)
            print(" COMPARISON COMPLETE")
            print("="*80)

        return self.rtneo_results, self.rtcneo_results

    def _calculate_all_metrics(self) -> Dict:
        """Calculate all comparison metrics."""
        if self.rtneo_results is None or self.rtcneo_results is None:
            raise RuntimeError("Must run simulations before calculating metrics")

        return {
            'smoothness_ratio': ComparisonMetrics.calculate_smoothness_ratio(
                self.rtneo_results, self.rtcneo_results
            ),
            'final_position_diff': ComparisonMetrics.calculate_final_position_difference(
                self.rtneo_results, self.rtcneo_results
            ),
            'trajectory_correlation': ComparisonMetrics.calculate_trajectory_correlation(
                self.rtneo_results, self.rtcneo_results
            ),
            'energy_drift': ComparisonMetrics.calculate_energy_drift_comparison(
                self.rtneo_results, self.rtcneo_results
            ),
            'rtneo_crossings': self.rtneo_results.count_barrier_crossings(),
            'rtcneo_crossings': self.rtcneo_results.count_barrier_crossings(),
        }

    def print_summary(self) -> None:
        """Print comprehensive comparison summary."""
        if self.metrics is None:
            raise RuntimeError("Must run comparison before printing summary")

        print("\n" + "="*80)
        print(" COMPARISON SUMMARY")
        print("="*80)

        # Final positions
        print("\nFinal Positions:")
        print(f"  RT-NEO:  {self.rtneo_results.get_final_position():7.3f} Å")
        print(f"  RT-cNEO: {self.rtcneo_results.get_final_position():7.3f} Å")
        print(f"  Difference: {self.metrics['final_position_diff']:.3f} Å")

        # Transfer assessment
        print("\nTransfer Assessment:")
        analyzer = TrajectoryAnalyzer()
        rtneo_analysis = analyzer.analyze(self.rtneo_results)
        rtcneo_analysis = analyzer.analyze(self.rtcneo_results)
        print(f"  RT-NEO:  {rtneo_analysis['transfer_assessment']}")
        print(f"  RT-cNEO: {rtcneo_analysis['transfer_assessment']}")

        # Smoothness
        print("\nTrajectory Smoothness:")
        print(f"  RT-cNEO is {self.metrics['smoothness_ratio']:.2f}× smoother than RT-NEO")

        # Barrier crossings
        print("\nBarrier Crossings:")
        print(f"  RT-NEO:  {self.metrics['rtneo_crossings']} crossings")
        print(f"  RT-cNEO: {self.metrics['rtcneo_crossings']} crossings")

        # Correlation
        print("\nTrajectory Correlation:")
        print(f"  Pearson r = {self.metrics['trajectory_correlation']:.4f}")

        # Energy conservation
        print("\nEnergy Conservation:")
        print(f"  RT-NEO drift:  {self.metrics['energy_drift']['rtneo_drift']:.2e}")
        print(f"  RT-cNEO drift: {self.metrics['energy_drift']['rtcneo_drift']:.2e}")

        print("="*80)

    def generate_report(self, output_dir: str = "comparison_results") -> None:
        """
        Generate comprehensive comparison report with plots and data files.

        Creates:
        - Full comparison plot (4 panels)
        - Constraint analysis plot
        - Summary text file
        - CSV data files for both methods
        """
        if self.metrics is None:
            raise RuntimeError("Must run comparison before generating report")

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"\nGenerating comparison report in: {output_path}/")

        # Generate plots
        plotter = ComparisonPlotter()

        comparison_fig = plotter.plot_full_comparison(
            self.rtneo_results,
            self.rtcneo_results,
            save_path=str(output_path / "comparison_full.png")
        )
        plt.close(comparison_fig)

        constraint_fig = plotter.plot_constraint_analysis(
            self.rtcneo_results,
            save_path=str(output_path / "constraint_analysis.png")
        )
        plt.close(constraint_fig)

        # Save data files
        np.savetxt(
            output_path / "rtneo_trajectory.csv",
            np.column_stack([
                self.rtneo_results.times,
                self.rtneo_results.positions,
                self.rtneo_results.energies
            ]),
            header="Time(au), Position(Å), Energy(au)",
            delimiter=",",
            fmt="%.6e"
        )

        np.savetxt(
            output_path / "rtcneo_trajectory.csv",
            np.column_stack([
                self.rtcneo_results.times,
                self.rtcneo_results.positions,
                self.rtcneo_results.energies,
                self.rtcneo_results.constraint_forces
            ]),
            header="Time(au), Position(Å), Energy(au), ConstraintForce(au)",
            delimiter=",",
            fmt="%.6e"
        )

        # Generate text summary
        with open(output_path / "comparison_summary.txt", 'w') as f:
            f.write("="*80 + "\n")
            f.write(" RT-NEO vs RT-cNEO COMPARISON REPORT\n")
            f.write("="*80 + "\n\n")

            f.write("Simulation Parameters:\n")
            for key, value in self.parameters.__dict__.items():
                f.write(f"  {key:25s}: {value}\n")

            f.write("\n" + "-"*80 + "\n")
            f.write(" RESULTS\n")
            f.write("-"*80 + "\n\n")

            f.write(f"Final Positions:\n")
            f.write(f"  RT-NEO:  {self.rtneo_results.get_final_position():.6f} Å\n")
            f.write(f"  RT-cNEO: {self.rtcneo_results.get_final_position():.6f} Å\n")
            f.write(f"  Difference: {self.metrics['final_position_diff']:.6f} Å\n\n")

            f.write(f"Smoothness Ratio: {self.metrics['smoothness_ratio']:.4f}\n")
            f.write(f"Trajectory Correlation: {self.metrics['trajectory_correlation']:.4f}\n\n")

            f.write(f"Barrier Crossings:\n")
            f.write(f"  RT-NEO:  {self.metrics['rtneo_crossings']}\n")
            f.write(f"  RT-cNEO: {self.metrics['rtcneo_crossings']}\n\n")

            f.write(f"Energy Drift:\n")
            f.write(f"  RT-NEO:  {self.metrics['energy_drift']['rtneo_drift']:.6e}\n")
            f.write(f"  RT-cNEO: {self.metrics['energy_drift']['rtcneo_drift']:.6e}\n")

        print(f"✓ Report generated successfully!")
        print(f"  - comparison_full.png")
        print(f"  - constraint_analysis.png")
        print(f"  - comparison_summary.txt")
        print(f"  - rtneo_trajectory.csv")
        print(f"  - rtcneo_trajectory.csv")
