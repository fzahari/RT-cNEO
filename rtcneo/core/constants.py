"""
Physical constants and parameter classes for RT-cNEO simulations.

This module contains all named constants, removing magic numbers from the codebase.
Follows Clean Code principles with clear, descriptive names.
"""

from dataclasses import dataclass, field
from typing import Dict
import numpy as np


class PhysicalConstants:
    """Physical constants in atomic units."""
    BOHR_TO_ANGSTROM = 0.529177
    ANGSTROM_TO_BOHR = 1.0 / BOHR_TO_ANGSTROM
    PROTON_MASS = 1836.15
    ELECTRON_MASS = 1.0
    HARTREE_TO_EV = 27.2114
    FEMTOSECOND_TO_AU = 41.341


@dataclass
class PotentialParameters:
    """Parameters for FHF- double-well potential."""
    quartic_coefficient: float = 0.1      # Coefficient for x^4 term
    quadratic_coefficient: float = 0.05   # Coefficient for x^2 term
    barrier_height: float = 0.02          # Gaussian barrier height
    barrier_width: float = 10.0           # Gaussian barrier width


@dataclass
class DynamicsConstants:
    """Constants for dynamics simulation."""
    DEFAULT_FIELD_RAMP_TIME_AU: float = 50.0
    DEFAULT_PULSE_CENTER_AU: float = 50.0
    DEFAULT_PULSE_WIDTH_AU: float = 20.0
    MAX_FORCE_HISTORY: int = 100
    CONSTRAINT_FORCE_MULTIPLIER: float = 2.0
    TRANSFER_THRESHOLD_ANGSTROM: float = 0.3
    PROGRESS_REPORT_INTERVAL: int = 100


@dataclass
class NumericalConstants:
    """Numerical thresholds for stability."""
    EIGENVALUE_FLOOR: float = 1e-14
    TRACE_THRESHOLD: float = 1e-10
    FIELD_COUPLING_FACTOR: float = 0.01


@dataclass
class SimulationParameters:
    """Immutable simulation parameters."""
    time_step: float = 0.1
    max_time: float = 500.0
    field_strength: float = 0.015
    smoothing_time: float = 20.0
    fluorine_distance: float = 2.3  # Angstroms
    basis_set: str = '6-31g*'
    proton_basis: str = 'pb4d'
    convergence_threshold: float = 1e-8
    max_scf_cycles: int = 100
    use_time_dependent_fock: bool = False  # Enable time-dependent Fock (expensive!)


@dataclass
class DynamicsState:
    """Represents the current state in dynamics simulation."""
    time: float
    electronic_density: np.ndarray
    nuclear_density: np.ndarray
    position: float
    energy: float
    constraint_force: float = 0.0

    def copy(self) -> 'DynamicsState':
        """Create a deep copy of the state."""
        return DynamicsState(
            time=self.time,
            electronic_density=self.electronic_density.copy(),
            nuclear_density=self.nuclear_density.copy(),
            position=self.position,
            energy=self.energy,
            constraint_force=self.constraint_force
        )


@dataclass
class SimulationResults:
    """Container for simulation results."""
    method: str
    times: np.ndarray
    positions: np.ndarray
    energies: np.ndarray
    constraint_forces: np.ndarray
    convergence_info: Dict = field(default_factory=dict)

    def get_final_position(self) -> float:
        """Get final proton position."""
        return self.positions[-1]

    def get_max_displacement(self) -> float:
        """Get maximum displacement from origin."""
        return np.max(np.abs(self.positions))

    def count_barrier_crossings(self) -> int:
        """Count number of times proton crosses x=0."""
        return np.sum(np.diff(np.sign(self.positions)) != 0)
