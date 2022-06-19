import math
import random


def decrease_temperature(initial_temperature: float, i: int) -> float:
    return initial_temperature * 0.999


def get_transition_probability(delta_e: float, t: float) -> float:
    return math.exp(-delta_e / t)


def is_transition(probability: float) -> bool:
    value: float = random.random()

    if value <= probability:
        return True
    else:
        return False
