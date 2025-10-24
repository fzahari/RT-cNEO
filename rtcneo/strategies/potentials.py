"""
Potential energy surface strategies for RT-cNEO.

Implements Strategy pattern for different PES calculations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import numpy as np

from ..core.constants import PhysicalConstants, PotentialParameters


class PotentialStrategy(ABC):
    """
    Abstract base class for potential energy surface strategies.

    Follows Open/Closed Principle: Can add new potentials without modifying existing code.
    """

    @abstractmethod
    def calculate_force(self, position: float) -> float:
        """
        Calculate force at given position.

        Force is negative gradient: F = -dV/dx
        """
        pass


class DoubleWellPotential(PotentialStrategy):
    """
    Symmetric double-well potential for proton transfer.

    V(x) = a*x^4 - b*x^2 + c*exp(-d*x^2)

    This is a MODEL potential with adjustable parameters. For realistic simulations,
    use PySCFGradientPotential which computes actual ab initio forces.
    """

    def __init__(self, parameters: Optional[PotentialParameters] = None):
        self.params = parameters or PotentialParameters()

    def calculate_force(self, position: float) -> float:
        """
        Calculate force at given position.

        Force is negative gradient: F = -dV/dx
        V(x) = a*x^4 - b*x^2 + c*exp(-d*x^2)

        Args:
            position: Position in Ångströms

        Returns:
            Force in atomic units (Hartree/Bohr)
        """
        quartic_term = self._calculate_quartic_force(position)
        quadratic_term = self._calculate_quadratic_force(position)
        gaussian_barrier_term = self._calculate_gaussian_barrier_force(position)

        # Sum gives force in Hartree/Ångström (since position is in Å)
        force_per_angstrom = quartic_term + quadratic_term + gaussian_barrier_term

        # Convert from Hartree/Ångström to atomic units (Hartree/Bohr)
        force_au = force_per_angstrom * PhysicalConstants.BOHR_TO_ANGSTROM

        return force_au

    def _calculate_quartic_force(self, position: float) -> float:
        """Force from quartic term: -d/dx(a*x^4) = -4*a*x^3."""
        return -4.0 * self.params.quartic_coefficient * position**3

    def _calculate_quadratic_force(self, position: float) -> float:
        """Force from quadratic term: -d/dx(-b*x^2) = 2*b*x."""
        return 2.0 * self.params.quadratic_coefficient * position

    def _calculate_gaussian_barrier_force(self, position: float) -> float:
        """Force from Gaussian barrier: -d/dx(c*exp(-d*x^2)) = 2*c*d*x*exp(-d*x^2)."""
        exponential = np.exp(-self.params.barrier_width * position**2)
        return (2.0 * self.params.barrier_height * self.params.barrier_width
                * position * exponential)


class PySCFGradientPotential(PotentialStrategy):
    """
    Real ab initio potential using PySCF-NEO numerical gradients.

    Uses finite difference method to calculate force from actual NEO-HF
    potential energy surface. This is the CORRECT way to get forces!
    """

    def __init__(self, neo_calculator, step_size: float = 0.001):
        """
        Initialize with NEO calculator.

        Args:
            neo_calculator: NEOCalculator instance with initialized NEO system
            step_size: Finite difference step size in Angstroms (default: 0.001 Å)
        """
        self.neo_calc = neo_calculator
        self.step_size = step_size  # in Angstroms

        # Create PES scanner for fast energy calculations
        if self.neo_calc.neo_mf is not None:
            print("[DEBUG] Creating PES scanner for gradient calculations...")
            self.pes_scanner = self.neo_calc.neo_mf.as_scanner()
        else:
            raise ValueError("NEO mean-field calculation must be run before creating gradient potential")

        # Cache geometry template
        self._cache_geometry_template()

        # Statistics
        self.num_gradient_calls = 0
        self.num_energy_evals = 0

    def _cache_geometry_template(self) -> None:
        """Cache the base geometry for efficient updates."""
        # Store F-F-H geometry as numpy array
        all_atoms = (self.neo_calc.system.classical_nuclei +
                    self.neo_calc.system.quantum_nuclei)

        self.geometry_template = np.array([
            [atom_data[1], atom_data[2], atom_data[3]]  # x, y, z
            for atom_data in all_atoms
        ])

        # Proton is last atom (index 2)
        self.proton_index = 2
        print(f"[DEBUG] Geometry template cached: {self.geometry_template.shape}")

    def calculate_force(self, position: float) -> float:
        """
        Calculate actual quantum mechanical force using numerical gradient.

        Force F = -dE/dx calculated via centered finite difference:
        F(x) = -(E(x+δ) - E(x-δ)) / (2δ)

        Args:
            position: Proton position in Angstroms

        Returns:
            Force in atomic units
        """
        self.num_gradient_calls += 1

        # Create geometries for finite difference
        geom_minus = self.geometry_template.copy()
        geom_plus = self.geometry_template.copy()

        # Update proton position (x-coordinate only)
        geom_minus[self.proton_index, 0] = position - self.step_size
        geom_plus[self.proton_index, 0] = position + self.step_size

        # Calculate energies at displaced geometries
        energy_minus = self._calculate_energy_at_geometry(geom_minus)
        energy_plus = self._calculate_energy_at_geometry(geom_plus)

        self.num_energy_evals += 2

        # Centered finite difference for gradient
        gradient = (energy_plus - energy_minus) / (2.0 * self.step_size)

        # Force is negative gradient: F = -dE/dx
        force = -gradient

        # Convert from Hartree/Angstrom to atomic units (Hartree/Bohr)
        force_au = force * PhysicalConstants.BOHR_TO_ANGSTROM

        return force_au

    def _calculate_energy_at_geometry(self, geometry: np.ndarray) -> float:
        """
        Calculate NEO-HF energy at given geometry.

        Args:
            geometry: Geometry as (N_atoms, 3) array in Angstroms

        Returns:
            Total energy in Hartree
        """
        # Use scanner for fast energy calculation
        energy = self.pes_scanner(geometry)
        return energy

    def get_statistics(self) -> Dict:
        """Return statistics about gradient calculations."""
        return {
            'num_gradient_calls': self.num_gradient_calls,
            'num_energy_evals': self.num_energy_evals,
            'avg_evals_per_gradient': (self.num_energy_evals / self.num_gradient_calls
                                      if self.num_gradient_calls > 0 else 0)
        }
