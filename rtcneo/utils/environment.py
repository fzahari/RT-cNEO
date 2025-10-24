"""
Environment configuration for RT-cNEO.

Critical macOS compatibility settings for PySCF-NEO.
"""

import os
import sys
from pathlib import Path


def configure_environment_for_macos() -> None:
    """
    Configure threading environment for macOS compatibility.

    CRITICAL: Must be called BEFORE importing numpy/scipy/PySCF to prevent
    BLAS threading deadlock on macOS Accelerate framework.
    """
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
    os.environ['BLAS'] = 'Accelerate'
    os.environ['OMP_NUM_THREADS'] = '1'       # CRITICAL for PySCF-NEO!
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'


def setup_pyscf_neo_path(pyscf_path: str = None) -> None:
    """
    Add Yang's PySCF-NEO to Python path.

    Args:
        pyscf_path: Path to PySCF-NEO installation. If None, uses default.
    """
    if pyscf_path is None:
        # Default path - update for your installation
        pyscf_path = '/Users/federicozahariev/Work/Programs/QEE_Split_Grouping/pyscf-master'

    pyscf_neo_path = Path(pyscf_path)
    if pyscf_neo_path.exists():
        sys.path.insert(0, str(pyscf_neo_path))
        return True
    else:
        print(f"Warning: PySCF-NEO path not found: {pyscf_path}")
        return False


def initialize_environment(pyscf_path: str = None) -> None:
    """
    Initialize complete environment for RT-cNEO.

    Call this at the start of your script before any scientific computing imports.

    Args:
        pyscf_path: Optional custom path to PySCF-NEO installation
    """
    configure_environment_for_macos()
    setup_pyscf_neo_path(pyscf_path)
