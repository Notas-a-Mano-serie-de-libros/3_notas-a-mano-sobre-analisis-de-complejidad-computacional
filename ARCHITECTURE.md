# Arquitectura de los recursos interactivos

## Principios

- Los notebooks contienen narrativa pedagógica y llamadas breves a módulos Python.
- La lógica comprobable vive fuera de los notebooks.
- Los controles, estilos y contratos reutilizables viven en `common/`.
- Cada capítulo separa el punto de entrada público, la lógica y las imágenes.
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

Cada capítulo usa la misma estructura: `notebooks/` contiene el README, los ejercicios
y las simulaciones; `runtime/` contiene bootstraps, launchers y recursos internos; e
`images/` contiene `recursos/` editoriales y `generadas/` para resultados reproducibles.
La lógica de dominio compartida por capítulos permanece en `core/` y los contratos
visuales reutilizables permanecen en `common/`.

## Comprobación

`make check` ejecuta lint, pruebas y validaciones estructurales. Los notebooks deben
permanecer sin outputs; `make clean-notebooks` los normaliza antes de confirmar cambios.
`scripts/validate_repository_paths.py` comprueba enlaces locales, rutas de Colab y
referencias históricas que ya no corresponden a la estructura vigente.
