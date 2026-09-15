# Contribuir al complemento digital

Gracias por ayudar a mejorar las simulaciones y el material complementario de la obra.

## Reportar una errata

Use la plantilla de erratas disponible en [GitHub Issues](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/issues/new?template=errata.md). Indique la página o sección, describa el problema y, si es posible, proponga una corrección.

## Proponer un cambio técnico

1. Cree una rama desde `main`.
2. Mantenga los cambios limitados a un problema concreto.
3. No incluya `site/`, salidas de notebooks, checkpoints ni documentos virtuales.
4. Ejecute las validaciones antes de abrir el pull request.

```bash
python -m ruff check .
python -m pytest -q desarrollo/tests
make validate PYTHON=python
```

Cuando cambie una simulación, compruebe su notebook tanto en JupyterLab como en Google Colab. Cuando cambie Pages, ejecute `python -m mkdocs build --strict`.

Las contribuciones deben respetar la licencia del código y los derechos editoriales indicados en [LICENSE](LICENSE).
