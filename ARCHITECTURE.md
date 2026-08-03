# Arquitectura de los recursos interactivos

## Principios

- Los notebooks contienen narrativa pedagógica y llamadas breves a módulos Python.
- La lógica comprobable vive fuera de los notebooks.
- Los controles, estilos y contratos reutilizables viven en `common/`.
- Cada capítulo mantiene su lógica de dominio cerca de sus notebooks.
- Los resultados generados y los estados de widgets no se versionan.

## Capas

```text
notebook
  └── bootstrap o launcher del capítulo
        └── módulo de dominio
              ├── common/widget_controls.py
              ├── common/experimental_simulation.py
              └── common/*_runtime.py
```

Los capítulos 2, 4 y 6 usan `common/experimental_simulation.py` como contrato para
normalizar la configuración y construir los tamaños de entrada. El capítulo 6
reutiliza el motor experimental del capítulo 4 para evitar una tercera implementación.

Los capítulos 7 y 8 separan explícitamente `notebooks/` y `domain/`. Para capítulos
anteriores se conserva la ubicación pública de los notebooks, pero cualquier función
nueva debe agregarse a un módulo Python, no a una celda extensa.

## Comprobación

`make check` ejecuta lint, pruebas y validaciones estructurales. Los notebooks deben
permanecer sin outputs; `make clean-notebooks` los normaliza antes de confirmar cambios.
