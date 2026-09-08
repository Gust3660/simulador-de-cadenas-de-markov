"""Normalización de matrices y simulación de cadenas de Markov."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MarkovSimulation:
    states: np.ndarray
    counts: np.ndarray
    empirical_probabilities: np.ndarray
    stationary_probabilities: np.ndarray
    transition_matrix: np.ndarray


def normalize_transition(matrix: list[list[float]] | np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2 or values.shape[0] != values.shape[1] or values.shape[0] < 2:
        raise ValueError("La matriz de transición debe ser cuadrada y tener al menos 2 estados.")
    if not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError("Las probabilidades deben ser valores finitos no negativos.")
    row_sums = values.sum(axis=1)
    if np.any(row_sums <= 0):
        raise ValueError("Cada estado debe tener al menos una transición con peso positivo.")
    return values / row_sums[:, None]


def stationary_distribution(matrix: np.ndarray, tolerance: float = 1e-12, max_iterations: int = 100_000) -> np.ndarray:
    probabilities = np.full(matrix.shape[0], 1 / matrix.shape[0])
    for _ in range(max_iterations):
        # Paso perezoso: mantiene la misma distribución estacionaria y ayuda
        # a converger también en cadenas periódicas.
        updated = 0.5 * (probabilities + probabilities @ matrix)
        if np.linalg.norm(updated - probabilities, ord=1) < tolerance:
            return updated / updated.sum()
        probabilities = updated
    return probabilities / probabilities.sum()


def simulate_chain(
    matrix: list[list[float]] | np.ndarray,
    steps: int,
    initial_state: int = 0,
    seed: int = 42,
) -> MarkovSimulation:
    transition = normalize_transition(matrix)
    if steps < 1:
        raise ValueError("El número de pasos debe ser al menos 1.")
    if not 0 <= initial_state < transition.shape[0]:
        raise ValueError("El estado inicial no existe en la matriz.")
    rng = np.random.default_rng(seed)
    states = np.empty(steps + 1, dtype=int)
    states[0] = initial_state
    for index in range(steps):
        states[index + 1] = rng.choice(transition.shape[0], p=transition[states[index]])
    counts = np.bincount(states, minlength=transition.shape[0])
    return MarkovSimulation(
        states=states,
        counts=counts,
        empirical_probabilities=counts / states.size,
        stationary_probabilities=stationary_distribution(transition),
        transition_matrix=transition,
    )
