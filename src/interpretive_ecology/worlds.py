"""Surface-distinct synthetic worlds sharing an undisclosed dynamic."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class Observation:
    world_id: str
    input_name: str
    state_name: str
    inputs: tuple[float, ...]
    states: tuple[float, ...]
    capacity: float


@dataclass(frozen=True)
class WorldSpec:
    world_id: str
    input_name: str
    state_name: str
    capacity: float
    lag: int
    inertia: float
    response: float
    phase: float


TRAINING_WORLDS = (
    WorldSpec("reservoir", "inflow", "stored_resource", 80.0, 3, 0.72, 0.55, 0.2),
    WorldSpec("router", "packet_pressure", "queue_load", 240.0, 3, 0.72, 0.55, 1.4),
    WorldSpec("ecosystem", "nutrient_pulse", "population", 35.0, 3, 0.72, 0.55, 2.7),
)

HELD_OUT_WORLD = WorldSpec(
    "thermal_grid", "power_demand", "stored_heat", 520.0, 3, 0.72, 0.55, 4.1
)


def generate_world(spec: WorldSpec, *, steps: int, seed: int) -> Observation:
    """Generate bounded delayed-response data without exposing the mechanism."""
    rng = random.Random(seed)
    scale = spec.capacity
    inputs = [
        scale
        * (
            0.42
            + 0.34 * math.sin(index * 0.31 + spec.phase)
            + 0.16 * math.sin(index * 0.077 + 2 * spec.phase)
        )
        for index in range(steps)
    ]
    inputs = [min(scale, max(0.0, value + rng.gauss(0.0, scale * 0.015))) for value in inputs]
    states = [scale * 0.25] * spec.lag
    for index in range(spec.lag, steps):
        target = inputs[index - spec.lag]
        value = spec.inertia * states[-1] + spec.response * target
        # Capacity makes the otherwise linear correction clip and linger.
        value = min(scale, max(0.0, value + rng.gauss(0.0, scale * 0.008)))
        states.append(value)
    return Observation(
        spec.world_id,
        spec.input_name,
        spec.state_name,
        tuple(inputs),
        tuple(states),
        spec.capacity,
    )


def normalized(observation: Observation) -> tuple[tuple[float, ...], tuple[float, ...]]:
    return (
        tuple(value / observation.capacity for value in observation.inputs),
        tuple(value / observation.capacity for value in observation.states),
    )
