"""
Molecular system definitions for RT-cNEO.

Currently implements FHF- (bifluoride anion) with quantum proton.
"""

from typing import Optional
from .constants import SimulationParameters

# PySCF imports - handled by environment setup
try:
    from pyscf import gto
    PYSCF_AVAILABLE = True
except ImportError:
    PYSCF_AVAILABLE = False
    gto = None


class MolecularSystem:
    """
    Represents the FHF- molecular system with quantum proton.

    This class properly interfaces with Yang's PySCF-NEO implementation.
    """

    def __init__(self, parameters: SimulationParameters):
        self.parameters = parameters
        self._setup_geometry()
        self._build_molecule()

    def _setup_geometry(self) -> None:
        """Define molecular geometry for FHF-."""
        half_distance = self.parameters.fluorine_distance / 2

        # Classical nuclei positions
        self.classical_nuclei = [
            ('F', -half_distance, 0.0, 0.0),
            ('F', half_distance, 0.0, 0.0)
        ]

        # Quantum proton initial position
        # CRITICAL: Must start at or right of well minimum to allow rightward motion!
        # Left well minimum from barrier scan: -0.15 Å
        self.quantum_nuclei = [
            ('H', -0.15, 0.0, 0.0)  # At left well minimum!
        ]

    def _build_molecule(self) -> None:
        """Build PySCF molecule object."""
        if not PYSCF_AVAILABLE or gto is None:
            print("[INFO] Simplified mode: Skipping PySCF molecule build")
            self.mol = None
            return

        self.mol = gto.Mole()

        # Combine all nuclei
        all_atoms = self.classical_nuclei + self.quantum_nuclei
        self.mol.atom = [f'{atom} {x:.6f} {y:.6f} {z:.6f}'
                        for atom, x, y, z in all_atoms]

        self.mol.basis = self.parameters.basis_set
        self.mol.charge = -1  # FHF- anion
        self.mol.spin = 0     # Closed shell
        self.mol.unit = 'angstrom'
        self.mol.verbose = 4
        self.mol.build()

        self._validate_electron_count()

    def _validate_electron_count(self) -> None:
        """Ensure correct electron count for FHF-."""
        expected_electrons = 20
        if self.mol.nelectron != expected_electrons:
            raise ValueError(f"Expected {expected_electrons} electrons, got {self.mol.nelectron}")
