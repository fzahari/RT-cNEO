"""
External field strategies for RT-cNEO dynamics.

Implements Strategy pattern for different time-dependent external fields.
Follows Open/Closed Principle: easy to add new field types without modifying existing code.
"""

from abc import ABC, abstractmethod
import numpy as np


class FieldStrategy(ABC):
    """
    Abstract base class for external field generation strategies.

    Follows Open/Closed Principle: Open for extension, closed for modification.
    """

    @abstractmethod
    def calculate_field(self, time: float) -> float:
        """Calculate field strength at given time."""
        pass


class ConstantField(FieldStrategy):
    """Constant external field."""

    def __init__(self, strength: float):
        self.strength = strength

    def calculate_field(self, time: float) -> float:
        """Return constant field strength."""
        return self.strength


class LinearRampField(FieldStrategy):
    """Linear ramp to final field strength."""

    def __init__(self, ramp_time: float, final_strength: float):
        self.ramp_time = ramp_time
        self.final_strength = final_strength

    def calculate_field(self, time: float) -> float:
        """Linear interpolation from 0 to final_strength."""
        if time < self.ramp_time:
            return self.final_strength * time / self.ramp_time
        return self.final_strength


class CosineRampField(FieldStrategy):
    """Smooth cosine ramp to final field strength."""

    def __init__(self, ramp_time: float, final_strength: float):
        self.ramp_time = ramp_time
        self.final_strength = final_strength

    def calculate_field(self, time: float) -> float:
        """Smooth cosine interpolation from 0 to final_strength."""
        if time < self.ramp_time:
            return self.final_strength * (1 - np.cos(np.pi * time / self.ramp_time)) / 2
        return self.final_strength


class GaussianPulseField(FieldStrategy):
    """
    Gaussian pulse centered at specific time.

    Naturally decays to zero, allowing system to settle into stable state.
    Ideal for proton transfer simulations.
    """

    def __init__(self, center: float, width: float, amplitude: float):
        self.center = center
        self.width = width
        self.amplitude = amplitude

    def calculate_field(self, time: float) -> float:
        """Gaussian pulse: A * exp(-((t-t0)/σ)^2)."""
        return self.amplitude * np.exp(-((time - self.center) / self.width)**2)


class PulsedField(FieldStrategy):
    """Field that turns on and off at specific times."""

    def __init__(self, strength: float, turn_on_time: float, turn_off_time: float):
        self.strength = strength
        self.turn_on_time = turn_on_time
        self.turn_off_time = turn_off_time

    def calculate_field(self, time: float) -> float:
        """Return strength during pulse window, zero otherwise."""
        if self.turn_on_time <= time <= self.turn_off_time:
            return self.strength
        return 0.0
