from __future__ import annotations

from sort_algorithms import ordered


def split_tree(values, start=0, depth=0):
    node = {"start": start, "end": start + len(values) - 1, "depth": depth, "values": list(values), "children": []}
    if len(values) > 1:
        mid = len(values) // 2
        node["children"] = [
            split_tree(values[:mid], start, depth + 1),
            split_tree(values[mid:], start + mid, depth + 1),
        ]
    return node


def quick_pivot_index(length, strategy):
    if strategy == "start":
        return 0
    if strategy == "middle":
        return length // 2
    return length - 1


def quick_tree(values, start=0, depth=0, descending=False, pivot_strategy="end"):
    node = {"start": start, "end": start + len(values) - 1, "depth": depth, "values": list(values), "children": []}
    if len(values) <= 1:
        return node
    pivot_index = quick_pivot_index(len(values), pivot_strategy)
    pivot_value = values[pivot_index]
    rest = values[:pivot_index] + values[pivot_index + 1:]
    left = [value for value in rest if ordered(value, pivot_value, descending)]
    right = [value for value in rest if not ordered(value, pivot_value, descending)]
    children = []
    if left:
        children.append(quick_tree(left, start, depth + 1, descending, pivot_strategy))
    pivot_start = start + len(left)
    children.append({"start": pivot_start, "end": pivot_start, "depth": depth + 1, "values": [pivot_value], "children": [], "pivot": True})
    if right:
        children.append(quick_tree(right, pivot_start + 1, depth + 1, descending, pivot_strategy))
    node["children"] = children
    return node


def flatten_tree(node):
    nodes = [node]
    for child in node.get("children", []):
        nodes.extend(flatten_tree(child))
    return nodes


def tree_depth(node):
    return max(item["depth"] for item in flatten_tree(node))


def tree_max_depth_for_state(state):
    algorithm = state.get("algorithm")
    if algorithm == "mezcla" and "merge_tree_max_depth" in state:
        return state["merge_tree_max_depth"]
    if algorithm == "rapido" and "quick_tree_max_depth" in state:
        return state["quick_tree_max_depth"]
    values = state.get("initial_values", state["arr"])
    root = quick_tree(values, descending=state.get("descending", False), pivot_strategy=state.get("pivot_strategy", "end")) if algorithm == "rapido" else split_tree(values)
    return tree_depth(root)


def range_key(node):
    return (node["start"], node["end"])


def find_tree_node(node, target):
    if range_key(node) == target:
        return node
    for child in node.get("children", []):
        found = find_tree_node(child, target)
        if found is not None:
            return found
    return None


def ancestor_ranges(node, target):
    if range_key(node) == target:
        return {target}
    for child in node.get("children", []):
        child_ranges = ancestor_ranges(child, target)
        if child_ranges:
            child_ranges.add(range_key(node))
            return child_ranges
    return set()


def merge_active_ranges(root, focus):
    if focus is None:
        return {range_key(root)}
    active = ancestor_ranges(root, focus)
    focus_node = find_tree_node(root, focus)
    if focus_node is not None:
        active.update(range_key(child) for child in focus_node.get("children", []))
    return active
