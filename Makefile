.PHONY: book-review install test lint validate clean-notebooks clean-graphics clean-project check docs-install docs-serve docs-build docs-validate check-links

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements-dev.txt -c requirements-lock.txt
	$(PYTHON) desarrollo/scripts/install_git_hooks.py

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .

validate:
	$(PYTHON) desarrollo/scripts/validate_book_structure.py
	$(PYTHON) desarrollo/scripts/validate_page_assets.py
	$(PYTHON) desarrollo/scripts/validate_external_references.py
	$(PYTHON) desarrollo/scripts/validate_repository_paths.py
	$(PYTHON) desarrollo/scripts/validate_colab_bootstrap.py
	$(PYTHON) desarrollo/scripts/validate_colab_links.py
	$(PYTHON) desarrollo/scripts/validate_notebook_launchers.py
	$(PYTHON) desarrollo/scripts/validate_size_budgets.py
	$(PYTHON) desarrollo/scripts/validate_html_snapshots.py
	$(PYTHON) desarrollo/scripts/validate_widget_contracts.py
	$(PYTHON) desarrollo/scripts/validate_editorial_content.py
	$(PYTHON) desarrollo/scripts/sync_local_execution.py --check
	$(PYTHON) desarrollo/scripts/sync_page_assets.py --check
	$(PYTHON) desarrollo/scripts/audit_simulation_references.py

clean-notebooks:
	$(PYTHON) desarrollo/scripts/clean_notebooks.py

clean-graphics:
	$(PYTHON) desarrollo/scripts/clean_generated_graphics.py

clean-project:
	$(PYTHON) desarrollo/scripts/clean_project.py

check-links:
	$(PYTHON) desarrollo/scripts/check_published_links.py --live

check: lint test validate audit-simulations

docs-install:
	$(PYTHON) -m pip install -r requirements-docs.txt -c requirements-lock.txt

docs-serve:
	$(PYTHON) desarrollo/scripts/sync_page_assets.py
	$(PYTHON) desarrollo/scripts/sync_local_execution.py
	$(PYTHON) desarrollo/scripts/build_java_examples.py
	$(PYTHON) desarrollo/scripts/build_c_examples.py --check
	$(PYTHON) -m mkdocs serve

docs-build:
	$(PYTHON) desarrollo/scripts/sync_page_assets.py
	$(PYTHON) desarrollo/scripts/sync_local_execution.py
	$(PYTHON) desarrollo/scripts/build_java_examples.py
	$(PYTHON) desarrollo/scripts/build_c_examples.py --check
	$(PYTHON) -m mkdocs build --strict

docs-validate: docs-build
	$(PYTHON) desarrollo/scripts/validate_editorial_content.py
	$(PYTHON) desarrollo/scripts/validate_pages_breadcrumbs.py --site-dir site

book-review:
	$(PYTHON) desarrollo/scripts/review_book_code.py

.PHONY: audit-simulations
audit-simulations:
	$(PYTHON) desarrollo/scripts/audit_simulation_references.py
