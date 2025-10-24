"""
RT-cNEO: Real-Time constrained Nuclear-Electronic Orbital dynamics.

A synthesis of RT-NEO quantum dynamics and cNEO classical trajectory extraction
for simulating quantum proton transfer in molecular systems like FHF-.

Quick Start:
-----------
>>> from rtcneo import SimulationFactory, SimulationParameters
>>> from rtcneo.strategies import GaussianPulseField
>>>
>>> params = SimulationParameters(time_step=0.1, max_time=500.0)
>>> simulator = SimulationFactory.create_simulator(params)
>>> results = simulator.run_rtcneo()

For RT-NEO vs RT-cNEO comparison:
---------------------------------
>>> from rtcneo.analysis import ComparisonStudy
>>> study = ComparisonStudy(params)
>>> results = study.run_full_comparison()
>>> study.generate_report()
"""

__version__ = "1.0.0"
__author__ = "Federico Zahariev"
__email__ = "fzahari@iastate.edu"

# Initialize environment FIRST
from .utils.environment import initialize_environment
initialize_environment()

# Core imports
from .core.constants import (
    PhysicalConstants,
    SimulationParameters,
    DynamicsState,
    SimulationResults
)

# Re-export the old monolithic module for backwards compatibility
# This allows: from rtcneo import SimulationFactory
try:
    # Import from modularized structure when complete
    from .dynamics.factory import SimulationFactory
    from .dynamics.simulator import DynamicsSimulator
except ImportError:
    # Fall back to monolithic version during transition
    import sys
    import os
    # Add parent directory to path to import rt_cneo_clean
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    try:
        from rt_cneo_clean import SimulationFactory, DynamicsSimulator
    except ImportError:
        print("Warning: Could not import SimulationFactory. Module structure incomplete.")
        SimulationFactory = None
        DynamicsSimulator = None

__all__ = [
    'PhysicalConstants',
    'SimulationParameters',
    'DynamicsState',
    'SimulationResults',
    'SimulationFactory',
    'DynamicsSimulator',
]
