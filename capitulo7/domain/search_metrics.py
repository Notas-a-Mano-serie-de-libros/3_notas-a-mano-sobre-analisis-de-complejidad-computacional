from __future__ import annotations

import math


def count_sequential(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index + 1
    return len(values)


def count_binary(values, target):
    low, high = 0, len(values) - 1
    steps = 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if values[mid] == target:
            return steps
        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return steps


def count_ternary(values, target):
    left, right = 0, len(values) - 1
    steps = 0
    while left <= right:
        m1 = math.floor(left + (right - left) / 3)
        m2 = math.floor(right - (right - left) / 3)
        steps += 1
        if values[m1] == target:
            return steps
        steps += 1
        if values[m2] == target:
            return steps
        if target < values[m1]:
            right = m1 - 1
        elif target > values[m2]:
            left = m2 + 1
        else:
            left = m1 + 1
            right = m2 - 1
    return steps


def count_jump(values, target):
    n = len(values)
    if n == 0:
        return 0
    jump = max(1, int(math.sqrt(n)))
    previous = 0
    current = min(jump, n)
    steps = 0
    while previous < n:
        steps += 1
        if target <= values[min(current, n) - 1]:
            break
        previous = current
        current = min(current + jump, n)
        if previous >= n:
            return steps
    for index in range(previous, min(current, n)):
        steps += 1
        if values[index] == target:
            return steps
    return steps


def count_exponential(values, target):
    n = len(values)
    if n == 0:
        return 0
    steps = 1
    if values[0] == target:
        return steps
    bound = 1
    while bound < n and values[bound] <= target:
        steps += 1
        if values[bound] == target:
            return steps
        bound *= 2
    low = bound // 2
    high = min(bound, n - 1)
    return steps + count_binary(values[low:high + 1], target)


def count_interpolation(values, target):
    low, high = 0, len(values) - 1
    steps = 0
    while low <= high and values[low] <= target <= values[high]:
        steps += 1
        if low == high:
            return steps
        denominator = values[high] - values[low]
        if denominator == 0:
            return steps
        pos = low + ((high - low) * (target - values[low])) // denominator
        if pos < low or pos > high:
            return steps
        if values[pos] == target:
            return steps
        if values[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return steps


STEP_COUNTERS = {
    "Binaria": count_binary,
    "Ternaria": count_ternary,
    "Exponencial": count_exponential,
    "Interpolación": count_interpolation,
    "Saltos": count_jump,
    "Secuencial": count_sequential,
}


def count_search_steps(name: str, values, target) -> int:
    return STEP_COUNTERS[name](values, target)


__all__ = [
    "STEP_COUNTERS",
    "count_binary",
    "count_exponential",
    "count_interpolation",
    "count_jump",
    "count_search_steps",
    "count_sequential",
    "count_ternary",
]
