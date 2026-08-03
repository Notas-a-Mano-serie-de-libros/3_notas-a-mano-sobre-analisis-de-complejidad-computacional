"""Contrato compartido para simulaciones experimentales de los capítulos 2, 4 y 6."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


MINIMUM_SAMPLING_POINTS = 10
MAXIMUM_SAMPLING_POINTS = 1_000
DEFAULT_SAMPLING_POINTS = 1_000
UNRESTRICTED_MAXIMUM = 10**10


@dataclass(frozen=True)
class SimulationConfig:
    """Parámetros normalizados que determinan una ejecución experimental."""

    maximum_n: int
    sampling_points: int = DEFAULT_SAMPLING_POINTS
    restrict_maximum: bool = True
    executions: int = 10

    def normalized(self) -> "SimulationConfig":
        return SimulationConfig(
            maximum_n=max(1, int(self.maximum_n)),
            sampling_points=clamp_sampling_points(self.sampling_points),
            restrict_maximum=bool(self.restrict_maximum),
            executions=max(1, int(self.executions)),
        )


def clamp_sampling_points(value: int) -> int:
    return max(MINIMUM_SAMPLING_POINTS, min(MAXIMUM_SAMPLING_POINTS, int(value)))


def next_order_of_magnitude(value: int) -> int:
    value = max(1, int(value))
    return 10 ** (int(math.floor(math.log10(value))) + 1)


def previous_order_of_magnitude(value: int) -> int:
    value = max(1, int(value))
    exponent = int(math.ceil(math.log10(value))) - 1
    return 10 ** max(0, exponent)


def effective_execution_limit(safe_maximum: int, restrict_maximum: bool) -> int:
    return max(1, int(safe_maximum)) if restrict_maximum else UNRESTRICTED_MAXIMUM


def build_experiment_sizes(
    maximum_n: int,
    max_safe_elements: int,
    points: int = DEFAULT_SAMPLING_POINTS,
) -> tuple[np.ndarray, np.ndarray]:
    """Construye tamaños únicos y ordenados, incluso para intervalos pequeños."""

    maximum_n = max(1, int(maximum_n))
    safe_maximum = max(1, min(maximum_n, int(max_safe_elements)))
    point_count = min(clamp_sampling_points(points), safe_maximum)
    dense_sizes = np.linspace(1, safe_maximum, num=point_count, dtype=np.int64)
    maximum_exponent = int(math.log10(maximum_n)) if maximum_n >= 10 else 0
    checkpoints = np.array(
        [10**exponent for exponent in range(1, maximum_exponent + 1)],
        dtype=np.int64,
    )
    executable_checkpoints = checkpoints[checkpoints <= safe_maximum]
    execution_sizes = np.unique(np.concatenate((dense_sizes, executable_checkpoints)))
    return execution_sizes, checkpoints


__all__ = [
    "DEFAULT_SAMPLING_POINTS",
    "MAXIMUM_SAMPLING_POINTS",
    "MINIMUM_SAMPLING_POINTS",
    "SimulationConfig",
    "build_experiment_sizes",
    "clamp_sampling_points",
    "effective_execution_limit",
    "next_order_of_magnitude",
    "previous_order_of_magnitude",
]
