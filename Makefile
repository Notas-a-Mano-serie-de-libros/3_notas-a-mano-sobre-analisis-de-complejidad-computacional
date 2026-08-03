.PHONY: install test lint validate clean-notebooks clean-graphics check

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PYTHON) scripts/install_git_hooks.py

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .

validate:
	$(PYTHON) scripts/validate_colab_bootstrap.py
	$(PYTHON) scripts/validate_colab_links.py
	$(PYTHON) scripts/validate_notebook_launchers.py
	$(PYTHON) scripts/validate_size_budgets.py
	$(PYTHON) scripts/validate_html_snapshots.py
	$(PYTHON) scripts/validate_widget_contracts.py

clean-notebooks:
	$(PYTHON) scripts/clean_notebooks.py

clean-graphics:
	$(PYTHON) scripts/clean_generated_graphics.py

check: lint test validate
