test: venv/.requirements_installed
	. venv/bin/activate; black --check .; isort --check-only; flake8 --exclude .git,venv,__pycache__,build,dist; pytest

format: venv/.requirements_installed
	. venv/bin/activate; isort -y; black .

venv/.requirements_installed: venv/bin/activate requirements.txt
	. venv/bin/activate; pip install --upgrade pip; pip install -q -r requirements.txt
	@touch venv/.requirements_installed

venv/bin/activate:
	python3 -m venv venv

clean:
	rm -Rf venv

.PHONY: clean test
