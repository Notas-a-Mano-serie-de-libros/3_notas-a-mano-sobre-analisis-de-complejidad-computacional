# Política de dependencias reproducibles

La compatibilidad oficial es Python 3.11 y 3.12. Los archivos raíz separan los alcances:

- `requirements-ci.txt`: pruebas, análisis y benchmarks;
- `requirements-docs.txt`: documentación estática;
- `requirements-publish.txt`: documentación y artefacto JupyterLite;
- `requirements-dev.txt`: entorno local completo;
- `requirements-lock.txt`: restricciones directas comunes mientras se adoptan los locks PEP 751.

## Generación de locks completos

Los locks deben resolverse en una máquina con los intérpretes oficiales y acceso al índice, nunca copiando `pip freeze` desde otra versión de Python:

```text
python3.11 -m pip lock -r requirements-ci.txt -c requirements-lock.txt -o pylock.ci.python311.toml
python3.11 -m pip lock -r requirements-publish.txt -c requirements-lock.txt -o pylock.publish.python311.toml
python3.12 -m pip lock -r requirements-ci.txt -c requirements-lock.txt -o pylock.ci.python312.toml
python3.12 -m pip lock -r requirements-publish.txt -c requirements-lock.txt -o pylock.publish.python312.toml
```

Antes de versionarlos se debe comprobar que cada dependencia transitiva tenga una versión exacta y hashes de sus archivos, ejecutar las pruebas con cada lock y auditar ambos entornos con `pip-audit`. La actualización de un lock es un cambio revisable: no se aceptan URL VCS flotantes, rutas locales ni dependencias sin hash.
