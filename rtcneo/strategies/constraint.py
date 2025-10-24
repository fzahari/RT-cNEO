"""
Constraint force calculation for RT-cNEO.

Implements exponential smoothing and constraint force calculation following
the RT-cNEO formalism.
"""

from typing import Optional, List, Tuple
import numpy as np

from .potentials import PotentialStrategy
from ..core.constants import DynamicsConstants


class ForceSmoother:
    """
    Applies exponential smoothing to force trajectory.

    Separated from force calculation following Single Responsibility Principle.
    """

    def __init__(self, smoothing_time: float):
        self.smoothing_time = smoothing_time
        self.previous_smoothed_force: Optional[float] = None

    def smooth(self, current_force: float, time_step: float) -> float:
        """
        Apply exponential smoothing to force.

        f_smooth(t) = α * f_smooth(t-Δt) + (1-α) * f(t)
        where α = exp(-Δt / τ_smooth)
        """
        if self.previous_smoothed_force is None:
            smoothed_force = current_force
        else:
            decay_factor = np.exp(-time_step / self.smoothing_time)
            smoothed_force = (decay_factor * self.previous_smoothed_force
                            + (1 - decay_factor) * current_force)

        self.previous_smoothed_force = smoothed_force
        return smoothed_force

    def reset(self) -> None:
        """Reset smoothing history."""
        self.previous_smoothed_force = None


class ForceHistory:
    """
    Manages history of force values.

    Separated from smoothing following Single Responsibility Principle.
    """

    def __init__(self, max_size: int = DynamicsConstants.MAX_FORCE_HISTORY):
        self.max_size = max_size
        self.history: List[float] = []

    def append(self, force: float) -> None:
        """Add force to history, maintaining max size."""
        self.history.append(force)
        if len(self.history) > self.max_size:
            self.history.pop(0)

    def get_recent(self, count: int) -> List[float]:
        """Get most recent force values."""
        return self.history[-count:] if len(self.history) >= count else self.history

    def clear(self) -> None:
        """Clear history."""
        self.history.clear()


class ConstraintForceCalculator:
    """
    Calculates RT-cNEO constraint force.

    REFACTORED: Now follows Single Responsibility Principle.
    - PotentialStrategy handles force calculation
    - ForceSmoother handles smoothing
    - This class only computes constraint from smoothed vs quantum force
    """

    def __init__(self,
                 potential_strategy: PotentialStrategy,
                 force_smoother: ForceSmoother,
                 force_history: Optional[ForceHistory] = None):
        self.potential = potential_strategy
        self.smoother = force_smoother
        self.history = force_history or ForceHistory()

    def calculate_constraint_force(self,
                                   position: float,
                                   time_step: float) -> Tuple[float, float]:
        """
        Calculate constraint force for RT-cNEO.

        Returns:
            (quantum_force, constraint_force)
        """
        # Calculate quantum force from potential
        quantum_force = self.potential.calculate_force(position)

        # Apply smoothing
        smoothed_force = self.smoother.smooth(quantum_force, time_step)

        # Constraint force penalizes deviations from smooth trajectory
        constraint_force = (DynamicsConstants.CONSTRAINT_FORCE_MULTIPLIER
                          * (smoothed_force - quantum_force))

        # Track history
        self.history.append(smoothed_force)

        return quantum_force, constraint_force

    def reset(self) -> None:
        """Reset all components."""
        self.smoother.reset()
        self.history.clear()
