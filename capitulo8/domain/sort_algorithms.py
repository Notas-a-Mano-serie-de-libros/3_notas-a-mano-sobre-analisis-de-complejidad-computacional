from __future__ import annotations

import random


def ordered(left, right, descending=False):
    return left >= right if descending else left <= right


def relation_symbol(descending=False):
    return "\\ge" if descending else "\\le"


def make_event(values, message, formula, roles=None, labels=None, complete=False, **extra):
    event = {
        "arr": list(values),
        "message": message,
        "formula": formula,
        "roles": list(roles or ["default"] * len(values)),
        "labels": list(labels or [""] * len(values)),
        "sorting_complete": complete,
    }
    event.update(extra)
    return event


def mark(roles, labels, index, role, label=""):
    if 0 <= index < len(roles):
        roles[index] = role
        labels[index] = label


def tree_nodes(item):
    result = [item]
    if item.get("left") is not None:
        result.extend(tree_nodes(item["left"]))
    if item.get("right") is not None:
        result.extend(tree_nodes(item["right"]))
    return result


def tree_ancestors(item):
    result = []
    while item is not None:
        result.append(item)
        item = item.get("parent")
    return result


def active_tree_ids(root, focus=None, visible_nodes=None, complete=False, include_children=True):
    if complete:
        nodes = visible_nodes if visible_nodes is not None else tree_nodes(root)
        return {id(item) for item in nodes}
    focus = focus or root
    result = {id(item) for item in tree_ancestors(focus)}
    if include_children:
        if focus.get("left") is not None:
            result.add(id(focus["left"]))
        if focus.get("right") is not None:
            result.add(id(focus["right"]))
    return result


def bubble_trace(values, descending=False):
    arr = list(values)
    n = len(arr)
    trace = [make_event(arr, "Presiona Paso siguiente para iniciar el ordenamiento burbuja.", r"\text{estado inicial}")]
    for i in range(n - 1):
        swapped = False
        boundary = n - 1 - i
        for j in range(0, boundary):
            roles = ["sorted" if index > boundary else "default" for index in range(n)]
            labels = [""] * n
            mark(roles, labels, boundary, "boundary", "b")
            mark(roles, labels, j, "current", "j")
            mark(roles, labels, j + 1, "compare", "j + 1")
            trace.append(
                make_event(
                    arr,
                    f"Compara las posiciones {j} y {j + 1}.",
                    rf"i = {i},\quad b = n - 1 - i = {boundary},\quad j = {j},\quad a_j = {arr[j]},\quad a_{{j+1}} = {arr[j + 1]},\quad {arr[j]} {relation_symbol(descending)} {arr[j + 1]}",
                    roles,
                    labels,
                )
            )
            if not ordered(arr[j], arr[j + 1], descending):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                roles = ["sorted" if index > boundary else "default" for index in range(n)]
                labels = [""] * n
                mark(roles, labels, boundary, "boundary", "b")
                mark(roles, labels, j, "current", "j")
                mark(roles, labels, j + 1, "compare", "j + 1")
                trace.append(
                    make_event(
                        arr,
                        f"Intercambia las posiciones {j} y {j + 1}.",
                        rf"i = {i},\quad b = {boundary},\quad a_j \leftrightarrow a_{{j+1}},\quad a_j = {arr[j]},\quad a_{{j+1}} = {arr[j + 1]}",
                        roles,
                        labels,
                    )
                )
        roles = ["sorted" if index >= boundary else "default" for index in range(n)]
        labels = [""] * n
        mark(roles, labels, boundary, "sorted", "ordenado")
        trace.append(make_event(arr, f"Fija la posición {boundary}.", rf"i = {i},\quad b = n - 1 - i = {boundary}", roles, labels))
        if not swapped:
            break
    trace.append(make_event(arr, "Finaliza el ordenamiento burbuja.", r"\text{arreglo ordenado}", ["sorted"] * n, [""] * n, True))
    return trace


def selection_trace(values, descending=False):
    arr = list(values)
    n = len(arr)
    candidate_label = "mínimo" if descending else "máximo"
    trace = [make_event(arr, "Presiona Paso siguiente para iniciar el ordenamiento por selección.", r"\text{estado inicial}")]

    def should_replace(candidate, current):
        return current < candidate if descending else current > candidate

    for i in range(n - 1, 0, -1):
        selected = 0
        roles = ["sorted" if index > i else "default" for index in range(n)]
        labels = [""] * n
        mark(roles, labels, i, "boundary", "i")
        mark(roles, labels, selected, "current", candidate_label)
        trace.append(
            make_event(
                arr,
                f"Comienza el recorrido para ubicar el {candidate_label} en la posición {i}.",
                rf"i = {i},\quad j = 1,\quad \text{{{candidate_label}}} = {arr[selected]}",
                roles,
                labels,
            )
        )

        for j in range(1, i + 1):
            candidate_value = arr[selected]
            current_value = arr[j]
            roles = ["sorted" if index > i else "default" for index in range(n)]
            labels = [""] * n
            mark(roles, labels, i, "boundary", "i")
            mark(roles, labels, selected, "current", candidate_label)
            mark(roles, labels, j, "compare", "j")
            trace.append(
                make_event(
                    arr,
                    f"Compara {candidate_value} con {current_value}.",
                    rf"i = {i},\quad j = {j},\quad \text{{{candidate_label}}} = {candidate_value},\quad a_j = {current_value}",
                    roles,
                    labels,
                )
            )
            if should_replace(candidate_value, current_value):
                selected = j
                roles = ["sorted" if index > i else "default" for index in range(n)]
                labels = [""] * n
                mark(roles, labels, i, "boundary", "i")
                mark(roles, labels, selected, "current", candidate_label)
                trace.append(
                    make_event(
                        arr,
                        f"{current_value} es el nuevo {candidate_label}.",
                        rf"i = {i},\quad j = {j},\quad \text{{{candidate_label}}} = {current_value}",
                        roles,
                        labels,
                    )
                )
        if selected != i:
            arr[i], arr[selected] = arr[selected], arr[i]
            roles = ["sorted" if index > i else "default" for index in range(n)]
            labels = [""] * n
            mark(roles, labels, selected, "swap", candidate_label)
            mark(roles, labels, i, "sorted", "ordenado")
            trace.append(
                make_event(
                    arr,
                    f"Intercambia el {candidate_label} con el elemento en la posición {i}.",
                    rf"i = {i},\quad \text{{{candidate_label}}} = {arr[i]}",
                    roles,
                    labels,
                )
            )
        else:
            roles = ["sorted" if index > i else "default" for index in range(n)]
            labels = [""] * n
            mark(roles, labels, i, "sorted", "ordenado")
            trace.append(make_event(arr, f"El {candidate_label} ya está en la posición {i}.", rf"i = {i},\quad \text{{{candidate_label}}} = {arr[i]}", roles, labels))
    trace.append(make_event(arr, "Finaliza el ordenamiento por selección.", r"\text{arreglo ordenado}", ["sorted"] * n, [""] * n, True))
    return trace


def insertion_trace(values, descending=False):
    arr = list(values)
    n = len(arr)
    trace = [make_event(arr, "Presiona Paso siguiente para iniciar el ordenamiento por inserción.", r"\text{estado inicial}")]

    def base_roles(limit):
        return ["current" if index < limit else "default" for index in range(n)]

    for i in range(1, n):
        j = i - 1
        roles = base_roles(i)
        trace.append(make_event(arr, f"Comienza el ordenamiento; inserta el elemento en la posición {i}.", rf"i = {i},\quad j = {j}", roles, [""] * n))

        roles = base_roles(i)
        labels = [""] * n
        mark(roles, labels, i, "compare", "i")
        trace.append(make_event(arr, f"Marca el elemento en la posición {i} para insertarlo.", rf"i = {i},\quad valor = {arr[i]}", roles, labels))

        while j >= 0:
            current_index = j + 1
            current_value = arr[current_index]
            previous_value = arr[j]
            roles = base_roles(i)
            labels = [""] * n
            mark(roles, labels, j, "current", "j")
            mark(roles, labels, current_index, "compare", "i")
            trace.append(make_event(arr, f"Compara {previous_value} con {current_value}.", rf"i = {i},\quad j = {j},\quad a_j = {previous_value},\quad a_i = {current_value}", roles, labels))

            if ordered(previous_value, current_value, descending):
                break

            arr[j], arr[current_index] = arr[current_index], arr[j]
            roles = base_roles(i)
            labels = [""] * n
            mark(roles, labels, j, "compare", "i")
            mark(roles, labels, current_index, "current", "j + 1")
            trace.append(make_event(arr, f"Mueve {current_value} hacia la posición {j}.", rf"i = {i},\quad j = {j},\quad a_j = {arr[j]}", roles, labels))
            j -= 1

        inserted_index = j + 1
        roles = base_roles(i)
        labels = [""] * n
        mark(roles, labels, inserted_index, "sorted", "insertado")
        trace.append(make_event(arr, f"El elemento quedó insertado; actualiza i a la posición {i + 1}.", rf"i = {i + 1},\quad insertado = {inserted_index}", roles, labels))
    trace.append(make_event(arr, "Finaliza el ordenamiento por inserción.", r"\text{arreglo ordenado}", ["sorted"] * n, [""] * n, True))
    return trace


def binary_insertion_trace(values, descending=False):
    arr = list(values)
    n = len(arr)
    trace = [make_event(arr, "Presiona Paso siguiente para iniciar la inserción binaria.", r"\text{estado inicial}")]

    def base_roles(limit):
        return ["current" if index < limit else "default" for index in range(n)]

    for i in range(1, n):
        value = arr[i]
        a = 0
        b = i
        last_m = None
        roles = base_roles(i)
        labels = [""] * n
        mark(roles, labels, i, "compare", "i")
        trace.append(
            make_event(
                arr,
                f"Busca con búsqueda binaria la posición de inserción de {value}.",
                rf"i = {i},\quad x = {value},\quad a = {a},\quad b = {b}",
                roles,
                labels,
            )
        )

        while a < b:
            m = a + (b - a) // 2
            last_m = m
            roles = base_roles(i)
            labels = [""] * n
            mark(roles, labels, i, "compare", "i")
            mark(roles, labels, a, "boundary", "a")
            mark(roles, labels, min(b, i - 1), "boundary", "b")
            mark(roles, labels, m, "boundary", "m")
            trace.append(
                make_event(
                    arr,
                    f"Compara {value} con {arr[m]} en la posición media.",
                    rf"m = a + \left\lfloor \frac{{b-a}}{{2}} \right\rfloor = {m},\quad x = {value},\quad a_m = {arr[m]}",
                    roles,
                    labels,
                )
            )
            goes_right = arr[m] >= value if descending else arr[m] <= value
            if goes_right:
                a = m + 1
                interval = rf"a = m + 1 = {a},\quad b = {b}"
            else:
                b = m
                interval = rf"a = {a},\quad b = m = {b}"
            roles = base_roles(i)
            labels = [""] * n
            mark(roles, labels, i, "compare", "i")
            if a < i:
                mark(roles, labels, a, "boundary", "a")
            if b > 0:
                mark(roles, labels, min(b, i - 1), "boundary", "b")
            if last_m is not None:
                mark(roles, labels, last_m, "boundary", "m")
            trace.append(make_event(arr, "Actualiza el rango de búsqueda.", interval, roles, labels))

        insert_at = a
        roles = base_roles(i)
        labels = [""] * n
        mark(roles, labels, insert_at, "sorted", "pos")
        if last_m is not None:
            mark(roles, labels, last_m, "boundary", "m")
        mark(roles, labels, i, "compare", "i")
        m_formula = rf"m = {last_m},\quad " if last_m is not None else ""
        trace.append(make_event(arr, f"La posición de inserción es {insert_at}.", rf"{m_formula}pos = {insert_at},\quad x = {value}", roles, labels))

        j = i
        while j > insert_at:
            arr[j] = arr[j - 1]
            roles = base_roles(i)
            labels = [""] * n
            mark(roles, labels, j - 1, "current", "j - 1")
            mark(roles, labels, j, "compare", "j")
            if last_m is not None:
                mark(roles, labels, last_m, "boundary", "m")
            trace.append(make_event(arr, f"Desplaza {arr[j]} una posición a la derecha.", rf"j = {j},\quad a_j = a_{{j-1}}", roles, labels))
            j -= 1

        arr[insert_at] = value
        roles = base_roles(i + 1)
        labels = [""] * n
        mark(roles, labels, insert_at, "sorted", "insertado")
        if last_m is not None:
            mark(roles, labels, last_m, "boundary", "m")
        trace.append(make_event(arr, f"Inserta {value} en la posición {insert_at}.", rf"i = {i},\quad insertado = {insert_at}", roles, labels))

    trace.append(make_event(arr, "Finaliza la inserción binaria.", r"\text{arreglo ordenado}", ["sorted"] * n, [""] * n, True))
    return trace


def shell_gaps(n, sequence="shell"):
    if n <= 1:
        return [1]

    if sequence == "hibbard":
        gaps = []
        value = 1
        while value < n:
            gaps.append(value)
            value = 2 * value + 1
        return sorted(set(gaps), reverse=True)

    if sequence == "sedgewick":
        gaps = [1]
        k = 1
        while True:
            even_gap = 9 * (4 ** k) - 9 * (2 ** k) + 1
            odd_gap = (4 ** (k + 1)) - 3 * (2 ** (k + 1)) + 1
            added = False
            for gap in (even_gap, odd_gap):
                if 0 < gap < n:
                    gaps.append(gap)
                    added = True
            if min(even_gap, odd_gap) >= n and not added:
                break
            k += 1
        return sorted(set(gaps), reverse=True)

    if sequence == "pratt":
        gaps = set()
        value_2 = 1
        while value_2 < n:
            value = value_2
            while value < n:
                gaps.add(value)
                value *= 3
            value_2 *= 2
        return sorted(gaps, reverse=True)

    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps or [1]


def shell_gap_formula_terms(n, sequence, gap, order):
    if sequence == "hibbard":
        k = max(1, (gap + 1).bit_length() - 1)
        return (
            rf"salto = 2^k - 1 = 2^{k} - 1 = {gap}",
            rf"k = {k}",
        )

    if sequence == "sedgewick":
        for k in range(1, max(2, n + 2)):
            even_gap = 9 * (4 ** k) - 9 * (2 ** k) + 1
            if even_gap == gap:
                return (
                    rf"salto = 9\cdot4^k - 9\cdot2^k + 1 = 9\cdot4^{k} - 9\cdot2^{k} + 1 = {gap}",
                    rf"k = {k}",
                )
            odd_gap = (4 ** (k + 1)) - 3 * (2 ** (k + 1)) + 1
            if odd_gap == gap:
                return (
                    rf"salto = 4^{{k+1}} - 3\cdot2^{{k+1}} + 1 = 4^{{{k + 1}}} - 3\cdot2^{{{k + 1}}} + 1 = {gap}",
                    rf"k = {k}",
                )
        return rf"salto = Sedgewick(k) = {gap}", r"k \geq 1"

    if sequence == "pratt":
        power_two = 1
        p = 0
        while power_two <= gap:
            power_three = 1
            q = 0
            while power_two * power_three <= gap:
                if power_two * power_three == gap:
                    return (
                        rf"salto = 2^p3^q = 2^{p}3^{q} = {gap}",
                        rf"p = {p},\quad q = {q}",
                    )
                power_three *= 3
                q += 1
            power_two *= 2
            p += 1
        return rf"salto = 2^p3^q = {gap}", r"p,q \geq 0"

    k = order + 1
    return (
        rf"salto = \left\lfloor \frac{{n}}{{2^k}} \right\rfloor = \left\lfloor \frac{{{n}}}{{2^{k}}} \right\rfloor = {gap}",
        rf"n = {n},\quad k = {k}",
    )


def shell_gap_formula(n, sequence, gap, order):
    formula, _terms = shell_gap_formula_terms(n, sequence, gap, order)
    return formula


def shell_formula(first_line, *lines):
    body = r"\\[8pt] ".join((first_line, *[line for line in lines if line]))
    return rf"\begin{{array}}{{l}} {body} \end{{array}}"


def shell_initial_formula(n, sequence="shell"):
    gaps = shell_gaps(n, sequence)
    first_gap = gaps[0] if gaps else 1
    first_line, terms = shell_gap_formula_terms(n, sequence, first_gap, 0)
    gap_values = ", ".join(str(gap) for gap in gaps)
    return shell_formula(first_line, terms, rf"\text{{saltos}} = [{gap_values}]")


def shell_trace(values, descending=False, gap_sequence="shell"):
    arr = list(values)
    n = len(arr)
    gaps = shell_gaps(n, gap_sequence)
    trace = [
        make_event(
            arr,
            "Presiona Paso siguiente para iniciar el ordenamiento Shell.",
            r"\text{estado inicial}",
            gap_sequence=gap_sequence,
            gap_values=list(gaps),
        )
    ]

    def gap_label():
        return ", ".join(str(gap) for gap in gaps)

    for order, gap in enumerate(gaps):
        gap_line, gap_terms = shell_gap_formula_terms(n, gap_sequence, gap, order)
        roles = ["default"] * n
        labels = [""] * n
        for index in range(0, n, gap):
            mark(roles, labels, index, "boundary", "salto")
        trace.append(
            make_event(
                arr,
                f"Inicia la pasada con salto {gap}.",
                shell_formula(gap_line, gap_terms, rf"\text{{saltos}} = [{gap_label()}]"),
                roles,
                labels,
                gap_sequence=gap_sequence,
                gap_values=list(gaps),
            )
        )

        for i in range(gap, n):
            j = i
            roles = ["default"] * n
            labels = [""] * n
            mark(roles, labels, i, "compare", "i")
            mark(roles, labels, i - gap, "current", "j - salto")
            trace.append(
                make_event(
                    arr,
                    f"Compara la posición {i} con la posición {i - gap} usando salto {gap}.",
                    shell_formula(
                        gap_line,
                        gap_terms,
                        rf"i = {i},\quad j = {j}",
                        rf"a_j = {arr[j]},\quad a_{{j-salto}} = {arr[j - gap]}",
                    ),
                    roles,
                    labels,
                    gap_sequence=gap_sequence,
                    gap_values=list(gaps),
                )
            )

            while j >= gap and not ordered(arr[j - gap], arr[j], descending):
                arr[j - gap], arr[j] = arr[j], arr[j - gap]
                roles = ["default"] * n
                labels = [""] * n
                mark(roles, labels, j - gap, "compare", "j - salto")
                mark(roles, labels, j, "current", "j")
                trace.append(
                    make_event(
                        arr,
                        f"Intercambia las posiciones {j - gap} y {j}.",
                        shell_formula(gap_line, gap_terms, rf"j = {j}", rf"a_{{j-salto}} \leftrightarrow a_j"),
                        roles,
                        labels,
                        gap_sequence=gap_sequence,
                        gap_values=list(gaps),
                    )
                )
                j -= gap

            roles = ["default"] * n
            labels = [""] * n
            mark(roles, labels, j, "sorted", "insertado")
            trace.append(
                make_event(
                    arr,
                    f"El elemento queda ubicado dentro de su subarreglo de salto {gap}.",
                    shell_formula(gap_line, gap_terms, rf"i = {i},\quad j = {j}"),
                    roles,
                    labels,
                    gap_sequence=gap_sequence,
                    gap_values=list(gaps),
                )
            )

    trace.append(
        make_event(
            arr,
            "Finaliza el ordenamiento Shell.",
            r"\text{arreglo ordenado}",
            ["sorted"] * n,
            [""] * n,
            True,
            gap_sequence=gap_sequence,
            gap_values=list(gaps),
        )
    )
    return trace


def merge_trace(values, descending=False):
    initial = list(values)
    n = len(initial)

    def node(start, values, depth=0, parent=None):
        item = {
            "start": start,
            "end": start + len(values) - 1,
            "depth": depth,
            "values": list(values),
            "roles": ["default"] * len(values),
            "visible": False,
            "sorted": False,
            "parent": parent,
            "left": None,
            "right": None,
        }
        if len(values) > 1:
            mid = len(values) // 2
            item["left"] = node(start, values[:mid], depth + 1, item)
            item["right"] = node(start + mid, values[mid:], depth + 1, item)
        return item

    root = node(0, initial)
    root["visible"] = True
    all_tree_nodes = tree_nodes(root)
    max_tree_depth = max(item["depth"] for item in all_tree_nodes)
    flat_values = list(initial)
    flat_roles = ["default"] * n

    def snapshot(focus=None, complete=False):
        active = active_tree_ids(root, focus=focus, visible_nodes=all_tree_nodes, complete=complete)
        nodes = []
        for item in all_tree_nodes:
            if not item["visible"]:
                continue
            roles = list(item["roles"]) if id(item) in active else ["excluded"] * len(item["values"])
            nodes.append(
                {
                    "start": item["start"],
                    "end": item["end"],
                    "depth": item["depth"],
                    "values": list(item["values"]),
                    "roles": roles,
                    "active": id(item) in active,
                }
            )
        return nodes

    def tree_meta(focus=None, complete=False):
        return {
            "merge_tree_nodes": snapshot(focus=focus, complete=complete),
            "merge_tree_max_depth": max_tree_depth,
        }

    trace = [
        make_event(
            flat_values,
            "Presiona Paso siguiente para iniciar el ordenamiento por mezcla.",
            r"\text{estado inicial}",
            flat_roles,
            [""] * n,
            **tree_meta(),
        )
    ]

    def set_flat_focus(start=None, end=None):
        for index in range(n):
            if start is None or start <= index <= end:
                flat_roles[index] = "default"
            else:
                flat_roles[index] = "excluded"

    def clear_roles():
        for item in all_tree_nodes:
            item["roles"] = ["default"] * len(item["values"])

    def actions_for(item):
        if len(item["values"]) == 1:
            return [("leaf", item)]
        return [("divide", item)] + actions_for(item["left"]) + actions_for(item["right"]) + [("merge", item)]

    actions = actions_for(root)
    trace.append(
        make_event(
            flat_values,
            "Comienza el ordenamiento.",
            r"fase = \text{inicio}",
            flat_roles,
            [""] * n,
            **tree_meta(focus=root),
        )
    )

    def append_event(message, formula, focus=None, complete=False):
        trace.append(make_event(flat_values, message, formula, flat_roles, [""] * n, complete, **tree_meta(focus=focus, complete=complete)))

    while actions:
        action, current = actions.pop(0)
        clear_roles()

        if action == "divide":
            current["visible"] = True
            current["roles"] = ["current"] * len(current["values"])
            if current["left"] is not None:
                current["left"]["visible"] = True
                current["left"]["roles"] = ["default"] * len(current["left"]["values"])
            if current["right"] is not None:
                current["right"]["visible"] = True
                current["right"]["roles"] = ["default"] * len(current["right"]["values"])
            set_flat_focus(current["start"], current["end"])
            for index in range(current["start"], current["end"] + 1):
                flat_roles[index] = "current"
            append_event(f"Divide el subarreglo {current['values']}.", rf"inicio = {current['start']},\quad fin = {current['end']}", focus=current)
            continue

        if action == "leaf":
            current["visible"] = True
            current["sorted"] = True
            current["roles"] = ["sorted"]
            set_flat_focus(current["start"], current["end"])
            flat_roles[current["start"]] = "sorted"
            append_event(f"El subarreglo [{current['values'][0]}] ya está ordenado.", rf"caso\ base = [{current['values'][0]}]", focus=current)
            continue

        left_values = list(current["left"]["values"])
        right_values = list(current["right"]["values"])
        buffer = [None] * len(current["values"])
        i = j = k = 0
        current["values"] = list(buffer)
        current["roles"] = ["write"] * len(current["values"])
        current["visible"] = True
        current["sorted"] = False
        set_flat_focus(current["start"], current["end"])
        append_event(f"Mezcla {left_values} y {right_values}.", rf"i = 0,\quad j = 0,\quad k = 0", focus=current)

        while True:
            clear_roles()
            current["roles"] = ["write"] * len(current["values"])
            if k >= len(current["values"]):
                current["values"] = list(buffer)
                current["roles"] = ["sorted"] * len(current["values"])
                current["sorted"] = True
                if current["left"] is not None:
                    current["left"]["visible"] = False
                if current["right"] is not None:
                    current["right"]["visible"] = False
                for offset, value in enumerate(current["values"]):
                    flat_values[current["start"] + offset] = value
                    flat_roles[current["start"] + offset] = "sorted"
                append_event("Termina de ordenar el subarreglo.", rf"inicio = {current['start']},\quad fin = {current['end']}", focus=current)
                break

            current["roles"][k] = "write"
            if i < len(current["left"]["roles"]):
                current["left"]["roles"] = ["default"] * len(current["left"]["values"])
                current["left"]["roles"][i] = "current"
            if j < len(current["right"]["roles"]):
                current["right"]["roles"] = ["default"] * len(current["right"]["values"])
                current["right"]["roles"][j] = "compare"

            set_flat_focus(current["start"], current["end"])
            write_index = current["start"] + k
            flat_roles[write_index] = "write"
            if i < len(left_values):
                flat_roles[current["left"]["start"] + i] = "current"
            if j < len(right_values):
                flat_roles[current["right"]["start"] + j] = "compare"

            left = left_values[i] if i < len(left_values) else None
            right = right_values[j] if j < len(right_values) else None
            if left is None:
                message = f"Inserta el elemento restante {right}."
            elif right is None:
                message = f"Inserta el elemento restante {left}."
            else:
                selected = "mayor" if descending else "menor"
                message = f"Compara {left} y {right}; inserta el {selected}."
            append_event(message, rf"i = {i},\quad j = {j},\quad k = {k}", focus=current)

            if right is None or (left is not None and ordered(left, right, descending)):
                value = left
                i += 1
            else:
                value = right
                j += 1
            buffer[k] = value
            current["values"] = list(buffer)
            flat_values[current["start"] + k] = value
            k += 1

    root["roles"] = ["sorted"] * len(root["values"])
    root["sorted"] = True
    flat_roles = ["sorted"] * n
    append_event("Finaliza el ordenamiento por mezcla.", r"\text{arreglo ordenado}", focus=root, complete=True)
    return trace


def choose_pivot(low, high, strategy):
    if strategy == "start":
        return low
    if strategy == "middle":
        return (low + high) // 2
    if strategy == "random":
        return random.randint(low, high)
    return high


def quick_trace(values, descending=False, pivot_strategy="end"):
    initial = list(values)
    n = len(initial)
    pivot_labels = {"start": "inicio", "middle": "medio", "end": "fin", "random": "aleatorio"}

    def node(start, values, depth=0, parent=None):
        return {
            "start": start,
            "end": start + len(values) - 1,
            "depth": depth,
            "values": list(values),
            "roles": ["default"] * len(values),
            "parent": parent,
            "left": None,
            "right": None,
            "is_sorted": False,
        }

    root = node(0, initial)
    visible_nodes = [root]
    pending_nodes = [root]
    sorted_mask = [False] * n
    current = None
    selected_pivot_index = None
    pivot_index = None
    partition_index = None
    scan_index = None
    phase = "start"

    def active_ids(complete=False):
        if complete:
            return active_tree_ids(root, visible_nodes=visible_nodes, complete=True)
        if current is None:
            return {id(root)}
        return active_tree_ids(root, focus=current, visible_nodes=visible_nodes, complete=complete)

    def reset_roles(item, role="default"):
        item["roles"] = [role] * len(item["values"])

    def mark_sorted(item):
        item["roles"] = ["sorted"] * len(item["values"])
        item["is_sorted"] = True

    def sync_with_parent(item):
        parent = item["parent"]
        if parent is None:
            return
        offset = item["start"] - parent["start"]
        for index, value in enumerate(item["values"]):
            parent["values"][offset + index] = value
        sync_with_parent(parent)

    def local_pivot_index(length):
        if pivot_strategy == "start":
            return 0
        if pivot_strategy == "middle":
            return (length - 1) // 2
        if pivot_strategy == "random":
            return random.randint(0, length - 1)
        return length - 1

    def before_pivot(value, pivot_value):
        return value >= pivot_value if descending else value <= pivot_value

    def append_label(groups, index, text):
        if index is not None and 0 <= index < len(groups):
            groups[index].append(text)

    def labels_for_node(item):
        labels = [[] for _ in item["values"]]
        if item is not current:
            return labels
        if item["values"]:
            append_label(labels, 0, "inicio")
            append_label(labels, len(item["values"]) - 1, "fin")
        append_label(labels, partition_index, "i")
        append_label(labels, scan_index, "j")
        pivot_local = pivot_index if pivot_index is not None else selected_pivot_index
        append_label(labels, pivot_local, "pivote")
        ordered_labels = ["inicio", "i", "j", "pivote", "fin"]
        return [[label for label in ordered_labels if label in group] for group in labels]

    def flat_roles_and_labels():
        roles = ["default"] * n
        label_groups = [[] for _ in range(n)]
        if current is not None:
            roles = ["excluded"] * n
            for index in range(current["start"], current["end"] + 1):
                roles[index] = "default"
            append_label(label_groups, current["start"], "inicio")
            append_label(label_groups, current["end"], "fin")
            if partition_index is not None:
                append_label(label_groups, current["start"] + partition_index, "i")
            if scan_index is not None and scan_index < len(current["values"]):
                append_label(label_groups, current["start"] + scan_index, "j")
            pivot_local = pivot_index if pivot_index is not None else selected_pivot_index
            if pivot_local is not None:
                append_label(label_groups, current["start"] + pivot_local, "pivote")
            for local_index, role in enumerate(current["roles"]):
                roles[current["start"] + local_index] = role
        for index, is_sorted in enumerate(sorted_mask):
            if is_sorted:
                roles[index] = "sorted"
        ordered_labels = ["inicio", "i", "j", "pivote", "fin"]
        labels = ["\n".join(label for label in ordered_labels if label in group) for group in label_groups]
        return roles, labels

    def snapshot(complete=False):
        active = active_ids(complete=complete)
        nodes = []
        for item in visible_nodes:
            roles = list(item["roles"])
            labels = labels_for_node(item)
            if id(item) not in active and not complete:
                roles = ["excluded"] * len(item["values"])
                labels = [[] for _ in item["values"]]
            nodes.append(
                {
                    "start": item["start"],
                    "end": item["end"],
                    "depth": item["depth"],
                    "values": list(item["values"]),
                    "roles": roles,
                    "labels": labels,
                    "active": id(item) in active,
                }
            )
        return nodes

    def append_event(message, formula, complete=False):
        roles, labels = flat_roles_and_labels()
        trace.append(
            make_event(
                root["values"],
                message,
                formula,
                roles,
                labels,
                complete,
                quick_tree_nodes=snapshot(complete=complete),
                quick_tree_max_depth=max(1, n - 1),
            )
        )

    trace = []
    append_event("Presiona Paso siguiente para iniciar el ordenamiento rápido.", r"\text{estado inicial}")

    phase = "select_node"
    append_event("Comienza el ordenamiento.", r"fase = \text{inicio}")

    while True:
        if phase == "select_node":
            if not pending_nodes:
                current = None
                selected_pivot_index = None
                pivot_index = None
                partition_index = None
                scan_index = None
                sorted_mask = [True] * n
                mark_sorted(root)
                append_event("Finaliza el ordenamiento rápido.", r"\text{arreglo ordenado}", complete=True)
                break
            current = pending_nodes.pop()
            selected_pivot_index = None
            pivot_index = None
            partition_index = None
            scan_index = None
            reset_roles(current)
            if len(current["values"]) <= 1:
                mark_sorted(current)
                sorted_mask[current["start"]] = True
                append_event(f"El subarreglo {current['values']} ya está ordenado.", rf"caso\ base = {current['values']}")
                current = None
                phase = "select_node"
                continue
            append_event(f"Trabaja sobre el subarreglo {current['values']}.", rf"inicio = {current['start']},\quad fin = {current['end']}")
            phase = "prepare_partition"
            continue

        if phase == "prepare_partition":
            selected_pivot_index = local_pivot_index(len(current["values"]))
            reset_roles(current)
            current["roles"][selected_pivot_index] = "pivot"
            pivot_value = current["values"][selected_pivot_index]
            pivot_label = pivot_labels[pivot_strategy]
            append_event(f"Selecciona el pivote {pivot_value} tomado del {pivot_label}.", rf"pivote = {pivot_value}")
            phase = "move_pivot"
            continue

        if phase == "move_pivot":
            selected_index = selected_pivot_index
            last_index = len(current["values"]) - 1
            selected_value = current["values"][selected_index]
            reset_roles(current)
            if selected_index != last_index:
                end_value = current["values"][last_index]
                current["values"][selected_index], current["values"][last_index] = end_value, selected_value
                sync_with_parent(current)
                current["roles"][selected_index] = "compare"
                current["roles"][last_index] = "pivot"
                message = f"Mueve el pivote {selected_value} al final del subarreglo para particionar."
            else:
                current["roles"][last_index] = "pivot"
                message = "El pivote ya está al final del subarreglo."
            pivot_index = last_index
            partition_index = 0
            scan_index = 0
            append_event(message, rf"pivote = {selected_value},\quad i = 0,\quad j = 0")
            phase = "compare"
            continue

        pivot_value = current["values"][pivot_index]

        if phase == "compare":
            reset_roles(current)
            current["roles"][pivot_index] = "pivot"
            if scan_index >= pivot_index:
                current["roles"][partition_index] = "current"
                append_event(f"Coloca el pivote {pivot_value} en su posición final.", rf"i = {partition_index},\quad pivote = {pivot_value}")
                phase = "place_pivot"
                continue
            current["roles"][partition_index] = "current"
            current["roles"][scan_index] = "compare"
            scan_value = current["values"][scan_index]
            append_event(f"Compara {scan_value} con el pivote {pivot_value}.", rf"i = {partition_index},\quad j = {scan_index},\quad pivote = {pivot_value}")
            phase = "apply_compare"
            continue

        if phase == "apply_compare":
            scan_value = current["values"][scan_index]
            reset_roles(current)
            current["roles"][pivot_index] = "pivot"
            if before_pivot(scan_value, pivot_value):
                if scan_index != partition_index:
                    partition_value = current["values"][partition_index]
                    current["values"][scan_index], current["values"][partition_index] = current["values"][partition_index], current["values"][scan_index]
                    sync_with_parent(current)
                    message = f"Intercambia {scan_value} con {partition_value}."
                else:
                    message = f"{scan_value} permanece antes del pivote."
                current["roles"][partition_index] = "current"
                current["roles"][scan_index] = "compare"
                partition_index += 1
            else:
                current["roles"][scan_index] = "compare"
                if partition_index < len(current["roles"]):
                    current["roles"][partition_index] = "current"
                message = f"{scan_value} permanece después del pivote."
            scan_index += 1
            append_event(message, rf"i = {partition_index},\quad j = {scan_index}")
            phase = "compare"
            continue

        if partition_index != pivot_index:
            current["values"][partition_index], current["values"][pivot_index] = current["values"][pivot_index], current["values"][partition_index]
            sync_with_parent(current)
        reset_roles(current)
        current["roles"][partition_index] = "sorted"
        global_pivot_index = current["start"] + partition_index
        sorted_mask[global_pivot_index] = True
        pivot_value = current["values"][partition_index]
        append_event(f"El pivote {pivot_value} queda ordenado.", rf"p = {global_pivot_index},\quad pivote = {pivot_value}")

        left_values = current["values"][:partition_index]
        right_values = current["values"][partition_index + 1:]
        current["left"] = None
        current["right"] = None
        children = []
        if left_values:
            current["left"] = node(current["start"], left_values, current["depth"] + 1, current)
            children.append(current["left"])
        if right_values:
            current["right"] = node(current["start"] + partition_index + 1, right_values, current["depth"] + 1, current)
            children.append(current["right"])
        visible_nodes.extend(children)
        for child in reversed(children):
            pending_nodes.append(child)
        current = None
        selected_pivot_index = None
        pivot_index = None
        partition_index = None
        scan_index = None
        phase = "select_node"

    return trace


def radix_trace(values, descending=False):
    arr = [int(value) for value in values]
    n = len(arr)
    trace = [
        make_event(
            arr,
            "Presiona Paso siguiente para iniciar el ordenamiento radix.",
            r"\text{estado inicial}",
        )
    ]
    if n == 0:
        trace.append(make_event(arr, "Finaliza el ordenamiento radix.", r"\text{arreglo ordenado}", complete=True))
        return trace
    if any(value < 0 for value in arr):
        raise ValueError("Radix sort requiere valores enteros no negativos")

    max_value = max(arr)
    digit_count = max(1, len(str(max_value)))
    exp = 1

    for digit_index in range(digit_count):
        buckets = [[] for _ in range(10)]
        digit_name = f"10^{digit_index}"
        for index, value in enumerate(arr):
            digit = (value // exp) % 10
            buckets[digit].append(value)
            roles = ["default"] * n
            labels = [""] * n
            mark(roles, labels, index, "compare", "d")
            trace.append(
                make_event(
                    arr,
                    f"Lee el dígito {digit} de {value} y lo ubica en el balde {digit}.",
                    rf"d = \left\lfloor {value}/{digit_name} \right\rfloor \bmod 10 = {digit}",
                    roles,
                    labels,
                )
            )

        ordered_values = []
        bucket_order = range(9, -1, -1) if descending else range(10)
        for bucket in bucket_order:
            ordered_values.extend(buckets[bucket])

        for index, value in enumerate(ordered_values):
            arr[index] = value
            roles = ["default"] * n
            labels = [""] * n
            mark(roles, labels, index, "write", "k")
            trace.append(
                make_event(
                    arr,
                    f"Escribe {value} en la posición {index} según el dígito {digit_index}.",
                    rf"k = {index},\quad 10^{digit_index},\quad a_k = {value}",
                    roles,
                    labels,
                )
            )

        exp *= 10
        trace.append(
            make_event(
                arr,
                f"Finaliza la pasada del dígito {digit_index}.",
                rf"10^{digit_index}\ \text{{procesado}}",
                ["sorted"] * n if digit_index == digit_count - 1 else ["default"] * n,
                [""] * n,
            )
        )

    trace.append(make_event(arr, "Finaliza el ordenamiento radix.", r"\text{arreglo ordenado}", ["sorted"] * n, [""] * n, True))
    return trace


TRACE_BUILDERS = {
    "burbuja": bubble_trace,
    "seleccion": selection_trace,
    "insercion": insertion_trace,
    "insercion_binaria": binary_insertion_trace,
    "shell": shell_trace,
    "mezcla": merge_trace,
    "rapido": quick_trace,
    "radix": radix_trace,
}



__all__ = [
    "bubble_trace",
    "selection_trace",
    "insertion_trace",
    "binary_insertion_trace",
    "shell_gaps",
    "shell_trace",
    "merge_trace",
    "quick_trace",
    "radix_trace",
    "TRACE_BUILDERS",
]
