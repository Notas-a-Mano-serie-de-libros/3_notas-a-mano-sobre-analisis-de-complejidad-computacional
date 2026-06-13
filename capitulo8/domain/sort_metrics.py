from __future__ import annotations


def ordered(left, right, descending=False):
    return left >= right if descending else left <= right


def count_bubble(values, descending=False):
    arr = list(values)
    n = len(arr)
    steps = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            steps += 1
            if not ordered(arr[j], arr[j + 1], descending):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps += 1
        steps += 1
        if not swapped:
            break
    return steps + 1


def count_selection(values, descending=False):
    arr = list(values)
    n = len(arr)
    steps = 0

    def should_replace(candidate, current):
        return current < candidate if descending else current > candidate

    for i in range(n - 1, 0, -1):
        selected = 0
        steps += 1
        for j in range(1, i + 1):
            steps += 1
            if should_replace(arr[selected], arr[j]):
                selected = j
                steps += 1
        if selected != i:
            arr[i], arr[selected] = arr[selected], arr[i]
        steps += 1
    return steps + 1


def count_insertion(values, descending=False):
    arr = list(values)
    steps = 0
    for i in range(1, len(arr)):
        steps += 2
        j = i - 1
        while j >= 0:
            current_index = j + 1
            steps += 1
            if ordered(arr[j], arr[current_index], descending):
                break
            arr[j], arr[current_index] = arr[current_index], arr[j]
            steps += 1
            j -= 1
        steps += 1
    return steps + 1


def count_merge(values, descending=False):
    arr = list(values)
    steps = 0

    def merge_sort(items):
        nonlocal steps
        if len(items) <= 1:
            steps += 1
            return items

        steps += 1
        mid = len(items) // 2
        left = merge_sort(items[:mid])
        right = merge_sort(items[mid:])
        merged = []
        i = j = 0
        steps += 1
        while i < len(left) or j < len(right):
            if i >= len(left):
                merged.append(right[j])
                j += 1
            elif j >= len(right):
                merged.append(left[i])
                i += 1
            else:
                steps += 1
                if ordered(left[i], right[j], descending):
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            steps += 1
        steps += 1
        return merged

    merge_sort(arr)
    return steps + 1


def pivot_index(values, strategy):
    if strategy == "start":
        return 0
    if strategy == "middle":
        return len(values) // 2
    return len(values) - 1


def count_quick(values, descending=False, pivot_strategy="end"):
    arr = list(values)
    steps = 0

    def quick(items):
        nonlocal steps
        if len(items) <= 1:
            steps += 1
            return items

        pivot_pos = pivot_index(items, pivot_strategy)
        pivot = items[pivot_pos]
        rest = items[:pivot_pos] + items[pivot_pos + 1:]
        left = []
        right = []
        steps += 2
        for value in rest:
            steps += 1
            goes_left = value > pivot if descending else value <= pivot
            if goes_left:
                left.append(value)
            else:
                right.append(value)
        steps += 1
        return quick(left) + [pivot] + quick(right)

    quick(arr)
    return steps + 1


def count_radix(values, descending=False):
    arr = [int(value) for value in values]
    if not arr:
        return 1
    digit_count = max(1, len(str(max(arr))))
    return digit_count * (2 * len(arr) + 1) + 1


OPERATION_COUNTERS = {
    "burbuja": count_bubble,
    "seleccion": count_selection,
    "insercion": count_insertion,
    "mezcla": count_merge,
    "rapido": count_quick,
    "radix": count_radix,
}


def count_sort_operations(key: str, values, descending=False) -> int:
    return OPERATION_COUNTERS[key](values, descending=descending)


__all__ = [
    "OPERATION_COUNTERS",
    "count_bubble",
    "count_insertion",
    "count_merge",
    "count_quick",
    "count_radix",
    "count_selection",
    "count_sort_operations",
    "ordered",
    "pivot_index",
]
