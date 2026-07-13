from __future__ import annotations


ALGORITHM_NAMES = {
    "burbuja": "ordenamiento burbuja",
    "seleccion": "ordenamiento por selección",
    "insercion": "ordenamiento por inserción",
    "insercion_binaria": "inserción binaria",
    "shell": "ordenamiento Shell",
    "mezcla": "ordenamiento por mezcla",
    "rapido": "ordenamiento rápido",
    "radix": "ordenamiento radix",
}

START_MESSAGES = {
    key: f"Presiona Paso siguiente para iniciar el {name}."
    for key, name in ALGORITHM_NAMES.items()
}
START_MESSAGES["insercion_binaria"] = "Presiona Paso siguiente para iniciar la inserción binaria."

FINAL_MESSAGES = {
    key: f"Finaliza el {name}."
    for key, name in ALGORITHM_NAMES.items()
}
FINAL_MESSAGES["insercion_binaria"] = "Finaliza la inserción binaria."
FINAL_MESSAGES["rapido_hoare"] = "Finaliza el ordenamiento rápido con el esquema de Hoare."


def start_message(algorithm):
    return START_MESSAGES[algorithm]


def final_message(algorithm):
    return FINAL_MESSAGES[algorithm]


def compare_positions_message(left, right):
    return f"Compara las posiciones {left} y {right}."


def swap_positions_message(left, right):
    return f"Intercambia las posiciones {left} y {right}."


def compare_values_message(left, right):
    return f"Compara {left} con {right}."


def radix_bucket_message(digit, value):
    return f"Lee el dígito {digit} de {value} y lo ubica en el bucket {digit}."
